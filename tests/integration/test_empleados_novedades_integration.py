from decimal import Decimal
from uuid import uuid4

from fastapi.testclient import TestClient

from backend.app.db.models import (Novedad, ParametrosLegales, TipoNovedad,
                                   TipoSalario)
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


def _ensure_parametros(anio: int = 2026):
    with SessionLocal() as db:
        parametro = (
            db.query(ParametrosLegales).filter(ParametrosLegales.anio == anio).first()
        )
        if parametro is None:
            parametro = ParametrosLegales(
                anio=anio,
                smmlv=Decimal("1300000"),
                auxilio_transporte=Decimal("162000"),
            )
            db.add(parametro)
            db.commit()
            db.refresh(parametro)


def _create_employee(headers, documento: str, salario_base: str = "1500000"):
    response = client.post(
        "/api/empleados/",
        json={
            "nombre": "Empleado Novedad",
            "documento": documento,
            "salario_base": salario_base,
            "tipo_salario": TipoSalario.ORDINARIO.value,
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    return response.json()


def _delete_employee(employee_id: int, headers):
    response = client.delete(f"/api/empleados/{employee_id}", headers=headers)
    assert response.status_code == 200, response.text


def test_crear_empleado_rechaza_salario_integral_bajo_minimo():
    _ensure_parametros(2026)
    headers = _admin_headers()
    response = client.post(
        "/api/empleados/",
        json={
            "nombre": "Integral Inválido",
            "documento": str(uuid4().int)[:10],
            "salario_base": "16000000",
            "tipo_salario": TipoSalario.INTEGRAL.value,
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert "13 SMMLV" in response.json()["message"]


def test_crear_novedad_sobre_mismo_periodo_actualiza_el_registro():
    headers = _admin_headers()
    employee = _create_employee(headers, documento=str(uuid4().int)[:10])

    try:
        first = client.post(
            "/api/novedades/",
            json={
                "empleado_id": employee["id"],
                "periodo": "2030-02",
                "tipo": TipoNovedad.BONIFICACION.value,
                "valor": "50000",
            },
            headers=headers,
        )
        assert first.status_code == 201, first.text
        assert first.json()["valor"] == "50000.00"

        second = client.post(
            "/api/novedades/",
            json={
                "empleado_id": employee["id"],
                "periodo": "2030-02",
                "tipo": TipoNovedad.DESCUENTO.value,
                "valor": "25000",
            },
            headers=headers,
        )
        assert second.status_code == 201, second.text
        assert second.json()["tipo"] == TipoNovedad.DESCUENTO.value
        assert second.json()["valor"] == "25000.00"

        with SessionLocal() as db:
            novedades = (
                db.query(Novedad)
                .filter(
                    Novedad.empleado_id == employee["id"], Novedad.periodo == "2030-02"
                )
                .all()
            )
            assert len(novedades) == 1
            assert novedades[0].tipo == TipoNovedad.DESCUENTO
    finally:
        _delete_employee(employee["id"], headers)


def test_crear_novedad_rechaza_empleado_inexistente():
    headers = _admin_headers()
    response = client.post(
        "/api/novedades/",
        json={
            "empleado_id": 999999,
            "periodo": "2030-03",
            "tipo": TipoNovedad.HORA_EXTRA.value,
            "valor": "10000",
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Empleado no encontrado"
