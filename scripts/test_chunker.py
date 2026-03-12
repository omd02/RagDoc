import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunker import chunk_documents

documents = load_pdf("data/raw/sample.pdf")

chunks = chunk_documents(documents)

print(f"Created {len(chunks)} chunks")

print("\nExample chunk:\n")
print(chunks[0])