# Guía de Exposición – NominaPro

Este documento contiene notas y puntos clave para la presentación del proyecto NominaPro.

## Resumen del sistema
- Arquitectura: Backend en FastAPI (Python) y Frontend en Vue 3 (Vite).
- Bases de datos: SQLite para desarrollo, PostgreSQL recomendado en producción.
- Autenticación: JWT con roles `RH_ADMIN`, `PAYROLL_USER`.

## Puntos para la demo
1. Mostrar la arquitectura (diagrama breve): explicar capas `api -> services -> repositories -> db`.
2. Iniciar el backend y mostrar Swagger en `/docs`.
3. Iniciar el frontend y abrir la vista de nóminas.
4. Crear empleado demo y mostrar flujo de liquidación.
4.1 (Opcional) Mostrar auditoría: crear un empleado o novedad y luego consultar `GET /api/auditoria/` con token `RH_ADMIN` para demostrar trazabilidad.
5. Mostrar pruebas unitarias y resultados de `pytest`.

## Roles y seguridad
- Explicar la gestión de roles y permisos en `core/auth.py`.
- Mostrar cómo se protege una ruta con dependencias de FastAPI.

## Puntos de implementación relevantes
- Separación clara de responsabilidades en `services` y `repositories`.
- Uso de Pydantic para validación en `schemas.py`.
- Mecanismo de migración de parámetros legales.

## Preguntas anticipadas
- ¿Cómo se manejan cambios en tasas legales?: vía tabla `parametros_legales`.
- ¿Cómo escalar en producción?: usar PostgreSQL, contenedores y CI/CD.

## Recomendaciones para la presentación
- Preparar captura de pantalla con la vista de nóminas y la liquidación exitosa.
- Tener `demo_api.sh` o `demo_api.ps1` listos para ejecutar.
- Ensayar el flujo de login con el usuario `admin`.

## Notas de alineación con el código
- **Login demo:** El token demo se obtiene en `POST /api/auth/token` (credenciales demo según configuración); úsalo para las demos que requieren rutas protegidas.
- **Novedades:** `POST /api/novedades/` hace upsert por `(empleado_id, periodo)` — al preparar la demo, limpiar datos o usar periodos distintos para evitar conflictos de unicidad.
- **Endpoints de nómina:** Usar `POST /api/nominas/liquidar` para la demo; `GET /api/nominas/` lista historial pero no filtra por `periodo` a menos que se añada soporte.
 - **Endpoints de nómina:** Usar `POST /api/nominas/liquidar` para la demo; `GET /api/nominas/` soporta `?periodo=YYYY-MM` para filtrar resultados durante la exposición.
