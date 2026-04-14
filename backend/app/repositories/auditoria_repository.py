from typing import List

from sqlalchemy.orm import Session

from ..db.models import Auditoria


class AuditoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, usuario_id: int, accion: str, detalle: str | None = None) -> Auditoria:
        record = Auditoria(usuario_id=usuario_id, accion=accion, detalle=detalle)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def list_recent(self, limit: int = 50) -> List[Auditoria]:
        return (
            self.db.query(Auditoria).order_by(Auditoria.id.desc()).limit(limit).all()
        )
