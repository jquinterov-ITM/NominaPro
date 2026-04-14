# Prompt: Documentación de Arquitectura – NominaPro

## Compatibilidad multiplataforma

Los comandos y ejemplos de este prompt son multiplataforma (Windows PowerShell/CMD y macOS/Linux). Ejemplo mínimo para crear/activar `venv`:

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
- **Frontend**: Vue.js
- **Backend**: Python + FastAPI
- **Base de datos**: SQLite (Desarrollo Local) / PostgreSQL usando psycopg[binary] (Producción)
- **Infraestructura**: ejecución local simple y después en Kubernetes

## Objetivo
Generar el archivo `/docs/01-arquitectura.md` de **NominaPro**.

## Instrucciones

Genera un documento de arquitectura en Markdown que incluya:

### 1. Visión General
- Descripción del sistema de nómina **NominaPro**, enfocado en reglas 2026 (Salario Integral, DIAN, UGPP).
- Arquitectura cliente-servidor con API REST.
- Diagrama de alto nivel (Mermaid) mostrando: Usuario → Frontend (Vue) → API (FastAPI) → SQLite (Local) / PostgreSQL (PROD).

### 2. Estructura del Repositorio
```text
NominaPro/
├── backend/
│   ├── app/
│   │   ├── main.py                 # Arranque FastAPI
│   │   ├── api/                    # Routers por módulo
│   │   ├── services/               # Reglas de cálculo de nómina
│   │   ├── repositories/           # Acceso a datos
│   │   └── db/                     # Conexión/modelos de BD (SQLite en dev / Postgres en prod)
│   └── requirements.txt
├── frontend/
│   └── src/
├── docs/
├── prompts/
└── README.md
```

### 3. Componentes del Sistema

#### Frontend (Vue.js)
- Interfaz SPA para operación de empleados, novedades y nóminas.
- Consumo de endpoints REST.
- Manejo de formularios, validaciones y estado de operación mensual.

#### Backend (Python + FastAPI)
- Punto de entrada en `main.py`.
- Routers por módulo (`empleados`, `novedades`, `nominas`).
- Servicios de negocio para liquidación.
- Exposición de endpoints bajo prefijo `/api` y endpoint `/health`.

#### Base de Datos (SQLite Local / PostgreSQL Producción)
- Conexión administrada por SQLAlchemy (compatible SQLite/PostgreSQL).
- Tablas principales: `empleados`, `novedades`, `nominas`.
- Restricciones de unicidad por documento y por `(empleado_id, periodo)`.

### 4. Comunicación entre Componentes
- Protocolo HTTP/REST + JSON.
- CORS habilitado para el frontend Vue por entorno.
- Patrón request/response síncrono para CRUD y generación de nómina.

### 5. Módulos Principales

| Módulo     | Frontend (Vue) | Backend (FastAPI `/api`) |
|------------|-----------------|---------------------------|
| Empleados  | Gestión de empleados | `GET /empleados`, `POST /empleados`, `PUT /empleados/{id}` |
| Novedades  | Registro por período | `GET /novedades/`, `POST /novedades` (upsert) |
| Nóminas    | Generación y consulta mensual | `POST /nominas/liquidar`, `GET /nominas/` |

### 6. Flujo Funcional Principal: Liquidación Mensual
Incluye un diagrama Mermaid `sequenceDiagram` con:
- Registro/actualización de novedades.
- Solicitud de generación mensual.
- Cálculo por empleado: Lectura de parámetros (SMMLV, topes), procesamiento Ordinario/Integral (factor 70/30), generación de aportes, FSP.
- Persistencia de resultados.
- Respuesta consolidada para frontend.

### 7. Riesgos y Ruta de Evolución
- Riesgos actuales: acoplamiento en reglas, crecimiento de módulos, validaciones dispersas, pruebas limitadas.
- Ruta de evolución:
	- separación estricta `api → service → repository`,
	- validación centralizada con Pydantic,
	- manejo de errores estandarizado,
	- **Base de datos**: SQLite para desarrollo local (sin configuración extra); PostgreSQL para producción (pooling, transacciones y observabilidad via `psycopg[binary]`). El cambio entre motores se controla únicamente con la variable `DATABASE_URL`,
	- estrategia de pruebas unitarias e integración.

## Formato de Salida
- Markdown bien estructurado con headers, tablas y diagramas Mermaid.


## Actualización (Día Actual)
El sistema ha materializado la arquitectura definida empleando Vue 3 con Vite en el frontend y FastAPI en el backend. Toda validación estricta de payloads (Pydantic v2) se coordina a través de Axios, manejando adecuadamente los formatos numéricos y parseos de respuestas HTTP.

## Notas de alineación con el código
- **Endpoints reales:** En el código actual los routers están bajo `/api` y los endpoints principales son `POST /api/empleados/`, `GET /api/empleados/`, `PUT /api/empleados/{id}`, `DELETE /api/empleados/{id}`, `POST /api/novedades/` (upsert), `GET /api/novedades/`, `POST /api/nominas/liquidar`, `GET /api/nominas/` y `GET /api/nominas/{id}`.
- **Filtros:** Los endpoints `GET /novedades/` y `GET /nominas/` devuelven el historial completo sin filtros por `periodo`. Se sugiere implementar `?periodo=YYYY-MM` si el frontend lo requiere.
- **Términos y modelos:** usar `tipo_salario` en documentación y UI (valores `ORDINARIO`/`INTEGRAL`).
