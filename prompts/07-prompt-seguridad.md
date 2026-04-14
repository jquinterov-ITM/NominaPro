# Prompt: Documentación de Seguridad – NominaPro

## Compatibilidad multiplataforma

Los comandos de ejemplo y procedimientos de este prompt son válidos en Windows (PowerShell/CMD), macOS y Linux. Ejemplo mínimo para `venv`:

PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

CMD:
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

macOS / Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```

## Contexto del Proyecto
- **Nombre**: NominaPro
- **Frontend**: Vue.js
- **Backend**: Python + FastAPI
- **Base de datos**: SQLite (Desarrollo Local) / PostgreSQL con psycopg[binary] (Producción)
- **Estado actual**: autenticación JWT de prueba integrada y controles base de API

## Objetivo
Generar el archivo `/docs/04-seguridad.md` de **NominaPro** con enfoque incremental y realista para la versión actual.

## Instrucciones

Genera un documento de seguridad en Markdown que incluya:

### 1. Estado Actual
- Inventario de controles existentes (CORS básico, validaciones mínimas, errores 500).
- Superficie de ataque de la API actual.

### 2. Riesgos Prioritarios
- Acceso no autenticado a endpoints de negocio.
- Manipulación de datos de nómina sin trazabilidad de usuario.
- Falta de límites de tasa para abuso de endpoints.
- Exposición accidental de información sensible en mensajes/logs.

### 3. Plan de Autenticación y Autorización (JWT + Roles)

#### 3.1 Fase 1 – Fundaciones (R11)
- Login con usuario/clave (o integración futura con proveedor externo).
- Emisión de JWT con expiración corta.
- Autenticación obligatoria con JWT usando `Security` de FastAPI.
- Exigir roles estandarizados para uso de endpoints: `RH_ADMIN` (para crear empleados) y `PAYROLL_USER` (para generar nóminas).
- Middleware de verificación de log/token auditable.

#### 3.2 Fase 2 – Roles
- Roles sugeridos: `admin`, `analista_nomina`, `consulta`.
- Matriz de permisos por endpoint.

#### 3.3 Fase 3 – Hardening
- Rotación de secretos.
- Refresh token (opcional).
- Revocación básica de sesiones.

### 4. Seguridad de API y Aplicación
| Medida                    | Recomendación para NominaPro                          |
|---------------------------|--------------------------------------------------------|
| Validación de entrada     | Validadores por ruta + tipos/rangos obligatorios       |
| Rate limiting             | `slowapi` o equivalente en endpoints sensibles         |
| Headers de seguridad      | middlewares de seguridad (`starlette`/proxy)           |
| CORS                      | Lista blanca por entorno (dev/prod)                    |
| Manejo de errores         | Respuesta estandarizada sin revelar detalles internos  |
| Logging                   | Registrar eventos sin datos sensibles                   |

### 5. Protección de Datos
- Definir política mínima de respaldo de datos: copia del archivo `nominapro.db` en desarrollo local (SQLite); dump, retención y restauración en producción (PostgreSQL).
- Evitar almacenar secretos en código fuente.
- Uso de `.env` por entorno.
- Cifrado en tránsito (HTTPS) obligatorio en producción.

### 6. Buenas Prácticas Operativas
- Actualización periódica de dependencias (`pip-audit`/`safety`).
- Checklist de seguridad antes de despliegue.
- Revisión de permisos y principio de mínimo privilegio.

## Formato de Salida
- Markdown con tablas, checklist y roadmap por fases.

## Notas de alineación con el código
- **JWT presente:** El código ya implementa JWT demo y validación por roles (`require_roles`) en routers; actualizar el prompt para trabajar con tokens de prueba en desarrollo.
- **EndPoints críticos:** `POST /api/empleados/` (creación con validaciones), `POST /api/novedades/` (upsert), `POST /api/nominas/liquidar`.
- **Recomendación:** Probar con credenciales demo definidas en `backend/app/core/config.py` y documentar pasos de obtención de token en `docs/07-implementacion.md`.
