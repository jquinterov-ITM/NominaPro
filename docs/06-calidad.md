# Documentación de Calidad – NominaPro

> **Nota:** La documentación detallada de pruebas (unitarias, integración, carga, estrés, E2E) está en [06-pruebas.md](06-pruebas.md).

## Estrategia de Testing
- Unitarios para reglas de nómina.
- Integración para endpoints FastAPI con DB de prueba.
- E2E opcional para flujo UI → API.
- Carga y estrés para validar rendimiento.

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
- Frontend: tests con Vitest. Ejecutar `npm run test` para probar.
- Ejecutar `python -m pytest` para validar el motor de nómina.

## Pruebas nuevas recomendadas
- Añadir pruebas de integración que cubran filtros: `GET /api/nominas?periodo=...` y `GET /api/novedades?empleado_id=...`.
- Añadir tests de auditoría: POST `api/auditoria/` (RH_ADMIN) y GET `api/auditoria/` para verificar trazabilidad.
- Tests de paginación en endpoints de listado.

## Comandos Recomendados
### Backend - Tests unitarios e integración
```cmd
.venv\Scripts\python -m pytest -q
```

### Backend - Tests de carga
```cmd
python tests/load/load_test.py
```

### Backend - Tests de estrés
```cmd
python tests/stress/stress_test.py
```

### Frontend - Tests unitarios (Vitest)
```cmd
cd frontend
npm install
npm run test
```

### Frontend - Tests E2E (Playwright)
```cmd
cd frontend
npx playwright install
npm run test:e2e
```

```cmd
.venv\Scripts\pre-commit run --all-files
```

## Notas de alineación con el código
- **Tests existentes:** Hay tests unitarios en `tests/unit/test_nomina_service.py` que cubren `liquidar_todos_empleados`.
- **Integración con API real:** Las pruebas de integración deben usar los endpoints reales (`/api`) y respetar la unicidad por `(empleado_id, periodo)`; `POST /api/novedades/` hace upsert y puede causar conflictos si no se limpian datos entre pruebas.
- **JWT en pruebas:** Para endpoints protegidos, obtener token en `POST /api/auth/token` usando credenciales de la tabla `usuarios` (admin/secret por defecto) y usar en encabezados `Authorization: Bearer <token>`.
- **Paginación:** Los tests de integración deben adaptarse a la respuesta paginada: `{items: [], total, page, limit, total_pages}`.
- **Salario mínimo:** Los tests que crean empleados deben usar salarios >= SMMLV vigente (2026: $1,750,905).
