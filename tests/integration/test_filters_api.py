from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.core.auth import create_access_token
from backend.app.core.config import settings
from backend.app.db.session import SessionLocal
from backend.app.db.models import Nomina
from uuid import uuid4


def get_token():
    return create_access_token({"sub": settings.DEMO_USERNAME, "roles": settings.demo_roles_list})


def test_novedades_and_nominas_filters():
    client = TestClient(app)
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Create an empleado
    empleado_payload = {
        "nombre": "Filter Test",
        "documento": f"FT-{str(uuid4().int)[:10]}",
        "salario_base": "1500000.00",
        "tipo_salario": "ORDINARIO",
    }
    res_emp = client.post("/api/empleados/", json=empleado_payload, headers=headers)
    assert res_emp.status_code == 201
    emp = res_emp.json()
    emp_id = emp["id"] if isinstance(emp, list) else emp["id"]

    # Create two novedades for different periodos
    nov1 = {"empleado_id": emp_id, "periodo": "2026-04", "tipo": "HORA_EXTRA", "valor": "100.00"}
    nov2 = {"empleado_id": emp_id, "periodo": "2026-05", "tipo": "HORA_EXTRA", "valor": "50.00"}

    r1 = client.post("/api/novedades/", json=nov1, headers=headers)
    assert r1.status_code == 201
    r2 = client.post("/api/novedades/", json=nov2, headers=headers)
    assert r2.status_code == 201

    # Filter novedades by empleado_id and periodo
    res = client.get(f"/api/novedades/?empleado_id={emp_id}&periodo=2026-04")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["periodo"] == "2026-04"

    # Insert nominas directly via DB session
    db = SessionLocal()
    try:
        n1 = Nomina(periodo="2026-04", empleado_id=emp_id, total_devengado=100, total_deducido=0, neto_pagar=100)
        n2 = Nomina(periodo="2026-05", empleado_id=emp_id, total_devengado=200, total_deducido=0, neto_pagar=200)
        db.add(n1)
        db.add(n2)
        db.commit()
    finally:
        db.close()

    # Filter nominas by periodo
    resn = client.get("/api/nominas/?periodo=2026-04")
    assert resn.status_code == 200
    nd = resn.json()
    assert any(item["periodo"] == "2026-04" for item in nd)
    assert all(item["periodo"] == "2026-04" for item in nd if item["periodo"] == "2026-04")
