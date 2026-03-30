from src.auth.auth import hash_password, verify_password, create_access_token
from src.database.db import Database
import os

def test_auth():
    db = Database("storage/test.db")
    email = "test@example.com"
    password = "password123"
    
    print(f"Testing registration for {email}...")
    try:
        pw_hash = hash_password(password)
        user_id = db.create_user(email, pw_hash)
        print(f"User created with ID: {user_id}")
    except Exception as e:
        print(f"Registration failed: {e}")
        return

    print("Testing login...")
    try:
        user = db.get_user_by_email(email)
        if user and verify_password(password, user[2]):
            print("Login successful!")
            token = create_access_token(user[0])
            print(f"Token generated: {token[:20]}...")
        else:
            print("Login failed: Invalid credentials or user not found.")
    except Exception as e:
        print(f"Login error: {e}")

    # Cleanup
    if os.path.exists("storage/test.db"):
        os.remove("storage/test.db")

if __name__ == "__main__":
    test_auth()
