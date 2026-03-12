import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension=384):
        """
        Initialize FAISS index using cosine similarity.
        """

        self.dimension = dimension

        # Inner product index (used for cosine similarity)
        self.index = faiss.IndexFlatIP(dimension)

        self.chunks = []

    def add_embeddings(self, chunks):
        """
        Add chunk embeddings to the index.
        """

        embeddings = [chunk["embedding"] for chunk in chunks]

        embeddings = np.array(embeddings).astype("float32")

        # Normalize vectors for cosine similarity
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

        self.chunks.extend(chunks)

    def search(self, query_embedding, top_k=5):
        """
        Search for most similar chunks.
        """

        query_vector = np.array([query_embedding]).astype("float32")

        # Normalize query vector
        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results