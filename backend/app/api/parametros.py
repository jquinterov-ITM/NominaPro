from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..db import models
from ..db.session import get_db

router = APIRouter()


@router.post(
    "/",
    response_model=schemas.ParametrosLegalesResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_parametro(
    param_in: schemas.ParametrosLegalesCreate, db: Session = Depends(get_db)
):
    """
    R12: Permite insertar los parámetros legales de un año.
    Necesarios para validaciones de topes e IBC.
    """
    param_db = (
        db.query(models.ParametrosLegales)
        .filter(models.ParametrosLegales.anio == param_in.anio)
        .first()
    )
    if param_db:
        raise HTTPException(
            status_code=400, detail="Los parámetros para este año ya existen."
        )

    nuevo_parametro = models.ParametrosLegales(**param_in.model_dump())
    db.add(nuevo_parametro)
    db.commit()
    db.refresh(nuevo_parametro)
    return nuevo_parametro


@router.get("/", response_model=list[schemas.ParametrosLegalesResponse])
def listar_parametros(db: Session = Depends(get_db)):
    return db.query(models.ParametrosLegales).all()
