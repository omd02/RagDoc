import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.rag.pipeline import RAGPipeline

async def main():
    # 1. Initialize RAG Pipeline
    print("Initializing RAG Pipeline...")
    pipeline = RAGPipeline()
    
    # Ensure some data is indexed for the test user
    test_user_id = 1
    sample_pdf = "data/raw/sample.pdf"
    if os.path.exists(sample_pdf) and not pipeline.vector_store.chunks:
        print(f"Indexing {sample_pdf}...")
        pipeline.index_document(sample_pdf, test_user_id)

    # 2. Define Evaluation Dataset
    # In a real scenario, you'd have more questions and ground truths
    eval_questions = [
        "What is the main topic of the document?",
        "Can you summarize the key findings?",
        "What are the specific recommendations mentioned?"
    ]
    
    # Ground truths (you would normally curate these)
    # For this demo, we'll use placeholders or simple expectations
    ground_truths = [
        ["The main topic is machine learning and its applications."],
        ["The key findings include the efficiency of neural networks in pattern recognition."],
        ["The document recommends further research into unsupervised learning."]
    ]

    print(f"Running pipeline on {len(eval_questions)} questions...")
    
    data = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }

    for i, query in enumerate(eval_questions):
        print(f"Processing query {i+1}/{len(eval_questions)}: {query}")
        result = pipeline.answer(query, test_user_id)
        
        data["question"].append(query)
        data["answer"].append(result["answer"])
        data["contexts"].append([c["text"] for c in result["context"]])
        data["ground_truth"].append(ground_truths[i][0])

    dataset = Dataset.from_dict(data)

    # 3. Configure RAGAS to use Groq and local embeddings
    eval_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )
    eval_embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    # 4. Run Evaluation
    print("\nRunning RAGAS Evaluation...")
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
        llm=eval_llm,
        embeddings=eval_embeddings,
        raise_exceptions=False
    )

    print("\n" + "="*30)
    print("RAGAS EVALUATION RESULTS")
    print("="*30)
    print(result)
    
    # Export to pandas for a nice table view
    df = result.to_pandas()
    print("\nDetailed Scores:")
    # Printing only available metric columns
    metric_cols = [col for col in df.columns if col in ['question', 'faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']]
    print(df[metric_cols].to_string())

if __name__ == "__main__":
    asyncio.run(main())
