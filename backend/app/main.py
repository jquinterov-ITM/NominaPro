from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .api import auth, empleados, nominas, novedades, parametros, auditoria
from .core.config import settings
from .db import models
from .db.session import Base, engine, ensure_sqlite_nomina_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_nomina_schema()
    yield


app = FastAPI(title="NominaPro Backend", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Los datos enviados no son válidos.",
            "code": 422,
            "details": exc.errors(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "code": exc.status_code, "details": None},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Ocurrió un error interno en el servidor.",
            "code": 500,
            "details": None,
        },
    )


@app.get("/health", tags=["health"])
def health_check():
    """Verificación rápida de estado del servidor."""
    return {"status": "ok"}


app.include_router(parametros.router, prefix="/api/parametros", tags=["parametros"])
app.include_router(empleados.router, prefix="/api/empleados", tags=["empleados"])
app.include_router(novedades.router, prefix="/api", tags=["novedades"])
app.include_router(nominas.router, prefix="/api", tags=["nominas"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(auditoria.router, prefix="/api/auditoria", tags=["auditoria"])

