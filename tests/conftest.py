import pytest


def pytest_sessionfinish(session, exitstatus):
    """Dispose the SQLAlchemy engine at session end to close sqlite connections."""
    try:
        from importlib import import_module

        db_session = import_module("backend.app.db.session")
        db_session.engine.dispose()
    except Exception:
        pass
