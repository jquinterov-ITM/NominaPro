import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Para desarrollo rápido y evitar errores de conexión si no tienes PostgreSQL instalado o activo,
# cambiamos temporalmente a SQLite local.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nominapro.db")

# Forzar el uso del driver psycopg3 si el .env tiene la URL vieja con psycopg2 y decides usar postgres
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# connect_args solo es necesario para SQLite
kwargs = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def ensure_sqlite_nomina_schema() -> None:
    if engine.dialect.name != "sqlite":
        return

    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if not table_names.intersection({"nominas", "novedades"}):
        return

    with engine.begin() as connection:
        if "nominas" in table_names:
            existing_columns = {
                column["name"] for column in inspector.get_columns("nominas")
            }
            required_columns = {
                "provision_prima": "NUMERIC(12, 2) NOT NULL DEFAULT 0",
                "provision_cesantias": "NUMERIC(12, 2) NOT NULL DEFAULT 0",
                "provision_intereses_cesantias": "NUMERIC(12, 2) NOT NULL DEFAULT 0",
                "provision_vacaciones": "NUMERIC(12, 2) NOT NULL DEFAULT 0",
                "total_provisiones": "NUMERIC(12, 2) NOT NULL DEFAULT 0",
            }

            for column_name, column_sql in required_columns.items():
                if column_name not in existing_columns:
                    connection.execute(
                        text(
                            f"ALTER TABLE nominas ADD COLUMN {column_name} {column_sql}"
                        )
                    )

        unique_indexes = {
            "nominas": "uq_nominas_empleado_periodo",
            "novedades": "uq_novedades_empleado_periodo",
        }
        for table_name, index_name in unique_indexes.items():
            if table_name in table_names:
                connection.execute(
                    text(
                        f"CREATE UNIQUE INDEX IF NOT EXISTS {index_name} ON {table_name} (empleado_id, periodo)"
                    )
                )

        # R12: Asegurar columnas dinámicas en parametros_legales
        if "parametros_legales" in table_names:
            existing_params = {
                column["name"] for column in inspector.get_columns("parametros_legales")
            }
            required_params = {
                "horas_mes": "NUMERIC(5, 2) NOT NULL DEFAULT 240",
                "dias_mes": "NUMERIC(5, 2) NOT NULL DEFAULT 30",
                "porcentaje_hora_extra": "NUMERIC(5, 4) NOT NULL DEFAULT 1.25",
                "factor_salario_integral": "NUMERIC(5, 4) NOT NULL DEFAULT 0.70",
                "tope_ibc_smmlv": "INTEGER NOT NULL DEFAULT 25",
                "porcentaje_salud_empleado": "NUMERIC(5, 4) NOT NULL DEFAULT 0.04",
                "porcentaje_pension_empleado": "NUMERIC(5, 4) NOT NULL DEFAULT 0.04",
                "porcentaje_fsp": "NUMERIC(5, 4) NOT NULL DEFAULT 0.01",
                "umbral_fsp_smmlv": "INTEGER NOT NULL DEFAULT 4",
                "umbral_transporte_smmlv": "INTEGER NOT NULL DEFAULT 2",
                "porcentaje_provision_prima": "NUMERIC(6, 5) NOT NULL DEFAULT 0.0833",
                "porcentaje_provision_cesantias": "NUMERIC(6, 5) NOT NULL DEFAULT 0.0833",
                "porcentaje_provision_intereses_cesantias": "NUMERIC(6, 5) NOT NULL DEFAULT 0.01",
                "porcentaje_provision_vacaciones": "NUMERIC(6, 5) NOT NULL DEFAULT 0.0417",
            }
            for col_name, col_sql in required_params.items():
                if col_name not in existing_params:
                    connection.execute(
                        text(
                            f"ALTER TABLE parametros_legales ADD COLUMN {col_name} {col_sql}"
                        )
                    )


ensure_sqlite_nomina_schema()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
