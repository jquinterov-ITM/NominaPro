"""Initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-04-22
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Initial migration: create tables from models metadata
    bind = op.get_bind()
    # Import models and create all tables (idempotent for initial setup)
    from backend.app.db.session import Base

    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    from backend.app.db.session import Base

    # Drop all tables created by models (use with caution)
    Base.metadata.drop_all(bind=bind)
