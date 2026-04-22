from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .db.models import EstadoNomina, TipoNovedad, TipoSalario


class ParametrosLegalesBase(BaseModel):
    anio: int
    smmlv: Decimal = Field(..., description="Salario Mínimo Mensual Legal Vigente")
    auxilio_transporte: Decimal = Field(
        ..., description="Monto del auxilio de transporte"
    )
    horas_mes: Decimal = Field(
        default=Decimal("240"), description="Horas nominales al mes"
    )
    dias_mes: Decimal = Field(
        default=Decimal("30"), description="Días nominales al mes"
    )
    porcentaje_hora_extra: Decimal = Field(
        default=Decimal("1.25"), description="Factor recargo extra"
    )
    factor_salario_integral: Decimal = Field(
        default=Decimal("0.70"), description="Factor prestacional integral"
    )
    tope_ibc_smmlv: int = Field(default=25, description="Tope máximo de IBC en SMMLV")
    porcentaje_salud_empleado: Decimal = Field(
        default=Decimal("0.04"), description="% Salud empleado"
    )
    porcentaje_pension_empleado: Decimal = Field(
        default=Decimal("0.04"), description="% Pensión empleado"
    )
    porcentaje_fsp: Decimal = Field(
        default=Decimal("0.01"), description="% Fondo Solidaridad Pensional"
    )
    umbral_fsp_smmlv: int = Field(
        default=4, description="Umbral SMMLV para cobro de FSP"
    )
    umbral_transporte_smmlv: int = Field(
        default=2, description="Umbral SMMLV para auxilio transporte"
    )
    porcentaje_provision_prima: Decimal = Field(
        default=Decimal("0.0833"), description="% Provisión Prima"
    )
    porcentaje_provision_cesantias: Decimal = Field(
        default=Decimal("0.0833"), description="% Provisión Cesantías"
    )
    porcentaje_provision_intereses_cesantias: Decimal = Field(
        default=Decimal("0.01"), description="% Provisión Intereses"
    )
    porcentaje_provision_vacaciones: Decimal = Field(
        default=Decimal("0.0417"), description="% Provisión Vacaciones"
    )


class ParametrosLegalesCreate(ParametrosLegalesBase):
    pass


class ParametrosLegalesResponse(ParametrosLegalesBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EmpleadoBase(BaseModel):
    nombre: str = Field(..., description="Nombre del empleado")
    documento: str = Field(..., description="Documento de identidad", max_length=50)
    salario_base: Decimal = Field(
        ..., gt=0, description="Salario numérico bruto del empleado"
    )
    tipo_salario: TipoSalario = Field(
        default=TipoSalario.ORDINARIO, description="Modalidad de salario según la ley"
    )


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoResponse(EmpleadoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class NovedadBase(BaseModel):
    empleado_id: int
    periodo: str = Field(..., description="Formato YYYY-MM")
    tipo: TipoNovedad
    valor: Decimal


class NovedadCreate(NovedadBase):
    pass


class NovedadResponse(NovedadBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class NominaBase(BaseModel):
    periodo: str
    empleado_id: int
    total_devengado: Decimal
    total_deducido: Decimal
    neto_pagar: Decimal
    provision_prima: Decimal = Decimal("0")
    provision_cesantias: Decimal = Decimal("0")
    provision_intereses_cesantias: Decimal = Decimal("0")
    provision_vacaciones: Decimal = Decimal("0")
    total_provisiones: Decimal = Decimal("0")
    estado: EstadoNomina


class NominaResponse(NominaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class NominaLiquidar(BaseModel):
    periodo: str = Field(..., description="Mes a liquidar en formato YYYY-MM")


class AuditoriaBase(BaseModel):
    usuario_id: int = Field(..., description="ID del usuario que ejecuta la acción")
    accion: str = Field(..., description="Acción registrada, p.ej. 'CREAR_EMPLEADO'")
    detalle: Optional[str] = Field(
        None, description="Detalle libre o JSON con contexto"
    )


class AuditoriaCreate(AuditoriaBase):
    pass


class AuditoriaResponse(AuditoriaBase):
    id: int
    fecha: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
