from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_documents
from src.retrieval.embeddings import EmbeddingModel
from src.retrieval.vector_store import VectorStore
from src.generation.rag_pipeline import Generator, DocumentGrader
from src.database.db import Database
from pathlib import Path


class RAGPipeline:

    def __init__(self):

        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()
        self.generator = Generator()
        self.grader = DocumentGrader()

        self.vector_store.load()

    def index_document(self, pdf_path, user_id: int):

        documents = load_pdf(pdf_path)

        chunks = chunk_documents(documents)

        embedded_chunks = self.embedding_model.embed_documents(chunks)

        self.vector_store.add_embeddings(embedded_chunks, user_id)

        self.vector_store.save()

    def retrieve(self, query, user_id: int, top_k=5):

        query_embedding = self.embedding_model.encode(query)

        # Updated to use the new hybrid search which requires query text
        results = self.vector_store.search(query, query_embedding, user_id, top_k)

        return results

    def answer(self, query: str, user_id: int):

        retrieved_context = self.retrieve(query, user_id)

        # Self-Correction Step: Grade documents for relevance
        relevant_context = []
        for chunk in retrieved_context:
            is_relevant = self.grader.grade(query, chunk["text"])
            if is_relevant:
                relevant_context.append(chunk)

        # If no relevant chunks are found, we might want to acknowledge that
        if not relevant_context:
            return {
                "answer": "I found some documents, but none of them seem relevant to your specific question. Could you please provide more details or ask about something else?",
                "context": []
            }

        # Clean chunks for JSON serialization (remove numpy embeddings)
        clean_context = []
        for chunk in relevant_context:
            clean_context.append({
                "text": chunk["text"],
                "metadata": chunk["metadata"]
            })

        answer = self.generator.generate(query, relevant_context)

        return {
            "answer": answer,
            "context": clean_context
        }