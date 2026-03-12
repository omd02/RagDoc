from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_documents
from src.retrieval.embeddings import EmbeddingModel
from src.retrieval.vector_store import VectorStore


class RAGPipeline:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

    def index_document(self, pdf_path):
        """
        Process and index a document.
        """

        documents = load_pdf(pdf_path)

        chunks = chunk_documents(documents)

        embedded_chunks = self.embedding_model.embed_documents(chunks)

        self.vector_store.add_embeddings(embedded_chunks)

    def retrieve(self, query, top_k=5):
        """
        Retrieve relevant chunks for a query.
        """

        query_embedding = self.embedding_model.model.encode(query)

        results = self.vector_store.search(query_embedding, top_k)

        return results