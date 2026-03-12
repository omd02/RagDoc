import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_documents
from src.retrieval.embeddings import EmbeddingModel

documents = load_pdf("data/raw/sample.pdf")

chunks = chunk_documents(documents)

model = EmbeddingModel()

embedded_chunks = model.embed_documents(chunks)

print(f"Generated embeddings for {len(embedded_chunks)} chunks")

print(len(embedded_chunks[0]["embedding"]))