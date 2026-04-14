---
name: nominapro-dev
description: Skill operativo para ejecutar y evolucionar NominaPro desde cero, con pasos verificables y trazables.
---

# NominaPro – Skill de Desarrollo (Ejecución desde cero)

## Compatibilidad multiplataforma

Los ejemplos de arranque y los comandos de este prompt funcionan en Windows (PowerShell/CMD), macOS y Linux (bash/zsh). Ejemplo mínimo para crear/activar el entorno virtual:

- Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

- macOS / Linux (bash/zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

## Objetivo del skill

Este skill define el **paso a paso estándar** para que cualquier agente o desarrollador pueda:

1. Levantar NominaPro desde una máquina limpia.
2. Verificar backend y frontend en orden correcto.
3. Ejecutar cambios incrementales sin romper flujos existentes.
4. Dejar evidencia mínima de validación y documentación actualizada.

## Contexto del proyecto

- **Frontend**: Vue 3 + Vite
- **Backend**: Python + FastAPI
- **Persistencia**: SQLite local (`nominapro.db`) / PostgreSQL en escenarios productivos
- **Módulos actuales**: parámetros, empleados, novedades, nóminas
 - **Módulos actuales**: parámetros, empleados, novedades, nóminas, auditoria

## Estructura base esperada

```text
NominaPro/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── db/
│   │   └── schemas.py
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   └── src/
├── docs/
├── prompts/
├── README.md
└── TODO.md
```

## Protocolo obligatorio “desde cero” (checklist)

### 0) Preflight técnico
- Confirmar versiones:
  - `python --version` (3.11+)
  - `pip --version`
  - `node -v` (20+)
  - `npm -v`
- Confirmar ubicación en la raíz del repositorio (`NominaPro/`).

### 1) Backend primero (orden obligatorio)
1. Crear entorno virtual:
   - Windows PowerShell: `python -m venv .venv`
2. Activar entorno:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
3. Instalar dependencias:
   - `pip install -r backend/requirements.txt`
4. Configurar base local o productiva:
   - SQLite local recomendado: `DATABASE_URL=sqlite:///./nominapro.db`
   - PostgreSQL (si aplica): `DATABASE_URL=postgresql+psycopg://usuario:password@localhost:5432/nominapro`
5. Levantar API:
   - `uvicorn app.main:app --reload --app-dir backend`
6. Validar:
   - `http://localhost:8000/docs`
   - `GET /api/empleados/`
   - `GET /api/novedades/`
   - `GET /api/nominas/`
   - Contratos mínimos:
     - `POST /api/novedades/` requiere `empleado_id`, `periodo`, `tipo` (`HORA_EXTRA`, `INCAPACIDAD`, `DESCUENTO`, `BONIFICACION`) y `valor`.
     - `POST /api/nominas/liquidar` requiere `periodo`.

### 2) Frontend después
1. Abrir segunda terminal.
2. Entrar a `frontend/`.
3. Instalar dependencias:
   - `npm install`
4. Ejecutar:
   - `npm run dev`
5. Validar UI:
   - `http://localhost:5173`
   - Navegar vistas: Home, Empleados, Novedades, Nóminas.

### 3) Regla de cambios incrementales
- Hacer cambios pequeños y verificables.
- No mezclar refactor masivo con nueva funcionalidad en el mismo lote.
- Si se modifica contrato API, actualizar frontend y documentación en el mismo ciclo.
- Mantener respuestas consistentes (éxito/error).

### 4) Regla de cierre de tarea
Se considera tarea cerrada si:
- Backend y frontend arrancan sin errores.
- El flujo mínimo funciona: empleado → novedad → liquidar nómina → consultar.
- Documentación relevante actualizada (`README` y/o `docs/`).
- Evidencia registrada en `TODO.md` o documento de avance equivalente.

## Convenciones de desarrollo

- Separar rutas (`api`) de reglas de negocio (servicios/lógica).
- Validar entrada con esquemas Pydantic.
- No introducir simulaciones frontend para ocultar fallos backend.
- Conservar compatibilidad de endpoints existentes salvo decisión explícita documentada.
- Favorecer legibilidad y trazabilidad sobre complejidad prematura.

## Guía rápida para agentes

Cuando un agente reciba una tarea debe seguir este orden:

1. Leer este `prompt-skill.md`.
2. Revisar `prompts/02-prompt-agents.md`.
3. Identificar archivos impactados y planificar cambios.
4. Ejecutar cambios por lotes pequeños.
5. Verificar ejecución local y actualizar documentación.

## Criterios de calidad mínimos

- Errores con mensajes claros.
- Validaciones de datos antes del procesamiento.
- Coherencia entre docs, prompts y estado real del código.
- Cero pasos ambiguos en instrucciones de arranque.

## Comandos de referencia

```bash
# Backend
python -m venv .venv

# Activar en Windows PowerShell:
.venv\Scripts\Activate.ps1
# Activar en macOS / Linux (bash/zsh):
# source .venv/bin/activate

pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend

# Frontend
cd frontend
npm install
npm run dev
```

## Notas de alineación con el código
- **Autenticación:** El backend ya expone autenticación JWT de prueba con usuario demo y roles (`RH_ADMIN`, `PAYROLL_USER`). Actualiza credenciales demo si se cambian en `core/config.py`.
- **Novedades:** `POST /api/novedades/` realiza *upsert* por `(empleado_id, periodo)`; no existe endpoint público filtrado por `empleado_id`/`periodo` (solo listado general y acceso por `novedad_id`).
- **Nóminas:** La generación se realiza con `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve todo y `GET /api/nominas/{id}` existe, pero no hay filtro por `periodo` en la API actual.
 - **Novedades:** `POST /api/novedades/` realiza *upsert* por `(empleado_id, periodo)`; `GET /api/novedades/` ahora soporta filtros por `?empleado_id` y `?periodo`.
 - **Nóminas:** La generación se realiza con `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve historial y soporta filtro `?periodo=YYYY-MM`.
 - **Auditoría:** Se añadió `POST /api/auditoria/` y `GET /api/auditoria/` protegidos por `RH_ADMIN` para trazabilidad administrativa.
- **Términos:** Usar `tipo_salario` (valores `ORDINARIO`/`INTEGRAL`) en lugar de "tipo de contrato" para coherencia con modelos y esquemas.
