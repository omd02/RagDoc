from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil

from src.rag.pipeline import RAGPipeline
from src.database.db import Database


app = FastAPI()

pipeline = RAGPipeline()
db = Database()

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)


@app.get("/")
def home():
    return {"message": "RAG Document QA API running"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pipeline.index_document(file_path)

    return {"message": f"{file.filename} indexed successfully"}


@app.post("/query")
def query_documents(query: str):

    results = pipeline.retrieve(query)

    formatted_results = []

    for r in results:
        formatted_results.append({
            "text": r["text"],
            "source": r["metadata"]["source"],
            "page": r["metadata"]["page"]
        })

    return {"results": formatted_results}


@app.get("/documents")
def list_documents():

    docs = db.list_documents()

    formatted = []

    for d in docs:
        formatted.append({
            "id": d[0],
            "filename": d[1],
            "path": d[2],
            "uploaded": d[3]
        })

    return {"documents": formatted}