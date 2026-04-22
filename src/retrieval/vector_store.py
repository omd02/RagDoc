import faiss
import numpy as np
import pickle
from pathlib import Path
from rank_bm25 import BM25Okapi
from fastembed import TextReranker


class VectorStore:

    def __init__(self, dimension=384):

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks = []
        self.bm25 = None
        # Using fastembed's ONNX-based re-ranker for extreme memory efficiency (<100MB RAM)
        self.reranker = TextReranker(model_name="mixedbread-ai/mxbai-rerank-xsmall-v1")

    def _tokenize(self, text):
        """Simple tokenizer for BM25."""
        return text.lower().split()

    def add_embeddings(self, chunks, user_id: int):
        print(f"Adding {len(chunks)} embeddings to the index for user {user_id}")
        embeddings = []
        for chunk in chunks:
            chunk["user_id"] = user_id
            # Pre-tokenize for BM25
            chunk["tokens"] = self._tokenize(chunk["text"])
            embeddings.append(chunk["embedding"])

        embeddings = np.array(embeddings).astype("float32")
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.chunks.extend(chunks)
        
        # Re-initialize BM25 with all chunks
        corpus = [c["tokens"] for c in self.chunks]
        self.bm25 = BM25Okapi(corpus)
        
        print(f"Total chunks in memory: {len(self.chunks)}")

    def search(self, query_text: str, query_embedding, user_id: int, top_k=5, use_hybrid=True):
        """
        Performs search using Vector search, BM25, RRF, and Cross-Encoder Re-ranking.
        """
        print(f"Searching for: '{query_text}' for user {user_id}")
        
        # 1. Vector Search
        query_vector = np.array([query_embedding]).astype("float32")
        faiss.normalize_L2(query_vector)
        # Search more than top_k for filtering and fusion
        v_scores, v_indices = self.index.search(query_vector, min(len(self.chunks), 50))
        
        # 2. BM25 Search
        tokenized_query = self._tokenize(query_text)
        bm25_scores = self.bm25.get_scores(tokenized_query) if self.bm25 else []
        
        # 3. Reciprocal Rank Fusion (RRF)
        # We combine the rankings from both methods
        rrf_scores = {}
        k = 60 # Standard constant for RRF
        
        # Vector rankings
        for rank, idx in enumerate(v_indices[0]):
            if idx == -1: continue
            if self.chunks[idx].get("user_id") == user_id:
                rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (rank + k)
                
        # BM25 rankings (sort scores to get ranks)
        bm25_ranks = np.argsort(bm25_scores)[::-1]
        for rank, idx in enumerate(bm25_ranks):
            if bm25_scores[idx] <= 0: continue # Only consider relevant matches
            if self.chunks[idx].get("user_id") == user_id:
                rrf_scores[idx] = rrf_scores.get(idx, 0) + 1 / (rank + k)
                
        # Sort by RRF score
        sorted_indices = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
        top_candidates = [self.chunks[i] for i in sorted_indices[:20]] # Take top 20 for re-ranking

        if not top_candidates:
            return []

        # 4. Cross-Encoder Re-ranking (FastEmbed ONNX version)
        # fastembed.rerank takes a query and a list of texts
        top_texts = [c["text"] for c in top_candidates]
        rerank_results = list(self.reranker.rerank(query_text, top_texts))
        
        # fastembed returns objects with 'index' and 'score'
        # We match them back to our candidates
        for res in rerank_results:
            top_candidates[res.index]["rerank_score"] = res.score
            
        final_results = sorted(top_candidates, key=lambda x: x.get("rerank_score", -100), reverse=True)
        
        print(f"Found {len(final_results[:top_k])} high-quality chunks after re-ranking")
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