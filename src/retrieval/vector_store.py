import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:

    def __init__(self, dimension=384):

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks = []

    def add_embeddings(self, chunks, user_id: int):
        print(f"Adding {len(chunks)} embeddings to the index for user {user_id}")
        embeddings = []
        for chunk in chunks:
            chunk["user_id"] = user_id
            embeddings.append(chunk["embedding"])

        embeddings = np.array(embeddings).astype("float32")
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.chunks.extend(chunks)
        print(f"Total chunks in memory: {len(self.chunks)}")

    def search(self, query_embedding, user_id: int, top_k=5):
        print(f"Searching index for user {user_id}. Total chunks: {len(self.chunks)}")
        query_vector = np.array([query_embedding]).astype("float32")
        faiss.normalize_L2(query_vector)

        # Search more than top_k to allow for filtering
        scores, indices = self.index.search(query_vector, min(len(self.chunks), top_k * 10) if len(self.chunks) > 0 else 0)

        results = []
        for idx in indices[0]:
            if idx == -1: continue
            chunk = self.chunks[idx]
            if chunk.get("user_id") == user_id:
                results.append(chunk)
                if len(results) >= top_k:
                    break

        print(f"Found {len(results)} matching chunks for user {user_id}")
        return results

    def save(self, path="storage"):

        Path(path).mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, f"{path}/faiss.index")

        with open(f"{path}/chunks.pkl", "wb") as f:
            pickle.dump(self.chunks, f)

    def load(self, path="storage"):

        index_path = Path(f"{path}/faiss.index")

        metadata_path = Path(f"{path}/chunks.pkl")

        if index_path.exists() and metadata_path.exists():

            self.index = faiss.read_index(str(index_path))

            with open(metadata_path, "rb") as f:
                self.chunks = pickle.load(f)

            print("Vector index loaded.")

        else:

            print("No saved index found.")