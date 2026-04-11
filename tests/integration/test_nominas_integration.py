from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.db.models import Nomina, ParametrosLegales, TipoSalario
from backend.app.db.session import Base, SessionLocal, engine
from backend.app.main import app

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def _admin_headers():
    token_resp = client.post(
        "/api/auth/token", data={"username": "admin", "password": "secret"}
    )
    assert token_resp.status_code == 200
    return {"Authorization": f"Bearer {token_resp.json()['access_token']}"}


def _ensure_parametros(anio: int, smmlv: Decimal, auxilio: Decimal):
    with SessionLocal() as db:
        parametro = (
            db.query(ParametrosLegales).filter(ParametrosLegales.anio == anio).first()
        )
        if parametro is None:
            parametro = ParametrosLegales(
                anio=anio,
                smmlv=smmlv,
                auxilio_transporte=auxilio,
            )
            db.add(parametro)
        else:
            parametro.smmlv = smmlv
            parametro.auxilio_transporte = auxilio
        db.commit()
        db.refresh(parametro)


def _create_employee(headers, *, documento: str, salario_base: str, tipo_salario: str):
    response = client.post(
        "/api/empleados/",
        json={
            "nombre": "Empleado Prueba",
            "documento": documento,
            "salario_base": salario_base,
            "tipo_salario": tipo_salario,
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    return response.json()


def _delete_employee(employee_id: int, headers):
    response = client.delete(f"/api/empleados/{employee_id}", headers=headers)
    assert response.status_code == 200, response.text


def _delete_nominas_por_periodo(periodo: str):
    with SessionLocal() as db:
        db.query(Nomina).filter(Nomina.periodo == periodo).delete(
            synchronize_session=False
        )
        db.commit()


def test_liquidar_nomina_crea_registro_y_rechaza_periodo_duplicado():
    headers = _admin_headers()
    periodo = "2099-01"
    _ensure_parametros(2099, Decimal("1400000"), Decimal("175000"))
    employee = _create_employee(
        headers,
        documento=str(uuid4().int)[:10],
        salario_base="1600000",
        tipo_salario=TipoSalario.ORDINARIO.value,
    )

    try:
        first = client.post(
            "/api/nominas/liquidar", json={"periodo": periodo}, headers=headers
        )
        assert first.status_code == 201, first.text
        data = first.json()
        item = next(
            (item for item in data if item["empleado_id"] == employee["id"]), None
        )
        assert item is not None
        assert item["periodo"] == periodo
        assert Decimal(item["total_devengado"]) >= Decimal("1600000")

        second = client.post(
            "/api/nominas/liquidar", json={"periodo": periodo}, headers=headers
        )
        assert second.status_code == 400
        assert "ya liquidado" in second.json()["message"]
    finally:
        _delete_nominas_por_periodo(periodo)
        _delete_employee(employee["id"], headers)
