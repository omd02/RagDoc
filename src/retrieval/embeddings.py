from fastembed import TextEmbedding
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        # fastembed is much lighter than sentence-transformers and doesn't require torch
        # "BAAI/bge-small-en-v1.5" is a high-performance, small model (384 dim)
        self.model = TextEmbedding(model_name=model_name)

    def encode(self, text):
        """
        Encode a single string or a list of strings.
        Returns a single embedding if text is a string, or a list of embeddings if text is a list.
        """
        if isinstance(text, str):
            # embed() returns a generator
            return list(self.model.embed([text]))[0]
        else:
            return list(self.model.embed(text))

    def embed_documents(self, chunks):
        """
        Generate embeddings for chunk texts with contextual metadata.
        """
        texts = [chunk["text"] for chunk in chunks]
        
        # fastembed.embed returns a generator of embeddings
        embeddings = list(self.model.embed(texts))

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

        return chunks
