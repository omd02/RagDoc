from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from pathlib import Path
import shutil
from src.auth.models import UserRegister, UserLogin
from src.auth.auth import hash_password, verify_password, create_access_token
from src.auth.dependencies import get_current_user
from src.database.db import Database
from src.rag.pipeline import RAGPipeline
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

# Global instances
db = Database()
# Pipeline loads heavy models, so we still do it here but ensure it's initialized before routes
print("Initializing RAG Pipeline...")
pipeline = RAGPipeline()
print("Initialization complete.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
Path(UPLOAD_DIR).mkdir(exist_ok=True)


@app.get("/")
def home():
    return {"message": "RAG Document QA API running"}

@app.post("/register")
def register(user: UserRegister):
    print(f"Registering user: {user.email}")
    try:
        existing = db.get_user_by_email(user.email)

        if existing:
            print(f"User already exists: {user.email}")
            raise HTTPException(status_code=400, detail="User already exists")

        print(f"Hashing password for {user.email}")
        password_hash = hash_password(user.password)

        print(f"Creating user in database: {user.email}")
        user_id = db.create_user(user.email, password_hash)

        print(f"User created successfully: {user.email}, ID: {user_id}")
        return {"message": "User created", "user_id": user_id}
    except Exception as e:
        print(f"Registration error for {user.email}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
def login(user: UserLogin):
    print(f"Login attempt for: {user.email}")
    try:
        db_user = db.get_user_by_email(user.email)

        if not db_user:
            print(f"Login failed: User {user.email} not found")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = db_user[0]
        password_hash = db_user[2]

        print(f"Verifying password for {user.email}")
        if not verify_password(user.password, password_hash):
            print(f"Login failed: Invalid password for {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        print(f"Creating access token for {user.email}")
        token = create_access_token(user_id)

        print(f"Login successful for {user.email}")
        return {"access_token": token}
    except Exception as e:
        print(f"Login error for {user.email}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(
    file: UploadFile,
    user_id: int = Depends(get_current_user)
):
    print(f"File upload request: {file.filename} for user {user_id}")
    file_path = f"{UPLOAD_DIR}/{user_id}_{file.filename}"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc_id = db.add_document(user_id, file.filename, file_path)
        print(f"Indexing document: {file.filename}")
        pipeline.index_document(file_path, user_id)
        print(f"Indexing complete for: {file.filename}")

        return {
            "message": "Document uploaded",
            "document_id": doc_id
        }
    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_documents(
    query: str,
    user_id: int = Depends(get_current_user)
):
    print(f"Query request: '{query}' for user {user_id}")
    try:
        result = pipeline.answer(query, user_id)
        print(f"Answer generated successfully")
        return result
    except Exception as e:
        print(f"Query error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

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

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)