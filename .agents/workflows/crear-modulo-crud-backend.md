---
description: crear un nuevo módulo en backend (FastAPI) para NominaPro
---

# Crear módulo en backend

Usar cuando necesites agregar un nuevo recurso REST completo al backend de InvoiceLite.

## Pasos

1. Definir la tabla SQLAlchemy en backend/app/db/models.py.
2. Crear esquemas (Pydantic v2) en backend/app/schemas.py.
3. Crear archivo de rutas backend/app/api/{modulo}.py (GET, POST, PUT, DELETE).
4. Incluir el router en backend/app/main.py.
5. Ejecutar uvicorn para asegurar que SQLite compile la nueva tabla.
