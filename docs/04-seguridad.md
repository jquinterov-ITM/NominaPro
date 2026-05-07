# Documentación de Seguridad – NominaPro

## Estado Actual
- CORS configurado por entorno.
- Validaciones uniformes en API con respuestas controladas.
- JWT con expiración y roles para rutas sensibles.
- Secretos y credenciales de demo centralizados en configuración.

## Riesgos Prioritarios
- Acceso no autenticado a endpoints de negocio.
- Manipulación de datos sin trazabilidad de usuario.
- Exposición accidental de información sensible en logs o errores.
- Falta de límites de tasa en endpoints críticos.

## Plan JWT + Roles
### Fase 1
- Login con usuario y clave.
- Emisión de JWT con expiración corta.
- Protección obligatoria de rutas sensibles.

### Fase 2
- Roles aplicados: `RH_ADMIN`, `PAYROLL_USER`.
- Rutas de lectura pública, escritura protegida por rol.

### Fase 3
- Rotación de secretos.
- Revocación básica de sesiones.
- Refresh token opcional.

## Medidas Base
| Medida | Recomendación |
|---|---|
| Validación | Validadores por ruta y manejo uniforme de errores |
| Rate limiting | Aplicar en endpoints sensibles |
| Headers | Middleware o proxy |
| CORS | Lista blanca por entorno |
| Errores | Formato uniforme sin detalles internos |
| Logging | Sin datos sensibles |

## Protección de Datos
- Secretos fuera del código fuente.
- Uso de `.env` por entorno.
- HTTPS obligatorio en producción.
- Respaldo mínimo y restauración documentada.

## Buenas Prácticas Operativas
- Revisar dependencias periódicamente.
- Aplicar mínimo privilegio.
- Ejecutar checklist de seguridad antes de despliegue.

## Verificación Aplicada
- El login emite JWT con expiración y roles.
- Los endpoints de creación y eliminación exigen rol autorizado.
- Los errores de validación y autorización no exponen detalles internos.
- CORS depende de la configuración del entorno.

## Autenticación con Usuarios en BD
- Las credenciales ahora se almacenan en la tabla `usuarios` con contraseñas hasheadas (bcrypt).
- El usuario `admin` se crea automáticamente al iniciar el backend si no existe.
- Credenciales por defecto: `admin` / `secret` (definidas en `.env`).

## Auditoría y Trazabilidad
- Se añadió la tabla `auditoria` y los endpoints `POST /api/auditoria/` y `GET /api/auditoria/` para registrar eventos administrativos.
- Acceso restringido: solamente roles `RH_ADMIN` pueden invocar estos endpoints.
- Recomendación: registrar `usuario_id`, `accion`, `detalle`, `fecha` y considerar en próximas versiones `valor_anterior` y `valor_nuevo` para cambios críticos (salarios, estado de nómina).

## Notas de alineación con el código
- **JWT + Usuarios BD:** El código implementa JWT en `backend/app/core/auth.py` consultando usuarios en la tabla `usuarios`. Las contraseñas se verifican con bcrypt.
- **Pruebas:** Para probar endpoints protegidos, obtener token en `POST /api/auth/token` usando credenciales de la tabla `usuarios` (por defecto: admin/secret).
- **Upsert y unicidad:** `POST /api/novedades/` realiza upsert por `(empleado_id, periodo)`; las pruebas de seguridad deben incluir escenarios de intento de duplicación y validación de permisos.
