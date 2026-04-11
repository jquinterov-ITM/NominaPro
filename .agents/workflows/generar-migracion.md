---
description: aplicar cambios de esquema en base de datos SQLite/PostgreSQL
---

# Generar migración / cambio de esquema

## Pasos

1. Modificar ackend/app/db/models.py.
2. Si se requiere recrear localmente sin Alembic, eliminar 
omina.db para regeneración automática vía create_all().
3. Actualizar ackend/app/schemas.py correspondientemente.
