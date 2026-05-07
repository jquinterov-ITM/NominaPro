# TODO simplificado — NominaPro

## Resumen de lo completado
- Documentación base y guías esenciales en `/docs/`.
- Backend: `nomina_service`, `nomina_repository` y routers principales implementados.
- Endpoints CRUD para `empleados`, `novedades` y generación de nóminas disponibles.
- Seguridad JWT con usuarios en BD (bcrypt), pruebas unitarias e integración.
- Paginación en APIs y validación SMMLV.
- Tests frontend con Vitest.

## Completados Mayo 2026
- ✅ Usuarios en BD con bcrypt (reemplaza usuario demo en memoria)
- ✅ Validación salary >= SMMLV al crear/actualizar empleados
- ✅ Paginación en APIs (`?page=`, `?limit=`, `?search=`)
- ✅ Tests frontend con Vitest
- ✅ Tests E2E con Playwright (`tests/e2e/`)
- ✅ Tests de carga (`tests/load/load_test.py`)
- ✅ Tests de estrés (`tests/stress/stress_test.py`)
- ✅ Documentación de pruebas (`docs/06-pruebas.md`)
- ✅ Documentación actualizada (README.md, docs/)

## Pendientes
- Dockerización del proyecto
- CI/CD con GitHub Actions
- Dashboard con métricas
- Exportar nóminas a PDF/Excel
- Rate limiting en APIs

## Prioridad sugerida
1. Dockerización para reproducibilidad
2. CI/CD para automatizar tests y build
3. Dashboard con métricas de nómina
4. Exportar reportes

*Actualizado: 2026-05-06*
