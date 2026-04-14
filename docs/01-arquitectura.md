# Documentación de Arquitectura – NominaPro

## Contexto del Proyecto
- **Nombre**: NominaPro
- **Frontend**: Vue.js
- **Backend**: Python + FastAPI
- **Base de datos**: SQLite (Desarrollo Local) / PostgreSQL usando psycopg[binary] (Producción)
- **Infraestructura**: ejecución local simple y después en Kubernetes

## Visión General
Descripción del sistema de nómina **NominaPro**, enfocado en reglas 2026 (Salario Integral, DIAN, UGPP).
Arquitectura cliente-servidor con API REST.

```mermaid
graph TD
    Usuario --> Frontend
    Frontend -->|HTTP/JSON| API_FastAPI
    API_FastAPI -->|SQLAlchemy| DB
    DB --> API_FastAPI
```

## Estructura del Repositorio (Actual)
```
NominaPro/
├── backend/app/
│   ├── main.py
│   ├── api/ (empleados.py, nominas.py, novedades.py, parametros.py)
│   ├── db/ (models.py, session.py)
│   └── schemas.py
├── frontend/src/views/ (EmpleadosView.vue etc.)
├── docs/
├── prompts/
└── README.md
```

## Componentes del Sistema
### Frontend (Vue 3 + Vite)
SPA para empleados, novedades, nóminas. Axios a /api.

### Backend (FastAPI)
main.py arranque, routers /api/*, servicios de nómina.

### Health Check
- `GET /health` — endpoint de verificación de salud de la API. Retorna `200 OK` con el payload `{"status": "ok"}` cuando la aplicación está operativa.

### Auditoría y filtros
- `POST /api/auditoria/` — registrar eventos administrativos (restringido a `RH_ADMIN`).
- `GET /api/auditoria/` — listar eventos de auditoría (restringido a `RH_ADMIN`).
- Filtros en APIs: `GET /api/novedades/` soporta `?empleado_id=` y `?periodo=`; `GET /api/nominas/` soporta `?periodo=YYYY-MM` para consultas más eficientes desde la UI.

### DB (SQLite local)
Modelos: Empleado, Novedad, Nomina.

## Flujo Liquidación Mensual
```mermaid
sequenceDiagram
    User->>Frontend: Registrar novedades
    Frontend->>API: POST /api/novedades
    API->>DB: Persistir
    User->>Frontend: Liquidar período
    Frontend->>API: POST /api/nominas/liquidar
    API->>Service: Calcular por empleado + novedades
    Service->>DB: Leer params SMMLV
    Note over Service,DB: Reglas 2026: integral>=13SMMLV, IBC 1-25, aportes
    Service->>DB: Persistir nóminas + auditoría
    API->>Frontend: Lista nóminas
```

## Módulos
| Módulo | API Endpoint | Funcionalidad |
|--------|--------------|---------------|
| Empleados | /api/empleados | CRUD |
| Novedades | /api/novedades | Por empleado/periodo |
| Nóminas | /api/nominas | Liquidar/listar |

## Evolución Pendiente

Estado actual: MVP operativo alineado.

## Notas de alineación con el código
- **Endpoints reales:** Los routers están expuestos bajo `/api` y los endpoints actuales incluyen `POST /api/empleados/`, `GET /api/empleados/`, `PUT /api/empleados/{id}`, `DELETE /api/empleados/{id}`, `POST /api/novedades/` (comportamiento *upsert*), `GET /api/novedades/`, `POST /api/nominas/liquidar`, `GET /api/nominas/` y `GET /api/nominas/{id}`.
- **Filtros:** La implementación ahora soporta `GET /api/nominas?periodo=...` y `GET /api/novedades?empleado_id=&periodo=`; se recomienda al frontend usar estos filtros para evitar transferencias innecesarias.
- **Términos:** usar `tipo_salario` (`ORDINARIO`/`INTEGRAL`) en documentación y en la UI para mantener coherencia con `models.py` y `schemas.py`.
