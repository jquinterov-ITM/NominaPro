from typing import List, Optional

import bcrypt
from sqlalchemy.orm import Session

from ..db.models import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def get_by_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def list_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def create(self, username: str, password: str, roles: str) -> Usuario:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        usuario = Usuario(username=username, password_hash=password_hash, roles=roles)
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def verificar_password(self, usuario: Usuario, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), usuario.password_hash.encode())

    def update_password(self, usuario_id: int, new_password: str) -> bool:
        usuario = self.get_by_id(usuario_id)
        if not usuario:
            return False
        usuario.password_hash = bcrypt.hashpw(
            new_password.encode(), bcrypt.gensalt()
        ).decode()
        self.db.commit()
        return True

    def seed_admin_if_not_exists(
        self, username: str, password: str, roles: str
    ) -> Usuario:
        usuario = self.get_by_username(username)
        if not usuario:
            return self.create(username, password, roles)
        return usuario
