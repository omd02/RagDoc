import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_path="storage/app.db"):

        Path("storage").mkdir(exist_ok=True)

        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        self.create_tables()

    def create_tables(self):

        cursor = self.conn.cursor()

        # USERS TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT
        )
        """)

        # DOCUMENTS TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT,
            path TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    # ---------- USER METHODS ----------

    def create_user(self, email, password_hash):

        cursor = self.conn.cursor()

        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )

        self.conn.commit()

        return cursor.lastrowid

    def get_user_by_email(self, email):

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        return cursor.fetchone()

    # ---------- DOCUMENT METHODS ----------

    def add_document(self, user_id, filename, path):

        cursor = self.conn.cursor()

        cursor.execute(
            "INSERT INTO documents (user_id, filename, path) VALUES (?, ?, ?)",
            (user_id, filename, path)
        )

        self.conn.commit()

        return cursor.lastrowid

    def get_documents(self, user_id):

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT * FROM documents WHERE user_id=?",
            (user_id,)
        )

        return cursor.fetchall()

    def delete_document(self, doc_id):

        cursor = self.conn.cursor()

        cursor.execute(
            "DELETE FROM documents WHERE id=?",
            (doc_id,)
        )

        self.conn.commit()