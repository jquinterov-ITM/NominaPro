# TODO.md - Ejecución Prompts NominaPro (Progreso)

## 1. Base ya completada

- [x] Crear documentación base en `/docs/`.
- [x] Implementar `backend/app/services/nomina_service.py`.
- [x] Ajustar `backend/app/repositories/nomina_repository.py` para persistencia.
- [x] Actualizar `api/nominas.py` para usar `service` directamente.
- [x] Mantener el README de arranque y uso local actualizado.

## 2. Lo que falta para cerrar alineación con prompts y README

### 2.1 Documentación pendiente

- [x] Crear `docs/3. frontend.md`.
- [x] Crear `docs/4. seguridad.md`.
- [x] Crear `docs/5. quality.md`.
- [x] Crear o actualizar `docs/implementacion.md`.
- [x] Revisar que `README.md` y `TODO.md` usen el mismo flujo de arranque.

### 2.2 Backend y dominio

- [x] Normalizar validación de salario integral con `ParametrosLegales` y `SMMLV`.
- [x] Unificar la regla de negocio entre `schemas.py` y `api/empleados.py`.
- [x] Confirmar contrato final entre router, service y repository.
- [x] Revisar cálculo de IBC, FSP, prestaciones y reglas 2026 contra el dominio esperado.
- [x] Verificar unicidad por `(empleado_id, periodo)` en novedades y nóminas.
- [x] Migrar constantes de ley a base de datos dinámica.

	- Nota: el service ya calcula horas extra con valor hora base, incapacidades como deducción, FSP, auxilio de transporte y provisiones de ordinarios.

### 2.3 Seguridad

- [x] Implementar JWT real con expiración y roles.
- [x] Definir permisos para `RH_ADMIN`, `PAYROLL_USER` y consulta.
- [x] Restringir CORS por entorno.
- [x] Agregar manejo uniforme de errores sin exponer detalles internos.
- [x] Dejar secretos y variables sensibles fuera del código fuente.

### 2.4 Frontend

- [x] Validar formularios en cliente para empleados, novedades y nóminas.
- [x] Mostrar estados de carga, vacío, éxito y error.
- [x] Conectar las acciones de eliminar contra DELETE real.
- [x] Preparar manejo de token si el login deja de ser demo.
- [x] Revisar UX de mensajes de 400 y 422.

### 2.5 Calidad y pruebas

- [x] Crear pruebas unitarias para `nomina_service`.
- [x] Crear pruebas unitarias y de componentes para el frontend (Vitest).
- [x] Crear pruebas de integración para empleados, novedades y nóminas.
- [x] Definir casos felices y casos de error por módulo.
- [x] Añadir verificación de cobertura mínima en servicios críticos.
- [x] Ejecutar lint y formato antes de cerrar cambios.

### 2.6 Implementación y verificación

- [x] Documentar comandos de arranque para Windows.
- [x] Documentar troubleshooting de puerto ocupado y `WinError 10013`.
- [x] Incluir flujo manual de prueba desde UI hasta API.
- [x] Dejar ejemplos de request y response en la documentación.

## 3. Prioridad sugerida

1. Normalizar validación de salario integral y contrato router/service/repository.
2. Cerrar seguridad JWT + roles.
3. Completar pruebas unitarias e integración.
4. Completar documentación faltante en `docs/`.
5. Mejorar validaciones y UX del frontend.

## 4. Estado actual resumido

- Services: `backend/app/services/nomina_service.py` implementado.
- Repositories: `backend/app/repositories/nomina_repository.py` implementado.
- API: rutas principales operativas.
- README: arranque local documentado con notas para Windows.

## 5. Siguiente paso natural

- [x] Cerrar la documentación pendiente de frontend, seguridad, calidad e implementación.
- [x] Luego pasar a seguridad y pruebas automatizadas.

## 6. Cierre formal

- La documentación operativa quedó alineada con el comportamiento actual del sistema.
- Las pruebas unitarias e integración quedaron ejecutadas y validadas.
- La cobertura crítica del service principal quedó por encima del umbral definido.
- El siguiente avance queda reservado para evolución funcional, no para cierre de pendientes.
