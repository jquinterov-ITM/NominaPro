import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest  # noqa: E402

from backend.app.core.config import settings  # noqa: E402
from backend.app.db.session import SessionLocal  # noqa: E402
from backend.app.repositories.usuario_repository import UsuarioRepository  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def crear_usuario_admin():
    """Crea el usuario admin en BD antes de los tests."""
    db = SessionLocal()
    try:
        repo = UsuarioRepository(db)
        repo.seed_admin_if_not_exists(
            username=settings.DEMO_USERNAME,
            password=settings.DEMO_PASSWORD,
            roles="RH_ADMIN,PAYROLL_USER",
        )
    finally:
        db.close()


def pytest_sessionfinish(session, exitstatus):
    """Dispose the SQLAlchemy engine at session end to close sqlite connections."""
    try:
        from importlib import import_module

        db_session = import_module("backend.app.db.session")
        db_session.engine.dispose()
    except Exception:
        pass
