---
name: nominapro-dev
description: Asistente de desarrollo para NominaPro. Conoce el stack actual del proyecto (FastAPI + SQLite/PostgreSQL + Vue 3/Vite) y aplica convenciones para evolución incremental.
---

# NominaPro – Skill de Desarrollo

## Descripción del proyecto

**NominaPro** es una aplicación web para gestionar empleados, novedades y liquidación mensual de nómina bajo las normativas colombianas de 2026.

- **Frontend**: Vue 3 + Vite
- **backend**: Python + FastAPI + Pydantic v2
- **Base de datos**: SQLite (Local) / PostgreSQL (Producción) con SQLAlchemy
- **Infraestructura**: Ejecución local

## Estructura del proyecto

```
NominaPro/
├── backend/
│   ├── app/
│   │   ├── main.py (Punto de entrada FastAPI y CORS)
│   │   ├── api/ (Endpoints por módulo)
│   │   ├── schemas.py (Pydantic v2)
│   │   ├── db/
│   │   │   ├── models.py (SQLAlchemy)
│   │   │   └── session.py
├── frontend/
│   ├── src/
│   │   ├── services/api.js (Instancia Axios)
│   │   ├── views/ (Componentes Vue)
│   │   ├── router/
│   │   └── App.vue
│   ├── vite.config.js (Proxy a 8000)
│   └── package.json
└── docs/, prompts/ (Documentación y directrices de IA)
```

## Convenciones de backend

- Modelos de DB se definen en backend/app/db/models.py.
- Esquemas de validación de datos en backend/app/schemas.py (Pydantic v2).
- Evitar caracteres nulos/ocultos al guardar archivos.
- Las rutas se organizan en backend/app/api/ y se incluyen en main.py.
- Retornar errores legibles (HTTPException 400 y 422).

## Convenciones de Frontend

- Utilizar Vue 3 Composition API `<script setup>`.
- Formatear valores monetarios con 	oLocaleString('es-CO') al mostrar.
- Al enviar payloads, convertir strings formateados a Number.
- Interceptar errores 400/422 y mostrarlos al usuario en un div con user-select: text para permitir copiarlos.

## Comandos frecuentes

```bash
# backend
cd backend
../.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 9000

# Frontend
cd frontend
npm run dev
```
