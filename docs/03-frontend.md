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

## Notas de alineación con el código
- **Autenticación:** El backend ya devuelve JWT demo y roles (`RH_ADMIN`, `PAYROLL_USER`); el frontend debe obtener y almacenar el token para llamadas protegidas.
- **Novedades y Upsert:** `POST /api/novedades/` implementa *upsert* por `(empleado_id, periodo)` — al crear novedades desde la UI, la interfaz debe manejar la actualización implícita.
- **Filtros de consulta:** Actualmente `GET /api/nominas/` devuelve todo; no existe `GET /api/nominas?periodo=...` — si la UI necesita filtrar por período, se debe añadir soporte en el backend o filtrar en cliente (menos óptimo).
 - **Filtros de consulta:** `GET /api/nominas/` soporta `?periodo=YYYY-MM` y `GET /api/novedades/` soporta `?empleado_id=` y `?periodo=`. Usar estos filtros desde la UI para reducir tráfico y carga.
- **Términos:** usar `tipo_salario` en formularios y validaciones (valores `ORDINARIO`/`INTEGRAL`).
 - **Auditoría:** operaciones administrativas (crear/actualizar empleado, eliminar nómina) pueden registrar eventos de auditoría en el backend; la UI no debe exponer esos datos sin autorización (`RH_ADMIN`).

## Implementación actual (resumen)

Estas notas documentan la implementación real añadida al frontend durante el desarrollo del MVP:

- **Stack:** Vue 3 + Vite, Pinia para estado, Vue Router, Axios para HTTP.
- **Estructura:** `views/`, `components/`, `stores/`, `services/`.
- **Autenticación:** Login realiza `POST /api/auth/token` enviando `application/x-www-form-urlencoded` (usar `URLSearchParams`). El token JWT se guarda en `localStorage` y en el store de Pinia (`auth`).
- **Protección de rutas:** Implementado guard global del router que usa `auth` store; rutas protegidas redirigen a `/login` si no hay token.
- **Header y navegación:** El `Header` (menú) se muestra condicionalmente según `auth.isAuthenticated`. `Logout` limpia el store y `localStorage`.
- **Servicios HTTP:** `src/services/api.ts` usa `baseURL` por defecto `'/api'` y un *interceptor* que añade `Authorization: Bearer <token>` desde el store. El interceptor maneja `401` limpiando sesión y redirigiendo a `/login`.
- **Proxy de desarrollo:** `vite.config.js` usa proxy `'/api' -> http://localhost:9000` para evitar CORS en desarrollo. Para producción, configurar `VITE_API_URL`.
- **Formato de login:** La API espera `Content-Type: application/x-www-form-urlencoded` en `/api/auth/token` (no JSON). El frontend lo maneja correctamente.
- **Hot reload:** Vite recarga cambios en caliente; instalar dependencias con `npm install` antes de `npm run dev`.

Usar estas referencias para integrar o extender la UI (roles, permisos, validaciones).