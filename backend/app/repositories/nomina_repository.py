from typing import Dict, List

from sqlalchemy.orm import Session

from ..db.models import Empleado, Nomina, Novedad, ParametrosLegales
from ..schemas import NominaBase


class NominaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_empleados(self) -> List[Empleado]:
        """Obtiene todos los empleados activos."""
        return self.db.query(Empleado).all()

    def get_parametros(self, anio: int) -> ParametrosLegales:
        """Obtiene parámetros legales por año."""
        param = (
            self.db.query(ParametrosLegales)
            .filter(ParametrosLegales.anio == anio)
            .first()
        )
        if not param:
            raise ValueError(f"No hay parámetros legales para {anio}")
        return param

    def get_novedades_mes(self, empleado_id: int, periodo: str) -> List[Novedad]:
        """Novedades por empleado/periodo."""
        return (
            self.db.query(Novedad)
            .filter(Novedad.empleado_id == empleado_id, Novedad.periodo == periodo)
            .all()
        )

    def periodo_ya_liquidado(self, periodo: str) -> bool:
        """Check duplicado."""
        return (
            self.db.query(Nomina).filter(Nomina.periodo == periodo).first() is not None
        )

    def list_nominas(self, periodo: str | None = None) -> List[Nomina]:
        """Lista nóminas, opcionalmente filtrando por periodo (YYYY-MM)."""
        q = self.db.query(Nomina)
        if periodo:
            q = q.filter(Nomina.periodo == periodo)
        return q.all()

    def persist_nominas(self, nominas_base: List[object]) -> List[Nomina]:
        """Persiste una lista de objetos pydantic (NominaBase) como registros Nomina."""
        nominas = []
        for nb in nominas_base:
            # soportar tanto pydantic v1 (dict) como v2 (model_dump)
            if hasattr(nb, "model_dump"):
                data = nb.model_dump()
            elif hasattr(nb, "dict"):
                data = nb.dict()
            else:
                data = dict(nb)

            nomina = Nomina(**data)
            self.db.add(nomina)
            nominas.append(nomina)

        self.db.commit()
        for n in nominas:
            self.db.refresh(n)
        return nominas
