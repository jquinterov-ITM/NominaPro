from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.auth import require_roles
from ..db.models import Nomina
from ..db.session import get_db
from ..repositories.nomina_repository import NominaRepository
from ..schemas import NominaLiquidar, NominaResponse
from ..services.nomina_service import liquidar_todos_empleados

router = APIRouter(prefix="/nominas", tags=["nominas"])


@router.get("/", response_model=List[NominaResponse])
def listar_nominas(db: Session = Depends(get_db)):
    """Obtiene todo el historial de nóminas procesadas"""
    return db.query(Nomina).all()


@router.get("/{nomina_id}", response_model=NominaResponse)
def obtener_nomina(nomina_id: int, db: Session = Depends(get_db)):
    nomina = db.query(Nomina).filter(Nomina.id == nomina_id).first()
    if not nomina:
        raise HTTPException(status_code=404, detail="Nómina no encontrada.")
    return nomina


@router.post(
    "/liquidar",
    response_model=List[NominaResponse],
    status_code=status.HTTP_201_CREATED,
)
def liquidar_nomina_mes(
    req: NominaLiquidar,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("RH_ADMIN", "PAYROLL_USER")),
):
    """
    Liquidación orquestada en el router.

    El router valida la solicitud, consulta datos mediante el repository,
    delega el cálculo al service y persiste el resultado con el repository.
    """
    repo = NominaRepository(db)
    try:
        # Validaciones y obtención de datos via repo
        if repo.periodo_ya_liquidado(req.periodo):
            raise ValueError(f"Período {req.periodo} ya liquidado")

        anio = int(req.periodo.split("-")[0])
        empleados = repo.get_empleados()
        param = repo.get_parametros(anio)

        novedades_por_emp = {}
        for emp in empleados:
            novedades_por_emp[emp.id] = repo.get_novedades_mes(emp.id, req.periodo)

        # Calcular nóminas usando el service
        nominas_base = liquidar_todos_empleados(
            empleados, novedades_por_emp, param, req.periodo
        )

        # Persistir resultados usando repo (repo ahora es responsable solo de persistencia)
        nominas = repo.persist_nominas(nominas_base)
        return nominas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{nomina_id}", status_code=status.HTTP_200_OK)
def eliminar_nomina(
    nomina_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles("RH_ADMIN", "PAYROLL_USER")),
):
    nomina = db.query(Nomina).filter(Nomina.id == nomina_id).first()
    if not nomina:
        raise HTTPException(status_code=404, detail="Nómina no encontrada.")

    db.delete(nomina)
    db.commit()
    return {"message": "Nómina eliminada correctamente."}
