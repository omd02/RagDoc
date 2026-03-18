from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from pathlib import Path
import shutil
from src.auth.models import UserRegister, UserLogin
from src.auth.auth import hash_password, verify_password, create_access_token
from src.auth.dependencies import get_current_user
from src.database.db import Database
from src.rag.pipeline import RAGPipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RAGPipeline()
db = Database()

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)


@app.get("/")
def home():
    return {"message": "RAG Document QA API running"}

@app.post("/register")
def register(user: UserRegister):

    existing = db.get_user_by_email(user.email)

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    password_hash = hash_password(user.password)

    user_id = db.create_user(user.email, password_hash)

    return {"message": "User created", "user_id": user_id}

@app.post("/login")
def login(user: UserLogin):

    db_user = db.get_user_by_email(user.email)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = db_user[0]
    password_hash = db_user[2]

    if not verify_password(user.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user_id)

    return {"access_token": token}

@app.post("/upload")
async def upload_document(
    file: UploadFile,
    user_id: int = Depends(get_current_user)
):

    file_path = f"{UPLOAD_DIR}/{user_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc_id = db.add_document(user_id, file.filename, file_path)

    pipeline.index_document(file_path)

    return {
        "message": "Document uploaded",
        "document_id": doc_id
    }



@app.post("/query")
def query_documents(
    query: str,
    user_id: int = Depends(get_current_user)
):

    results = pipeline.retrieve(query)

    return {"results": results}

@app.get("/documents")
def get_documents(user_id: int = Depends(get_current_user)):

    docs = db.get_documents(user_id)

    results = []

    for d in docs:
        results.append({
            "id": d[0],
            "filename": d[2]
        })

    return {"documents": results}

@app.delete("/documents/{doc_id}")
def delete_document(
    doc_id: int,
    user_id: int = Depends(get_current_user)
):

    db.delete_document(doc_id)

    return {"message": "Document deleted"}