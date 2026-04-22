from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..core.auth import require_roles
from ..db import models
from ..db.session import get_db

router = APIRouter()


@router.post(
    "/", response_model=schemas.EmpleadoResponse, status_code=status.HTTP_201_CREATED
)
def crear_empleado(
    empleado_in: schemas.EmpleadoCreate,
    current_user: dict = Depends(require_roles("RH_ADMIN")),
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo empleado en el sistema y ejecuta validaciones del Dominio 2026.
    """
    # 1. Validar que el documento no exista
    empleado_existente = (
        db.query(models.Empleado)
        .filter(models.Empleado.documento == empleado_in.documento)
        .first()
    )
    if empleado_existente:
        raise HTTPException(
            status_code=400, detail="Ya existe un empleado con este documento."
        )

    # 2. Regla R01 y R02: Validación Dominio 2026 (Salario Integral estrictamente >= 13 SMMLV)
    if empleado_in.tipo_salario == models.TipoSalario.INTEGRAL:
        # En la vida real, sacarías el año de la fecha de inicio del contrato. Aquí usamos la fecha actual del sistema.
        anio_actual = datetime.now().year
        param_legal = (
            db.query(models.ParametrosLegales)
            .filter(models.ParametrosLegales.anio == anio_actual)
            .first()
        )

        if not param_legal:
            raise HTTPException(
                status_code=400,
                detail=f"Faltan parámetros legales para el año {anio_actual}. Son requeridos para validar si el salario integral cumple con el tope mínimo.",
            )

        # Fórmula estricta: 13 SMMLV
        minimo_integral = param_legal.smmlv * Decimal("13")
        if empleado_in.salario_base < minimo_integral:
            raise HTTPException(
                status_code=400,
                detail=f"REGLA R01: El salario integral no puede ser inferior a 13 SMMLV. El mínimo para {anio_actual} es ${minimo_integral:,.2f} (usted envió ${empleado_in.salario_base:,.2f}).",
            )

    # 3. Guardar en Base de Datos
    nuevo_empleado = models.Empleado(**empleado_in.model_dump())
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)

    # TODO (R10): Aquí iría la inserción en la tabla de Auditoría de creación de recursos
    return nuevo_empleado


@router.get("/", response_model=list[schemas.EmpleadoResponse])
def listar_empleados(db: Session = Depends(get_db)):
    return db.query(models.Empleado).all()


@router.get("/{empleado_id}", response_model=schemas.EmpleadoResponse)
def obtener_empleado(empleado_id: int, db: Session = Depends(get_db)):
    empleado = (
        db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    )
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")
    return empleado


@router.put("/{empleado_id}", response_model=schemas.EmpleadoResponse)
def actualizar_empleado(
    empleado_id: int,
    empleado_in: schemas.EmpleadoCreate,
    current_user: dict = Depends(require_roles("RH_ADMIN")),
    db: Session = Depends(get_db),
):
    """
    Actualiza los datos de un empleado existente.
    Aplica las mismas validaciones de dominio que la creación.
    """
    empleado = (
        db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    )
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")

    # Validar que el documento no esté duplicado en otro empleado
    duplicado = (
        db.query(models.Empleado)
        .filter(
            models.Empleado.documento == empleado_in.documento,
            models.Empleado.id != empleado_id,
        )
        .first()
    )
    if duplicado:
        raise HTTPException(
            status_code=400, detail="Ya existe otro empleado con este documento."
        )

    # Regla R01/R02: Validación Salario Integral >= 13 SMMLV
    if empleado_in.tipo_salario == models.TipoSalario.INTEGRAL:
        anio_actual = datetime.now().year
        param_legal = (
            db.query(models.ParametrosLegales)
            .filter(models.ParametrosLegales.anio == anio_actual)
            .first()
        )
        if not param_legal:
            raise HTTPException(
                status_code=400,
                detail=f"Faltan parámetros legales para el año {anio_actual}.",
            )
        minimo_integral = param_legal.smmlv * Decimal("13")
        if empleado_in.salario_base < minimo_integral:
            raise HTTPException(
                status_code=400,
                detail=f"REGLA R01: El salario integral no puede ser inferior a 13 SMMLV. Mínimo para {anio_actual}: ${minimo_integral:,.2f}.",
            )

    empleado.nombre = empleado_in.nombre
    empleado.documento = empleado_in.documento
    empleado.salario_base = empleado_in.salario_base
    empleado.tipo_salario = empleado_in.tipo_salario
    db.commit()
    db.refresh(empleado)
    return empleado


@router.delete("/{empleado_id}", status_code=status.HTTP_200_OK)
def eliminar_empleado(
    empleado_id: int,
    current_user: dict = Depends(require_roles("RH_ADMIN")),
    db: Session = Depends(get_db),
):
    empleado = (
        db.query(models.Empleado).filter(models.Empleado.id == empleado_id).first()
    )
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado.")

    db.query(models.Novedad).filter(models.Novedad.empleado_id == empleado_id).delete(
        synchronize_session=False
    )
    db.query(models.Nomina).filter(models.Nomina.empleado_id == empleado_id).delete(
        synchronize_session=False
    )
    db.delete(empleado)
    db.commit()

    return {"message": "Empleado eliminado correctamente."}
