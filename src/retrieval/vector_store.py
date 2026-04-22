import faiss
import numpy as np
import pickle
import gc # For explicit memory cleanup
from pathlib import Path
from rank_bm25 import BM25Okapi

# Resilient import for TextCrossEncoder
try:
    from fastembed import TextCrossEncoder
except ImportError:
    try:
        from fastembed.rerank.cross_encoder import TextCrossEncoder
    except ImportError:
        try:
            from fastembed import TextReranker as TextCrossEncoder
        except ImportError:
            raise ImportError("Could not import TextCrossEncoder or TextReranker from fastembed.")


class VectorStore:

    def __init__(self, dimension=384):

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks = []
        self.bm25 = None
        self.reranker = None 

    def _get_reranker(self):
        # We don't use self.reranker here to allow explicit deletion in search
        return TextCrossEncoder(model_name="Xenova/ms-marco-MiniLM-L-6-v2", threads=1)

    def _tokenize(self, text):
        """Simple tokenizer for BM25."""
        return text.lower().split()

    def add_embeddings(self, chunks, user_id: int):
        print(f"Adding {len(chunks)} embeddings to the index for user {user_id}")
        embeddings = []
        for chunk in chunks:
            chunk["user_id"] = user_id
            embeddings.append(chunk["embedding"])
            
            # Temporary tokens for BM25 build
            chunk["_tmp_tokens"] = self._tokenize(chunk["text"])

        embeddings = np.array(embeddings).astype("float32")
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.chunks.extend(chunks)
        
        # Build BM25 and then CLEAN UP
        corpus = [c["_tmp_tokens"] for c in self.chunks]
        self.bm25 = BM25Okapi(corpus)
        
        # CRITICAL: Remove heavy data from RAM
        for c in self.chunks:
            if "embedding" in c: del c["embedding"]
            if "_tmp_tokens" in c: del c["_tmp_tokens"]
            if "tokens" in c: del c["tokens"]
        
        gc.collect() # Force cleanup
        print(f"Total chunks in memory: {len(self.chunks)}")

    def search(self, query_text: str, query_embedding, user_id: int, top_k=5):
        print(f"Searching for: '{query_text}' for user {user_id}")
        
        # 1. Vector Search
        query_vector = np.array([query_embedding]).astype("float32")
        faiss.normalize_L2(query_vector)
        v_scores, v_indices = self.index.search(query_vector, min(len(self.chunks), 30))
        
        # 2. BM25 Search
        # Re-tokenize query on the fly
        tokenized_query = self._tokenize(query_text)
        bm25_scores = self.bm25.get_scores(tokenized_query) if self.bm25 else []
        
        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores = {}
        k = 60
        
        for rank, idx in enumerate(v_indices[0]):
            if idx == -1: continue
            if self.chunks[idx].get("user_id") == user_id:
                rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (rank + k)
                
        bm25_ranks = np.argsort(bm25_scores)[::-1]
        for rank, idx in enumerate(bm25_ranks):
            if bm25_scores[idx] <= 0: continue
            if self.chunks[idx].get("user_id") == user_id:
                rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (rank + k)
                
        sorted_indices = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
        top_candidates = [self.chunks[i] for i in sorted_indices[:8]] # Very tight pool for RAM

        if not top_candidates:
            return []

        # 4. Use-and-Toss Re-ranking
        # Load, use, and immediately discard to keep RAM < 512MB
        try:
            reranker = self._get_reranker()
            top_texts = [c["text"] for c in top_candidates]
            rerank_results = list(reranker.rerank(query_text, top_texts))
            
            for i, score in enumerate(rerank_results):
                top_candidates[i]["rerank_score"] = score
            
            # Explicitly delete reranker and trigger GC
            del reranker
            gc.collect()
        except Exception as e:
            print(f"Reranking skipped due to memory/error: {e}")
            # Fallback to RRF order
            for i, c in enumerate(top_candidates):
                c["rerank_score"] = 1.0 / (i + 1)
            
        final_results = sorted(top_candidates, key=lambda x: x.get("rerank_score", -100), reverse=True)
        return final_results[:top_k]

    def save(self, path="storage"):
        Path(path).mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, f"{path}/faiss.index")
        
        # Don't save tokens/embeddings in the pickle to save space if needed, 
        # but for now, we keep them for simplicity.
        with open(f"{path}/chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self, path="storage"):
        index_path = Path(f"{path}/faiss.index")
        metadata_path = Path(f"{path}/chunks.pkl")

        if index_path.exists() and metadata_path.exists():
            self.index = faiss.read_index(str(index_path))
            with open(metadata_path, "rb") as f:
                self.chunks = pickle.load(f)
            
            # Re-initialize BM25 from loaded chunks
            corpus = [c.get("tokens", self._tokenize(c["text"])) for c in self.chunks]
            if corpus:
                self.bm25 = BM25Okapi(corpus)
            
            print(f"Vector index and BM25 loaded with {len(self.chunks)} chunks.")
        else:
            print("No saved index found.")
