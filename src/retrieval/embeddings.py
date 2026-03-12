from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the embedding model.
        """
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, chunks):
        """
        Generate embeddings for chunk texts.

        Args:
            chunks (list): list of chunk dictionaries

        Returns:
            list: chunks with embeddings
        """

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(texts)

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

        return chunks