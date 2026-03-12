import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.ingestion.pdf_loader import load_pdf

documents = load_pdf("data/raw/sample.pdf")

print(f"Loaded {len(documents)} pages")
print(documents[0])