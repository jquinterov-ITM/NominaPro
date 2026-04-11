---
description: agregar un nuevo endpoint a un módulo existente del backend de NominaPro (FastAPI)
---

# Agregar endpoint a módulo existente

Usar cuando necesites añadir un endpoint nuevo sin crear un módulo completo desde cero.

## Pasos

1. Modificar backend/app/schemas.py si el endpoint necesita validaciones de Pydantic.
2. Modificar backend/app/db/models.py si el cambio implica base de datos.
3. Implementar el endpoint en backend/app/api/{modulo}.py.
4. Asegurar retornar el esquema Response adecuado (
esponse_model).
5. Actualizar el frontend (frontend/src/views/{Modulo}View.vue y/o api.js) para consumir el endpoint.
6. Probar levantando Uvicorn.
