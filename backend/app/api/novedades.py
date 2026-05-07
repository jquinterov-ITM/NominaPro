from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..core.auth import require_roles
from ..db.models import Empleado, Novedad
from ..db.session import get_db
from ..schemas import NovedadCreate, NovedadResponse, PaginatedResponse

router = APIRouter(prefix="/novedades", tags=["novedades"])


@router.get("/", response_model=PaginatedResponse[NovedadResponse])
def listar_novedades(
    page: int = 1,
    limit: int = 20,
    empleado_id: Optional[int] = Query(None, description="Filtra por empleado_id"),
    periodo: Optional[str] = Query(None, description="Filtra por periodo YYYY-MM"),
    db: Session = Depends(get_db),
):
    """Retorna historial de novedades, opcionalmente filtrado por empleado y/o periodo"""
    q = db.query(Novedad)
    if empleado_id is not None:
        q = q.filter(Novedad.empleado_id == empleado_id)
    if periodo:
        q = q.filter(Novedad.periodo == periodo)

    total = q.count()
    total_pages = (total + limit - 1) // limit
    offset = (page - 1) * limit

    novedades = q.order_by(Novedad.id.desc()).offset(offset).limit(limit).all()

    return PaginatedResponse(
        items=novedades,
        total=total,
        page=page,
        limit=limit,
        total_pages=total_pages,
    )


@router.get("/{novedad_id}", response_model=NovedadResponse)
def obtener_novedad(novedad_id: int, db: Session = Depends(get_db)):
    novedad = db.query(Novedad).filter(Novedad.id == novedad_id).first()
    if not novedad:
        raise HTTPException(status_code=404, detail="Novedad no encontrada.")
    return novedad


@router.post("/", response_model=NovedadResponse, status_code=status.HTTP_201_CREATED)
def crear_novedad(
    novedad: NovedadCreate,
    current_user: dict = Depends(require_roles("RH_ADMIN")),
    db: Session = Depends(get_db),
):
    """
    Registra o actualiza una novedad validando que el empleado exista.
    """
    emp = db.query(Empleado).filter(Empleado.id == novedad.empleado_id).first()
    if not emp:
        raise HTTPException(status_code=400, detail="Empleado no encontrado")

    db_novedad = (
        db.query(Novedad)
        .filter(
            Novedad.empleado_id == novedad.empleado_id,
            Novedad.periodo == novedad.periodo,
        )
        .first()
    )

    if db_novedad:
        db_novedad.tipo = novedad.tipo
        db_novedad.valor = novedad.valor
    else:
        db_novedad = Novedad(**novedad.model_dump())
        db.add(db_novedad)

    db.commit()
    db.refresh(db_novedad)
    return db_novedad


@router.delete("/{novedad_id}", status_code=status.HTTP_200_OK)
def eliminar_novedad(
    novedad_id: int,
    current_user: dict = Depends(require_roles("RH_ADMIN")),
    db: Session = Depends(get_db),
):
    novedad = db.query(Novedad).filter(Novedad.id == novedad_id).first()
    if not novedad:
        raise HTTPException(status_code=404, detail="Novedad no encontrada.")

    db.delete(novedad)
    db.commit()
    return {"message": "Novedad eliminada correctamente."}
