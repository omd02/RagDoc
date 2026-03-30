import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.rag.pipeline import RAGPipeline

# Initialize pipeline
pipeline = RAGPipeline()

# Define test variables
test_pdf = "data/raw/sample.pdf"
test_user_id = 1

# Index document if it doesn't already exist in memory (or just index it for testing)
if os.path.exists(test_pdf):
    print(f"Indexing {test_pdf} for user {test_user_id}...")
    pipeline.index_document(test_pdf, test_user_id)
else:
    print(f"Warning: {test_pdf} not found. Skipping indexing.")

# Query the pipeline
query = "What is machine learning?"
print(f"Querying: {query}")

try:
    result = pipeline.answer(query, test_user_id)

    print("\n--- Answer ---\n")
    print(result["answer"])

    print("\n--- Retrieved Chunks ---\n")
    for r in result["context"]:
        print(f"Source: {r['metadata']['source']} (Page {r['metadata']['page']})")
        print(f"Text: {r['text'][:200]}...")
        print("-" * 20)

except Exception as e:
    print(f"Error: {e}")
    if "GROQ_API_KEY" in str(e):
        print("\nNote: Please make sure GROQ_API_KEY is set in your .env file.")
