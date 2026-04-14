from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.auth import create_access_token
from backend.app.core.config import settings


def get_token():
    return create_access_token({"sub": settings.DEMO_USERNAME, "roles": settings.demo_roles_list})


def test_auditoria_api_post_and_get():
    client = TestClient(app)
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Create an audit record
    res = client.post(
        "/api/auditoria/",
        json={"usuario_id": 7, "accion": "INTEGRATION_TEST", "detalle": "detalle int"},
        headers=headers,
    )
    assert res.status_code == 201
    body = res.json()
    assert body["accion"] == "INTEGRATION_TEST"

    # List recent and ensure our record is present
    res2 = client.get("/api/auditoria/?limit=10", headers=headers)
    assert res2.status_code == 200
    data = res2.json()
    assert any(item["accion"] == "INTEGRATION_TEST" for item in data)
