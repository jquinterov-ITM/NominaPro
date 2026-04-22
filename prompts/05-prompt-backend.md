# Prompt: Backend – Python/FastAPI con Buenas Prácticas (NominaPro)

## Compatibilidad multiplataforma

Los ejemplos de instalación y arranque están escritos para funcionar en Windows (PowerShell/CMD) y en macOS/Linux. Ejemplo mínimo de `venv`:

PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

CMD:
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

macOS / Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

## Contexto del Proyecto
- **Nombre**: NominaPro
- **Backend**: Python + FastAPI
- **Base de datos**: SQLite (Desarrollo Local) / PostgreSQL con psycopg[binary] (Producción)
- **Frontend**: Vue.js
- **Módulos actuales**: empleados, novedades, nóminas
 - **Módulos actuales**: empleados, novedades, nóminas, auditoria

## Objetivo
Generar el archivo `/docs/05-backend.md` de **NominaPro**.
Proponer e implementar mejoras del backend de **NominaPro** manteniendo su enfoque pedagógico, sin romper endpoints actuales y con cambios incrementales de bajo riesgo.

## Estado operativo actual
- El backend ya expone rutas reales para empleados, novedades y nóminas.
- No se deben introducir simulaciones en frontend como sustituto de endpoints faltantes.
- Las rutas consumidas por el frontend deben mantenerse bajo `/api` y responder con datos persistidos en la base de datos.

## Instrucciones

Actúa como backend engineer y entrega una propuesta técnica en Markdown que incluya:

### 1. Diagnóstico del Estado Actual
- Arquitectura actual (`main.py`, `api`, `db`, `schemas.py`).
- Fortalezas (simplicidad, claridad del flujo) y limitaciones (acoplamiento, validación y manejo de errores distribuido).

### 2. Objetivo de Refactor Incremental
- Mantener compatibilidad de API actual:
	- `GET/POST/PUT/DELETE /api/empleados`
	- `GET/POST /api/novedades`
	- `GET /api/nominas`
	- `GET /api/nominas/{id}`
	- `POST /api/nominas/liquidar`
- Separar responsabilidades de forma gradual: `routers → services → repositories`.

### 3. Propuesta de Estructura (sin sobreingeniería)
```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── repositories/
│   ├── db/
│   │   ├── session.py
│   │   └── models.py
│   ├── schemas/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   └── utils/
├── tests/
└── requirements.txt
```

Nota: incluye una carpeta `backend/alembic/` en el control de versiones si gestionas migraciones, y asegúrate de listar `alembic` en `requirements.txt` para entornos limpios.

### 4. Validación y Errores
- Definir validaciones de request por endpoint (campos requeridos, tipos y rangos).
- Estandarizar respuestas de error con formato único (ej. `{ message, code, details }`).
- Implementar handlers globales de excepciones en FastAPI.

### 5. Reglas de Negocio Críticas (Dominio 2026)
- **Modelado de BD (SQLAlchemy agnóstico a SQLite/PostgreSQL):** 
  - Crear modelo `ParametrosLegales` con campos para: `anio`, `smmlv`, `auxilio_transporte`, `horas_mes`, `dias_mes`, `porcentaje_hora_extra`, `factor_salario_integral`, `tope_ibc_smmlv`, `porcentaje_salud_empleado`, `porcentaje_pension_empleado`, `porcentaje_fsp`, `umbral_fsp_smmlv`, `umbral_transporte_smmlv`, y porcentajes de provisiones.
  - Actualizar modelo `Empleado` con `tipo_salario` (enum: 'ORDINARIO' o 'INTEGRAL').
	- **Auditoría:** Crear modelo `Auditoria` (usuario_id, accion, detalle, fecha) para registrar cambios administrativos y operativos. Endpoints `POST /api/auditoria/` y `GET /api/auditoria/` deben estar protegidos por rol `RH_ADMIN`.
	- Nota: `valor_anterior` / `valor_nuevo` pueden añadirse en una futura versión si se requiere almacenar estados previos y nuevos de manera estructurada.
- **Validación Salario:** Al crear empleado (`POST /api/empleados`), si es 'INTEGRAL', el salario base estrictamente **no puede ser menor a 13 SMMLV** (usando `ParametrosLegales`). Lanzar HTTP 400 si no cumple.
- **Cálculo IBC y Aportes:** El IBC no puede ser inferior a 1 SMMLV ni superior a 25 SMMLV. Si es Integral, IBC pensión/salud = 70% del base. Calcular Salud (Emp 4%, Pat 8.5%), Pensión (Emp 4%, Pat 12%), Caja (Pat 4%).
- **FSP y Transporte:** Auxilio de Transporte si el salario base es < 2 SMMLV (solo Ordinario). FSP si IBC Pensión >= 4 SMMLV (inicia en 1%).
- **Prestaciones:** Provisionar mensualmente para Ordinarios: Prima (8.33%), Cesantías (8.33%), Int. Cesantías (1%), Vacaciones (4.17%).
- **Estados de Nómina:** La nómina debe transitar los estados 'BORRADOR', 'LIQUIDADA' y 'CERRADA_DIAN'.
- Conservar idempotencia mensual y unicidad por `(empleado_id, periodo)` para novedades y nóminas.

### 6. Seguridad Base
- Preparar base para JWT + roles (sin obligar implementación completa inmediata).
- Añadir recomendaciones mínimas: CORS restringido por entorno, rate limit para endpoints sensibles, headers de seguridad y gestión de secretos por entorno.

### 7. Estrategia de Pruebas
- Unit tests para `calcularNomina`.
- Integration tests para endpoints clave con `pytest` + `httpx` y DB temporal.
- Casos mínimos: happy path, validación fallida, recurso no encontrado y conflicto de unicidad.

### 8. Plan de Implementación por Fases
- Fase 1: normalizar validación y errores.
- Fase 2: extraer acceso a datos / repositorios.
- Fase 3: pruebas automatizadas.
- Fase 4: seguridad (JWT + roles).

## Formato de Salida
- Markdown estructurado con secciones, tablas y checklist de tareas accionables.

## Notas de alineación con el código
- **Autenticación:** JWT ya está implementado y utilizado en dependencias `require_roles` en routers (`backend/app/core/auth.py`).
- **Novedades:** `POST /api/novedades/` realiza *upsert* por `(empleado_id, periodo)`; el repositorio (`NominaRepository`) sí posee helpers para obtener novedades por empleado+periodo, pero no hay endpoint público para ese filtrado.
- **Nóminas:** Orquestación en `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve historial completo sin filtro `periodo` en la API actual.
 - **Nóminas:** Orquestación en `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve historial y soporta filtro por `?periodo=YYYY-MM`.
 - **Novedades:** `GET /api/novedades/` soporta filtros `?empleado_id=` y `?periodo=` para facilitar consultas del frontend.
- **Modelos:** `ParametrosLegales`, `Empleado`, `Novedad`, `Nomina` están implementados en `backend/app/db/models.py` y los esquemas en `backend/app/schemas.py`.

## Cambios recientes (resumen)

- `.env.example` añadido; mover secretos a variables de entorno.
- Alembic configurado en `backend/alembic/` y migración inicial disponible; seguir `docs/07-implementacion.md` para aplicar migraciones.
- `pre-commit` integrado (black/isort/ruff) y un workflow CI básico añadido.
- Pequeñas correcciones operativas: cierre de engine al salir y uso de timestamps enteros en JWT `exp`.

Recomendación: verificar `backend/requirements.txt` y añadir `alembic` si planeas usar migraciones en entornos limpios.
