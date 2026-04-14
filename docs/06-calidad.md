# Documentación de Calidad – NominaPro

## Estrategia de Testing
- Unitarios para reglas de nómina.
- Integración para endpoints FastAPI con DB de prueba.
- E2E opcional para flujo UI → API.

## Tests Backend
| Módulo | Happy path | Error principal |
|---|---|---|
| Empleados | Crear y listar | Campos faltantes, documento duplicado |
| Novedades | Crear, listar y eliminar | Empleado no existe, período ausente |
| Nóminas | Generar, consultar y eliminar | Sin período, duplicado, sin empleados |
| Cálculo | Liquidación correcta | Valores inválidos |

## Tests Frontend (Vitest)
- Pruebas de componentes para asegurar que la UI reaccione correctamente a los estados del backend.

## Calidad de Código
- Black para backend.
- ESLint/Prettier para frontend.
- Vitest para pruebas de componentes frontend.
- Commits convencionales.

## Cobertura
- Cobertura Backend: meta alta en `backend.app.services.nomina_service`.
- Ejecutar `npm run test` en la carpeta `frontend`.
- Ejecutar `python -m pytest` para validar el motor de nómina.

## Comandos Recomendados
### Backend
```cmd
.venv\Scripts\python -m pytest -q
```

### Frontend
```cmd
cd frontend
npm run test
```

```cmd
.venv\Scripts\pre-commit run --all-files
```

## Notas de alineación con el código
- **Tests existentes:** Hay tests unitarios en `tests/unit/test_nomina_service.py` que cubren `liquidar_todos_empleados`.
- **Integración con API real:** Las pruebas de integración deben usar los endpoints reales (`/api`) y respetar la unicidad por `(empleado_id, periodo)`; `POST /api/novedades/` hace upsert y puede causar conflictos si no se limpian datos entre pruebas.
- **JWT en pruebas:** Para endpoints protegidos, obtener token demo en `POST /api/auth/token` y usar en encabezados `Authorization: Bearer <token>`.
