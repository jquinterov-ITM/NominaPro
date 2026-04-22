# CHANGELOG

All notable changes to this project are documented in this file.

## [Unreleased] - 2026-04-22

### Added
- `.env.example` with recommended environment variables for backend (SECRET_KEY, DATABASE_URL, etc.).
- Basic Alembic setup and initial migration: `backend/alembic/` and `0001_initial_schema`.
- GitHub Actions CI workflow: `.github/workflows/ci.yml` (runs backend tests, frontend tests, and linters).
- Pre-commit configuration: `.pre-commit-config.yaml` (black, isort, ruff).

### Changed
- Moved secrets and demo credentials out of source code into environment-based configuration.
  - `backend/app/core/config.py` now reads from `.env` (uses pydantic settings) and warns if `SECRET_KEY` is missing.
- `backend/app/db/session.py` no longer unconditionally applies ad-hoc SQLite ALTERs when `USE_ALEMBIC=1` is set; added `atexit` engine disposal to avoid unclosed DB connections.
- Replaced naive UTC datetimes with timezone-aware UTC and set JWT `exp` as POSIX timestamp.
  - `backend/app/core/auth.py` now uses `datetime.now(timezone.utc)` and encodes `exp` as `int(timestamp)`.
- Added package markers and test helper for imports: `backend/__init__.py`, `backend/app/__init__.py`, `tests/conftest.py`.

### Fixed
- ResourceWarning: unclosed SQLite connections during tests fixed by disposing SQLAlchemy engine on exit.
- Resolved multiple formatting and import issues by running pre-commit (black/isort/ruff).

### Tests
- Full test suite executed: `pytest` — 12 passed.

### Notes / Next steps
- Consider enforcing stricter CI linter failures (remove temporary `|| true`).
- Replace remaining naive datetimes elsewhere if found and migrate DB to a production-ready RDBMS for deployments.
