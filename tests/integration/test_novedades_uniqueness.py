import uuid

from fastapi.testclient import TestClient

from backend.app.core.auth import create_access_token
from backend.app.db.session import Base, engine
from backend.app.main import app

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def test_novedad_upsert_por_empleado_y_periodo():
    token = create_access_token({"sub": "admin", "roles": ["RH_ADMIN"]})
    headers = {"Authorization": f"Bearer {token}"}
    documento = f"DOC-{uuid.uuid4().hex[:10]}"
    empleado_resp = client.post(
        "/api/empleados/",
        headers=headers,
        json={
            "nombre": "Empleado Prueba",
            "documento": documento,
            "salario_base": "2000000",
            "tipo_salario": "ORDINARIO",
        },
    )
    assert empleado_resp.status_code in (200, 201)
    empleado_id = empleado_resp.json()["id"]

    payload = {
        "empleado_id": empleado_id,
        "periodo": "2026-01",
        "tipo": "HORA_EXTRA",
        "valor": "50000",
    }
    first_resp = client.post("/api/novedades/", json=payload, headers=headers)
    assert first_resp.status_code in (200, 201)
    first_id = first_resp.json()["id"]

    payload["tipo"] = "BONIFICACION"
    payload["valor"] = "75000"
    second_resp = client.post("/api/novedades/", json=payload, headers=headers)
    assert second_resp.status_code in (200, 201)
    second_json = second_resp.json()

    assert second_json["id"] == first_id
    assert second_json["tipo"] == "BONIFICACION"
    assert second_json["valor"] == "75000.00"

    response = client.get("/api/novedades/")
    data = response.json()
    matching = [
        nov
        for nov in data["items"]
        if nov["empleado_id"] == empleado_id and nov["periodo"] == "2026-01"
    ]
    assert len(matching) == 1
