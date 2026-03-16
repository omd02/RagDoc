from fastapi import FastAPI, UploadFile, File, Depends
from pathlib import Path
import shutil
from src.auth.models import UserRegister, UserLogin
from src.auth.auth import hash_password, verify_password, create_access_token
from src.auth.dependencies import get_current_user
from src.database.db import Database
from src.rag.pipeline import RAGPipeline
from src.database.db import Database

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later we can restrict this
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
        return {"error": "User already exists"}

    password_hash = hash_password(user.password)

    user_id = db.create_user(user.email, password_hash)

    return {"message": "User created", "user_id": user_id}

@app.post("/login")
def login(user: UserLogin):

    db_user = db.get_user_by_email(user.email)

    if not db_user:
        return {"error": "Invalid credentials"}

    user_id = db_user[0]
    password_hash = db_user[2]

    if not verify_password(user.password, password_hash):
        return {"error": "Invalid credentials"}

    token = create_access_token(user_id)

    return {"access_token": token}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pipeline.index_document(file_path)

    return {"message": f"{file.filename} indexed successfully"}



@app.post("/query")
def query_documents(
    query: str,
    user_id: int = Depends(get_current_user)
):

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