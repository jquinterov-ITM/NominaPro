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

## Notas de alineación con el código
- **JWT en el repo:** El código implementa JWT demo en `backend/app/core/auth.py` y las rutas usan la dependencia `require_roles` para control de acceso.
- **Pruebas:** Para probar endpoints protegidos, obtener token en `POST /api/auth/token` usando credenciales demo según `config`.
- **Upsert y unicidad:** `POST /api/novedades/` realiza upsert por `(empleado_id, periodo)`; las pruebas de seguridad deben incluir escenarios de intento de duplicación y validación de permisos.