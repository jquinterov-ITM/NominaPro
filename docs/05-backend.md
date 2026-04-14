# Documentación Backend – NominaPro

## Objetivo
Describir la arquitectura, rutas y aspectos operativos del backend (FastAPI) para desarrolladores y operadores.

## Estructura principal
- `backend/app/main.py` — arranque y registro de routers.
- `backend/app/api/` — routers: `empleados.py`, `novedades.py`, `nominas.py`, `parametros.py`.
- `backend/app/services/` — lógica de negocio (cálculo de nómina).
- `backend/app/repositories/` — persistencia y helpers (ej: `NominaRepository`).
- `backend/app/db/models.py` — modelos SQLAlchemy (`Empleado`, `Novedad`, `Nomina`, `ParametrosLegales`).
- `backend/app/schemas.py` — Pydantic para validación y serialización.

## Endpoints principales (prefijo `/api`)

- `GET /health` — endpoint de verificación de salud (no requiere prefijo `/api`). Retorna `200 OK` con `{"status": "ok"}` cuando la API está operativa.
- `POST /api/empleados/` — crear empleado (valida unicidad `documento`, valida integral >= 13 SMMLV según `ParametrosLegales`).
- `GET /api/empleados/` — listar empleados.
- `GET /api/empleados/{id}` — obtener empleado.
- `PUT /api/empleados/{id}` — actualizar empleado (mismas validaciones que creación: unicidad de documento, salario integral >= 13 SMMLV).
- `DELETE /api/empleados/{id}` — eliminar empleado y cascada lógica sobre novedades/nominas.

- `GET /api/novedades/` — listar todas las novedades.
- `GET /api/novedades/{id}` — obtener novedad.
- `POST /api/novedades/` — crea o actualiza (upsert) una novedad por `(empleado_id, periodo)`.
- `DELETE /api/novedades/{id}` — eliminar novedad.

- `GET /api/nominas/` — lista histórico de nóminas.
- `GET /api/nominas/{id}` — obtener nómina.
- `POST /api/nominas/liquidar` — orquesta el cálculo masivo de nóminas (usa `services.nomina_service` y `repositories` para persistencia).

- `POST /api/auditoria/` — registra un evento de auditoría (restringido a `RH_ADMIN`).
- `GET /api/auditoria/` — lista eventos recientes de auditoría (restringido a `RH_ADMIN`).

## Seguridad
- Autenticación JWT integrada (endpoint `POST /api/auth/token` para token demo).
- Dependencias `require_roles(...)` aplicadas en routers para `RH_ADMIN` y `PAYROLL_USER`.

## Reglas de negocio críticas implementadas
- Validación salario integral (>= 13 SMMLV) en creación de empleado.
- Cálculo de IBC, aportes, FSP y auxilio transporte según `ParametrosLegales`.
- Unicidad por `(empleado_id, periodo)` para `novedades` y `nominas` (UniqueConstraint).

## Observaciones y recomendaciones
- Filtros expuestos: `GET /api/nominas?periodo=YYYY-MM` y `GET /api/novedades?empleado_id=&periodo=` implementados para consultas más eficientes desde el frontend.
- Auditoría: endpoints `POST /api/auditoria/` y `GET /api/auditoria/` implementados (acceso restringido a `RH_ADMIN`). Considerar ampliar campos de `Auditoria` en siguientes iteraciones (valor_anterior/valor_nuevo).
- Mantener pruebas de integración que usen tokens demo y limpien registros entre casos para evitar conflictos por unicidad.
