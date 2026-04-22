import sys
from pathlib import Path

# Asegurar que el root del proyecto esté en sys.path para poder importar el paquete `backend`
repo_root = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_root))

from fastapi.testclient import TestClient

from backend.app.core.auth import create_access_token
from backend.app.core.config import settings
from backend.app.main import app


def run():
    client = TestClient(app)

    token = create_access_token(
        {"sub": settings.DEMO_USERNAME, "roles": settings.demo_roles_list}
    )
    headers = {"Authorization": f"Bearer {token}"}

    print("POST /api/auditoria/ -> creating record")
    res = client.post(
        "/api/auditoria/",
        json={"usuario_id": 1, "accion": "TEST_CREAR", "detalle": "Prueba local"},
        headers=headers,
    )
    print(res.status_code, res.text)

    print("GET /api/auditoria/ -> list recent")
    res2 = client.get("/api/auditoria/?limit=5", headers=headers)
    print(res2.status_code, res2.text)


if __name__ == "__main__":
    run()
