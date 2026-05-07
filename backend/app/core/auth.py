from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..db.session import SessionLocal
from ..repositories.usuario_repository import UsuarioRepository
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

SECRET_KEY = str(settings.SECRET_KEY)
ALGORITHM = str(settings.ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str) -> Optional[dict]:
    db = next(get_db())
    try:
        repo = UsuarioRepository(db)
        usuario = repo.get_by_username(username)
        if not usuario or not usuario.activo:
            return None
        if not repo.verificar_password(usuario, password):
            return None
        return {
            "username": usuario.username,
            "roles": usuario.roles.split(","),
            "id": usuario.id,
        }
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") or payload.get("username")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de autenticación inválidas.",
            )
        db = next(get_db())
        try:
            repo = UsuarioRepository(db)
            usuario = repo.get_by_username(username)
            if usuario is None or not usuario.activo:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no encontrado o inactivo.",
                )
            roles = payload.get("roles")
            if not isinstance(roles, list):
                roles = usuario.roles.split(",")
            return {"username": usuario.username, "roles": roles, "id": usuario.id}
        finally:
            db.close()
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado."
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido."
        )


def require_roles(*allowed_roles: str):
    def dependency(current_user: dict = Depends(get_current_user)) -> dict:
        user_roles = set(current_user.get("roles", []))
        if allowed_roles and not user_roles.intersection(allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para ejecutar esta acción.",
            )
        return current_user

    return dependency
