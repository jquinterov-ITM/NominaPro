from decimal import Decimal
from typing import List

from ..db.models import (Empleado, EstadoNomina, Novedad, ParametrosLegales,
                         TipoNovedad, TipoSalario)
from ..schemas import NominaBase


def calcular_nomina_para_empleado(
    emp: Empleado, novedades_mes: List[Novedad], param: ParametrosLegales, periodo: str
) -> NominaBase:
    """Servicio desacoplado para liquidación R01-R14 (extraído de api/nominas.py).
    Maneja reglas salario integral, IBC, aportes, FSP, transporte.
    """
    # Suma novedades
    sum_horas_extras = sum(
        (n.valor for n in novedades_mes if n.tipo == TipoNovedad.HORA_EXTRA),
        Decimal("0"),
    )
    sum_bonificaciones = sum(
        (n.valor for n in novedades_mes if n.tipo == TipoNovedad.BONIFICACION),
        Decimal("0"),
    )
    sum_descuentos = sum(
        (n.valor for n in novedades_mes if n.tipo == TipoNovedad.DESCUENTO),
        Decimal("0"),
    )
    sum_incapacidades = sum(
        (n.valor for n in novedades_mes if n.tipo == TipoNovedad.INCAPACIDAD),
        Decimal("0"),
    )

    valor_hora = emp.salario_base / param.horas_mes
    valor_dia = emp.salario_base / param.dias_mes
    devengado_horas_extras = sum_horas_extras * valor_hora * param.porcentaje_hora_extra
    deduccion_incapacidades = sum_incapacidades * valor_dia

    # Cálculo IBC
    ibc = emp.salario_base
    if emp.tipo_salario == TipoSalario.INTEGRAL:
        ibc = emp.salario_base * param.factor_salario_integral
    ibc = max(param.smmlv, min(ibc, param.smmlv * param.tope_ibc_smmlv))

    # Deducciones ley
    salud_emp = ibc * param.porcentaje_salud_empleado
    pension_emp = ibc * param.porcentaje_pension_empleado
    deducciones_ley = salud_emp + pension_emp

    # FSP
    fsp = (
        ibc * param.porcentaje_fsp
        if ibc >= param.smmlv * param.umbral_fsp_smmlv
        else Decimal("0")
    )
    deducciones_ley += fsp

    # Auxilio transporte
    aux_trans = Decimal("0")
    if (
        emp.tipo_salario == TipoSalario.ORDINARIO
        and emp.salario_base < param.smmlv * param.umbral_transporte_smmlv
    ):
        aux_trans = param.auxilio_transporte

    # Provisiones del empleador para ordinarios
    provision_prima = Decimal("0")
    provision_cesantias = Decimal("0")
    provision_intereses_cesantias = Decimal("0")
    provision_vacaciones = Decimal("0")
    if emp.tipo_salario == TipoSalario.ORDINARIO:
        provision_prima = emp.salario_base * param.porcentaje_provision_prima
        provision_cesantias = emp.salario_base * param.porcentaje_provision_cesantias
        provision_intereses_cesantias = (
            emp.salario_base * param.porcentaje_provision_intereses_cesantias
        )
        provision_vacaciones = emp.salario_base * param.porcentaje_provision_vacaciones

    total_provisiones = (
        provision_prima
        + provision_cesantias
        + provision_intereses_cesantias
        + provision_vacaciones
    )

    # Totales
    total_devengado = (
        emp.salario_base + aux_trans + sum_bonificaciones + devengado_horas_extras
    )
    total_deducido = deducciones_ley + sum_descuentos + deduccion_incapacidades
    neto_pagar = total_devengado - total_deducido

    return NominaBase(
        periodo=periodo,
        empleado_id=emp.id,
        total_devengado=total_devengado,
        total_deducido=total_deducido,
        neto_pagar=neto_pagar,
        provision_prima=provision_prima,
        provision_cesantias=provision_cesantias,
        provision_intereses_cesantias=provision_intereses_cesantias,
        provision_vacaciones=provision_vacaciones,
        total_provisiones=total_provisiones,
        estado=EstadoNomina.LIQUIDADA,
    )


def liquidar_todos_empleados(
    empleados: List[Empleado],
    novedades_por_empleado: dict[int, List[Novedad]],
    params: ParametrosLegales,
    periodo: str,
) -> List[NominaBase]:
    """Orquesta liquidación masiva."""
    nominas = []
    for emp in empleados:
        novedades = novedades_por_empleado.get(emp.id, [])
        nomina = calcular_nomina_para_empleado(emp, novedades, params, periodo)
        nominas.append(nomina)
    return nominas
