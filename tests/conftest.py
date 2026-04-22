import os
import sys

# Asegura que la raíz del proyecto esté en sys.path para que las importaciones como
# `backend.app` funcionen cuando pytest se ejecuta desde el directorio tests.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import pytest


def pytest_sessionfinish(session, exitstatus):
    """Dispose the SQLAlchemy engine at session end to close sqlite connections."""
    try:
        from importlib import import_module

        db_session = import_module("backend.app.db.session")
        db_session.engine.dispose()
    except Exception:
        pass
