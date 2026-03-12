import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_documents
from src.retrieval.embeddings import EmbeddingModel
from src.retrieval.vector_store import VectorStore


documents = load_pdf("data/raw/sample.pdf")

chunks = chunk_documents(documents)

model = EmbeddingModel()

embedded_chunks = model.embed_documents(chunks)

vector_store = VectorStore()

vector_store.add_embeddings(embedded_chunks)

query = "What is machine learning?"

query_embedding = model.model.encode(query)

results = vector_store.search(query_embedding)

print("\nTop results:\n")

for r in results:
    print(r["metadata"])
    print(r["text"][:200])
    print()