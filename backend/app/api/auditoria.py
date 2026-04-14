from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas
from ..core.auth import require_roles
from ..db.session import get_db
from ..repositories.auditoria_repository import AuditoriaRepository

router = APIRouter()


@router.post("/", response_model=schemas.AuditoriaResponse, status_code=status.HTTP_201_CREATED)
def crear_auditoria(
    payload: schemas.AuditoriaCreate,
    current_user: dict = Depends(require_roles("RH_ADMIN")),
    db: Session = Depends(get_db),
):
    repo = AuditoriaRepository(db)
    rec = repo.create(usuario_id=payload.usuario_id, accion=payload.accion, detalle=payload.detalle)
    return rec


@router.get("/", response_model=list[schemas.AuditoriaResponse])
def listar_auditoria(
    limit: int = 50,
    current_user: dict = Depends(require_roles("RH_ADMIN")),
    db: Session = Depends(get_db),
):
    repo = AuditoriaRepository(db)
    return repo.list_recent(limit=limit)
