import enum

from sqlalchemy import (Column, DateTime, Enum, Integer, Numeric, String, Text,
                        UniqueConstraint, func)

from .session import Base


# --- ENUMS PARA REGLAS DE NEGOCIO ---
class TipoSalario(str, enum.Enum):
    ORDINARIO = "ORDINARIO"
    INTEGRAL = "INTEGRAL"


class EstadoNomina(str, enum.Enum):
    BORRADOR = "BORRADOR"
    LIQUIDADA = "LIQUIDADA"
    CERRADA_DIAN = "CERRADA_DIAN"


# --- MODELOS DE DATOS ---


class ParametrosLegales(Base):
    """
    R12: Tabla de parámetros por vigencia (Dominio 2026).
    Se usa para calcular el SMMLV actual y topes (ej. para validar >= 13 SMMLV integral).
    """

    __tablename__ = "parametros_legales"

    id = Column(Integer, primary_key=True, index=True)
    anio = Column(Integer, unique=True, index=True, nullable=False)
    smmlv = Column(Numeric(12, 2), nullable=False)
    auxilio_transporte = Column(Numeric(12, 2), nullable=False, default=0)

    # Nuevos campos para centralizar constantes (R12 avanzado)
    horas_mes = Column(Numeric(5, 2), nullable=False, default=240)
    dias_mes = Column(Numeric(5, 2), nullable=False, default=30)
    porcentaje_hora_extra = Column(Numeric(5, 4), nullable=False, default=1.25)
    factor_salario_integral = Column(Numeric(5, 4), nullable=False, default=0.70)
    tope_ibc_smmlv = Column(Integer, nullable=False, default=25)
    porcentaje_salud_empleado = Column(Numeric(5, 4), nullable=False, default=0.04)
    porcentaje_pension_empleado = Column(Numeric(5, 4), nullable=False, default=0.04)
    porcentaje_fsp = Column(Numeric(5, 4), nullable=False, default=0.01)
    umbral_fsp_smmlv = Column(Integer, nullable=False, default=4)
    umbral_transporte_smmlv = Column(Integer, nullable=False, default=2)
    porcentaje_provision_prima = Column(Numeric(6, 5), nullable=False, default=0.0833)
    porcentaje_provision_cesantias = Column(
        Numeric(6, 5), nullable=False, default=0.0833
    )
    porcentaje_provision_intereses_cesantias = Column(
        Numeric(6, 5), nullable=False, default=0.01
    )
    porcentaje_provision_vacaciones = Column(
        Numeric(6, 5), nullable=False, default=0.0417
    )


class Empleado(Base):
    """
    R01: Diferenciar Salario Ordinario vs Integral (Fase 1).
    """

    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    documento = Column(String, unique=True, index=True, nullable=False)
    salario_base = Column(Numeric(12, 2), nullable=False)
    tipo_salario = Column(
        Enum(TipoSalario), nullable=False, default=TipoSalario.ORDINARIO
    )


class Auditoria(Base):
    """
    R10: Trazabilidad y Cumplimiento UGPP
    Rastrea quién modificó qué, cómo estaba antes y cómo quedó.
    """

    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)  # ID del admin (Fase 2 de JWT)
    accion = Column(String, nullable=False)  # Ej: 'CREAR_EMPLEADO', 'EDITAR_SALARIO'


class TipoNovedad(str, enum.Enum):
    HORA_EXTRA = "HORA_EXTRA"
    INCAPACIDAD = "INCAPACIDAD"
    DESCUENTO = "DESCUENTO"
    BONIFICACION = "BONIFICACION"


class Novedad(Base):
    __tablename__ = "novedades"
    __table_args__ = (
        UniqueConstraint(
            "empleado_id", "periodo", name="uq_novedades_empleado_periodo"
        ),
    )
    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(Integer, index=True, nullable=False)
    periodo = Column(String, index=True, nullable=False)  # YYYY-MM
    tipo = Column(Enum(TipoNovedad), nullable=False)
    valor = Column(Numeric(12, 2), nullable=False)


class Nomina(Base):
    __tablename__ = "nominas"
    __table_args__ = (
        UniqueConstraint("empleado_id", "periodo", name="uq_nominas_empleado_periodo"),
    )
    id = Column(Integer, primary_key=True, index=True)
    periodo = Column(String, index=True, nullable=False)  # YYYY-MM
    empleado_id = Column(Integer, index=True, nullable=False)
    total_devengado = Column(Numeric(12, 2), nullable=False)
    total_deducido = Column(Numeric(12, 2), nullable=False)
    neto_pagar = Column(Numeric(12, 2), nullable=False)
    provision_prima = Column(Numeric(12, 2), nullable=False, default=0)
    provision_cesantias = Column(Numeric(12, 2), nullable=False, default=0)
    provision_intereses_cesantias = Column(Numeric(12, 2), nullable=False, default=0)
    provision_vacaciones = Column(Numeric(12, 2), nullable=False, default=0)
    total_provisiones = Column(Numeric(12, 2), nullable=False, default=0)
    estado = Column(Enum(EstadoNomina), nullable=False, default=EstadoNomina.BORRADOR)
    valor_anterior = Column(Text, nullable=True)  # JSON con el estado previo
    valor_nuevo = Column(Text, nullable=True)  # JSON con el estado nuevo
    fecha = Column(DateTime(timezone=True), server_default=func.now())
