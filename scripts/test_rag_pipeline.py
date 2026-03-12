import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.rag.pipeline import RAGPipeline


pipeline = RAGPipeline()

pipeline.index_document("data/raw/sample.pdf")

query = "What is machine learning?"

results = pipeline.retrieve(query)

print("\nRetrieved Chunks:\n")

for r in results:
    print(r["metadata"])
    print(r["text"][:200])
    print()