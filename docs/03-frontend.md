# Documentación Frontend – NominaPro

## Objetivo
Definir la estructura y criterios de implementación de la SPA en Vue para operar empleados, novedades y nóminas consumiendo la API real.

## Arquitectura Frontend
- SPA con Vue 3 + Vite.
- Organización por `views`, `components`, `stores` y `services`.
- La capa `services` centraliza llamadas HTTP a `/api`.
- El frontend no simula datos cuando el backend falla; muestra el error real.

## Módulos UI
| Módulo | Función | Estado esperado |
|---|---|---|
| Empleados | Crear, listar y eliminar | Formulario, tabla y confirmación |
| Novedades | Registrar por período | Upsert y validación por `YYYY-MM` |
| Nóminas | Liquidar y consultar | Resumen mensual y detalle |

## Validaciones y UX
- Validar campos obligatorios, rangos numéricos y formato de período.
- Mostrar estados de carga, vacío, éxito y error.
- Presentar mensajes claros para errores 400 y 422.

## Seguridad Frontend
- Preparar manejo de JWT cuando el login deje de ser demo.
- Proteger rutas por rol en fases posteriores.
- No exponer secretos en cliente.

## Calidad
- Pruebas unitarias para componentes críticos.
- Pruebas de flujo mensual contra la API.
- Lint y formato antes de merge.

## Roadmap
1. MVP de operación mensual.
2. Validaciones y UX avanzada.
3. Soporte de estados y trazabilidad.