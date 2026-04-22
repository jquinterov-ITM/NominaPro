import secrets
import warnings
from decimal import Decimal
from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Valor por defecto aproximado; en producción usar VARIABLE DE ENTORNO o tabla ParametrosLegales
    SMMLV: Decimal = Decimal("1300000")
    AUXILIO_TRANSPORTE: Decimal = Decimal("140000")
    # Auth / JWT (mover secrets a variables de entorno)
    # En producción se recomienda definir `SECRET_KEY` en el .env o en las variables del entorno.
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEMO_USERNAME: str = "admin"
    # Evitar dejar contraseñas por defecto en repositorio; usar .env
    DEMO_PASSWORD: str = ""
    DEMO_ROLES: str = "RH_ADMIN,PAYROLL_USER"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Cargar variables desde .env si existe
    model_config = ConfigDict(
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins_list(self) -> List[str]:
        return [
            origin.strip()
            for origin in self.ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    @property
    def demo_roles_list(self) -> List[str]:
        return [role.strip() for role in self.DEMO_ROLES.split(",") if role.strip()]


settings = Settings()

# Seguridad: si no se proporciona SECRET_KEY en el entorno, generar uno efímero
if not settings.SECRET_KEY:
    warnings.warn(
        "No SECRET_KEY encontrado en el entorno. Se generará una clave efímera para desarrollo. "
        "Define SECRET_KEY en .env para entornos reales.",
        UserWarning,
    )
    settings.SECRET_KEY = secrets.token_urlsafe(32)

if not settings.DEMO_PASSWORD:
    warnings.warn(
        "No DEMO_PASSWORD encontrado en el entorno. Se recomienda definir una contraseña demo en .env.",
        UserWarning,
    )
    # Valor por defecto temporal para desarrollo (no recomendado en producción)
    settings.DEMO_PASSWORD = "secret"
