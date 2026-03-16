import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.database.db import Database


db = Database()

docs = db.list_documents()

print("\nDocuments in database:\n")

for d in docs:
    print(d)