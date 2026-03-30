from src.database.db import Database
import sqlite3
import os

def list_users():
    db_path = "storage/app.db"
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password_hash FROM users")
    users = cursor.fetchall()
    
    print(f"Found {len(users)} users:")
    for user in users:
        print(f"ID: {user[0]}, Email: {user[1]}, Hash: {user[2][:30]}...")
    
    conn.close()

if __name__ == "__main__":
    list_users()
