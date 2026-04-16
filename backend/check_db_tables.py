from pathlib import Path
import sqlite3


db_path = Path(__file__).resolve().parent / "nominapro.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
print(f"DB usada: {db_path}")
print(cur.fetchall())
conn.close()
