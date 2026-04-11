from decimal import Decimal
from types import SimpleNamespace

from backend.app.db.models import TipoNovedad, TipoSalario
from backend.app.schemas import NominaBase
from backend.app.services.nomina_service import (calcular_nomina_para_empleado,
                                                 liquidar_todos_empleados)


def make_emp(salario_base: Decimal, tipo_salario, emp_id: int = 1):
    return SimpleNamespace(
        id=emp_id, salario_base=salario_base, tipo_salario=tipo_salario
    )


def make_novedad(tipo, valor):
    return SimpleNamespace(tipo=tipo, valor=valor)


def test_calcular_nomina_ordinario_incluye_auxilio_y_provisiones():
    emp = make_emp(Decimal("1500000"), tipo_salario=TipoSalario.ORDINARIO)
    params = SimpleNamespace(
        smmlv=Decimal("1300000"),
        auxilio_transporte=Decimal("162000"),
        horas_mes=Decimal("240"),
        dias_mes=Decimal("30"),
        porcentaje_hora_extra=Decimal("1.25"),
        factor_salario_integral=Decimal("0.70"),
        tope_ibc_smmlv=25,
        porcentaje_salud_empleado=Decimal("0.04"),
        porcentaje_pension_empleado=Decimal("0.04"),
        porcentaje_fsp=Decimal("0.01"),
        umbral_fsp_smmlv=4,
        umbral_transporte_smmlv=2,
        porcentaje_provision_prima=Decimal("0.0833"),
        porcentaje_provision_cesantias=Decimal("0.0833"),
        porcentaje_provision_intereses_cesantias=Decimal("0.01"),
        porcentaje_provision_vacaciones=Decimal("0.0417"),
    )

    nomina = calcular_nomina_para_empleado(emp, [], params, "2026-01")

    assert isinstance(nomina, NominaBase)
    assert nomina.periodo == "2026-01"
    assert nomina.empleado_id == 1
    assert nomina.total_devengado == Decimal("1662000")
    assert nomina.total_provisiones > 0
    assert nomina.neto_pagar < nomina.total_devengado


def test_calcular_nomina_integral_aplica_ibc_y_fsp():
    emp = make_emp(Decimal("20000000"), tipo_salario=TipoSalario.INTEGRAL, emp_id=2)
    params = SimpleNamespace(
        smmlv=Decimal("1300000"),
        auxilio_transporte=Decimal("162000"),
        horas_mes=Decimal("240"),
        dias_mes=Decimal("30"),
        porcentaje_hora_extra=Decimal("1.25"),
        factor_salario_integral=Decimal("0.70"),
        tope_ibc_smmlv=25,
        porcentaje_salud_empleado=Decimal("0.04"),
        porcentaje_pension_empleado=Decimal("0.04"),
        porcentaje_fsp=Decimal("0.01"),
        umbral_fsp_smmlv=4,
        umbral_transporte_smmlv=2,
        porcentaje_provision_prima=Decimal("0.0833"),
        porcentaje_provision_cesantias=Decimal("0.0833"),
        porcentaje_provision_intereses_cesantias=Decimal("0.01"),
        porcentaje_provision_vacaciones=Decimal("0.0417"),
    )

    nomina = calcular_nomina_para_empleado(emp, [], params, "2026-01")

    assert nomina.empleado_id == 2
    assert nomina.total_devengado == emp.salario_base
    assert nomina.total_provisiones == 0
    assert nomina.total_deducido > Decimal("0")
    assert nomina.neto_pagar < nomina.total_devengado


def test_liquidar_todos_empleados_usa_novedades_por_empleado():
    empleados = [
        make_emp(Decimal("1500000"), TipoSalario.ORDINARIO, emp_id=1),
        make_emp(Decimal("1500000"), TipoSalario.ORDINARIO, emp_id=2),
    ]
    novedades_por_empleado = {
        1: [make_novedad(TipoNovedad.BONIFICACION, Decimal("50000"))],
        2: [make_novedad(TipoNovedad.DESCUENTO, Decimal("25000"))],
    }
    params = SimpleNamespace(
        smmlv=Decimal("1300000"),
        auxilio_transporte=Decimal("162000"),
        horas_mes=Decimal("240"),
        dias_mes=Decimal("30"),
        porcentaje_hora_extra=Decimal("1.25"),
        factor_salario_integral=Decimal("0.70"),
        tope_ibc_smmlv=25,
        porcentaje_salud_empleado=Decimal("0.04"),
        porcentaje_pension_empleado=Decimal("0.04"),
        porcentaje_fsp=Decimal("0.01"),
        umbral_fsp_smmlv=4,
        umbral_transporte_smmlv=2,
        porcentaje_provision_prima=Decimal("0.0833"),
        porcentaje_provision_cesantias=Decimal("0.0833"),
        porcentaje_provision_intereses_cesantias=Decimal("0.01"),
        porcentaje_provision_vacaciones=Decimal("0.0417"),
    )

    nominas = liquidar_todos_empleados(
        empleados, novedades_por_empleado, params, "2026-02"
    )

    assert len(nominas) == 2
    assert nominas[0].empleado_id == 1
    assert nominas[1].empleado_id == 2
    assert nominas[0].total_devengado > nominas[1].total_devengado
