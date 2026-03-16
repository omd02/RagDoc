import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_path="storage/documents.db"):

        Path("storage").mkdir(exist_ok=True)

        self.conn = sqlite3.connect(db_path)

        self.create_tables()

    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            path TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def add_document(self, filename, path):

        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO documents (filename, path)
        VALUES (?, ?)
        """, (filename, path))

        self.conn.commit()

        return cursor.lastrowid

    def list_documents(self):

        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM documents")

        return cursor.fetchall()