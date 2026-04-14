from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.db.session import Base
from backend.app.repositories.auditoria_repository import AuditoriaRepository


def test_auditoria_repository_create_and_list():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        repo = AuditoriaRepository(db)
        rec = repo.create(usuario_id=42, accion="UNIT_TEST", detalle="detalle unit")

        assert rec.id == 1
        assert rec.usuario_id == 42
        assert rec.accion == "UNIT_TEST"

        items = repo.list_recent(limit=10)
        assert len(items) == 1
        assert items[0].accion == "UNIT_TEST"
    finally:
        db.close()
        engine.dispose()
