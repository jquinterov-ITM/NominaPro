import os
import sys

sys.path.insert(0, os.getcwd())
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)
resp = client.post("/api/nominas/liquidar", json={"periodo": "2026-01"})
print(resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)
