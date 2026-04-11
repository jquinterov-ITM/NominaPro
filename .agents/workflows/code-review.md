---
description: revisar y corregir código de NominaPro en Frontend Vue y Backend FastAPI
---

# Code Review de NominaPro

Usar antes de hacer commit, crear un Pull Request o hacer merge de cambios.

## Pasos

1. Backend (FastAPI):
   - Validaciones estrictas con Pydantic.
   - Manejo de excepciones (HTTPException 400).
   - Lógica de nómina (ej. > 13 SMMLV para salario integral) bien aplicada.
2. Frontend (Vue 3):
   - Payloads de Axios deben coincidir exactamente con Pydantic (documento vs identificacion).
   - Campos monetarios deben enviarse como Number.
   - Errores de validación (422) de FastAPI mostrados claramente.
   - Bloques de error con user-select: text.
