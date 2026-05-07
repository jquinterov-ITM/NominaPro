from datetime import timedelta

from fastapi.testclient import TestClient

from backend.app.core.auth import create_access_token
from backend.app.db.session import Base, engine
from backend.app.main import app

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def test_protected_employee_creation_requires_rh_admin_role():
    token = create_access_token(
        {"sub": "admin", "roles": []}, expires_delta=timedelta(minutes=5)
    )
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nombre": "Prueba Seguridad",
        "documento": "9999999999",
        "salario_base": "2000000",
        "tipo_salario": "ORDINARIO",
    }

    response = client.post("/api/empleados/", json=payload, headers=headers)

    assert response.status_code == 403
    assert response.json()["message"] == "No tienes permisos para ejecutar esta acción."
