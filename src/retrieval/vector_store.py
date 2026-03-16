import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:

    def __init__(self, dimension=384):

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks = []

    def add_embeddings(self, chunks):

        embeddings = [chunk["embedding"] for chunk in chunks]

        embeddings = np.array(embeddings).astype("float32")

        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

        self.chunks.extend(chunks)

    def search(self, query_embedding, top_k=5):

        query_vector = np.array([query_embedding]).astype("float32")

        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for idx in indices[0]:
            results.append(self.chunks[idx])

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