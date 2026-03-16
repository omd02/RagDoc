from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_documents
from src.retrieval.embeddings import EmbeddingModel
from src.retrieval.vector_store import VectorStore  
from src.database.db import Database
from pathlib import Path


class RAGPipeline:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

        self.vector_store.load()

        self.db = Database()

    def index_document(self, pdf_path):

        filename = Path(pdf_path).name

        self.db.add_document(filename, pdf_path)

        documents = load_pdf(pdf_path)

        chunks = chunk_documents(documents)

        embedded_chunks = self.embedding_model.embed_documents(chunks)

        self.vector_store.add_embeddings(embedded_chunks)

        self.vector_store.save()

    def retrieve(self, query, top_k=5):

        query_embedding = self.embedding_model.model.encode(query)

        results = self.vector_store.search(query_embedding, top_k)

        return results