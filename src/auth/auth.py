import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def create_access_token(user_id: int):
    print(f"Generating access token for user_id: {user_id}")
    import time
    start = time.time()
    expire = datetime.utcnow() + timedelta(hours=24)

    payload = {
        "user_id": user_id,
        "exp": int(expire.timestamp())
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token generated in {time.time() - start:.4f}s")
    return token