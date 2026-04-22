from fastapi.testclient import TestClient

from backend.app.core.auth import create_access_token
from backend.app.core.config import settings
from backend.app.main import app

client = TestClient(app)


def get_token():
    return create_access_token(
        {"sub": settings.DEMO_USERNAME, "roles": settings.demo_roles_list}
    )


headers = {"Authorization": f"Bearer {get_token()}"}
payload = {
    "nombre": "Filter Test",
    "documento": "FT-12345",
    "salario_base": "1500000.00",
    "tipo_salario": "ORDINARIO",
}
res = client.post("/api/empleados/", json=payload, headers=headers)
print(res.status_code)
try:
    print(res.json())
except Exception as e:
    print("No JSON body", e)
