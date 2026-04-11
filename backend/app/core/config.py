from decimal import Decimal
from typing import List

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Valor por defecto aproximado; en producción usar VARIABLE DE ENTORNO o tabla ParametrosLegales
    SMMLV: Decimal = Decimal("1300000")
    AUXILIO_TRANSPORTE: Decimal = Decimal("140000")
    # Auth / JWT defaults (override with env vars in production)
    SECRET_KEY: str = "NominaPro-demo-jwt-secret-2026-use-env-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEMO_USERNAME: str = "admin"
    DEMO_PASSWORD: str = "secret"
    DEMO_ROLES: str = "RH_ADMIN,PAYROLL_USER"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = ConfigDict(env_prefix="")

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
