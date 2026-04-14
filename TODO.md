# TODO simplificado — NominaPro

## Resumen de lo completado
- Documentación base y guías esenciales en `/docs/`.
- Backend: `nomina_service`, `nomina_repository` y routers principales implementados.
- Endpoints CRUD para `empleados`, `novedades` y generación de nóminas disponibles.
- Seguridad demo (JWT), pruebas unitarias e integración básicas y scripts de arranque documentados.

## Pendientes (prioridad y seguimiento)

- Filtros en API: evaluar e implementar (opcional/pendiente):
	- `GET /api/nominas?periodo=YYYY-MM`
	- `GET /api/novedades?empleado_id=...` 
	- Estado: pendiente — mejora futura (evitar carga innecesaria en frontend).

- Auditoría (R10): diseño e implementación de la tabla y endpoints de auditoría.
- Auditoría (R10): diseño e implementación de la tabla y endpoints de auditoría.
	- Estado: implementado (esquema mínimo y endpoints `POST /api/auditoria/`, `GET /api/auditoria/` añadidos). Requiere pruebas y validación en entorno local.

## Prioridad sugerida
1. Auditoría (R10) — diseño y API mínima para captura de eventos.
2. Filtros en API según necesidades del frontend.
3. Mejoras menores y refactorizaciones (si surgen durante pruebas).

## Instrucciones para marcar tareas como completadas
- Para cambios de documentación o código ya aplicados, deja un comentario en este archivo indicando qué se completó y la fecha.
- Cuando termines pruebas locales, haz commit manual y actualiza esta sección con la referencia del commit.

## Siguiente paso (táctico)
- Diseñar el esquema de `Auditoria` y proponer el primer endpoint (`POST /api/auditoria/`) — puedo generar el esquema inicial si quieres.

*Actualizado: 2026-04-14*
