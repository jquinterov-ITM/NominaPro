---
description: workflows y guías de agentes para el proyecto NominaPro
---

# Workflows de NominaPro para Agentes

Compatibilidad multiplataforma: los pasos de arranque funcionan en Windows (PowerShell/CMD), macOS y Linux (bash/zsh). Ejemplo mínimo para crear/activar `venv`:

- PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

- macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Documento operativo para que los agentes ejecuten NominaPro **desde cero**, realicen cambios con bajo riesgo y cierren tareas con trazabilidad.

---

## Flujo maestro obligatorio (orden estricto)

### Paso 1. Cargar contexto base
1.  Leer el skill de contexto del proyecto en `prompts/01-prompt-skill.md`.
2. Revisar `README.md` (arranque y troubleshooting).
3. Revisar `docs/07-implementacion.md` (instalación guiada).

### Paso 2. Preflight de entorno
1. Verificar versiones: Python, pip, Node, npm.
2. Confirmar ubicación en la raíz del proyecto.
3. Confirmar que no hay procesos previos bloqueando puertos 9000/5173.

### Paso 3. Levantar backend primero
1. Crear y activar `.venv`.
2. Instalar `backend/requirements.txt`.
3. Configurar SQLite local (`DATABASE_URL=sqlite:///./nominapro.db`) cuando aplique.
4. Ejecutar:
   - `uvicorn app.main:app --reload --app-dir backend`
5. Validar:
   - `/docs`
   - endpoints principales bajo `/api`.

### Paso 4. Levantar frontend después
1. Entrar a `frontend/`.
2. Ejecutar `npm install`.
3. Ejecutar `npm run dev`.
4. Validar navegación de vistas y comunicación con backend.

### Paso 5. Ejecutar tarea de desarrollo
1. Definir alcance en lote pequeño.
2. Editar solo archivos necesarios.
3. Mantener contratos API o documentar cualquier cambio explícito.
4. Validar funcionalidad afectada.

### Paso 6. Cierre y evidencia
1. Actualizar documentación impactada (`README`, `prompts/*`, `docs/*`).
2. Registrar estado en `TODO.md`.
3. Confirmar criterios de terminado:
   - ejecución local reproducible,
   - flujo mínimo funcional,
   - documentación coherente con el código.

---

## Workflow A – Crear nuevo módulo CRUD backend

**Uso**: agregar un recurso nuevo (ej: centros de costo).

**Pasos**:
1. Crear router en `backend/app/api/{modulo}.py`.
2. Crear/ajustar esquemas en `backend/app/schemas.py` (o archivo equivalente).
3. Crear lógica de negocio en capa de servicio (si aplica).
4. Ajustar modelos/tablas en `backend/app/db/models.py` y sesión según necesidad.
5. Registrar router en `backend/app/main.py` bajo `/api/{modulo}`.
6. Validar casos: éxito, validación inválida, no encontrado.
7. Documentar endpoints y reglas en `docs/backend.md` y `docs/02-funcional.md`.

---
## Workflow B – Ampliar módulo existente

**Uso**: ampliar `empleados`, `novedades`, `nominas`, `parametros`.

**Pasos**:
1. Revisar router actual en `backend/app/api/{modulo}.py`.
2. Revisar modelos/esquemas impactados.
3. Implementar validación de entrada y manejo homogéneo de errores.
4. Probar compatibilidad con frontend existente.
5. Actualizar documentación del módulo.

## Workflow C – Refactor por capas sin romper API

**Uso**: mejorar mantenibilidad sin cambiar contratos.

**Pasos**:
1. Identificar lógica extensa en rutas.
2. Extraer a funciones o servicios reutilizables.
3. Mantener payloads de request/response.
4. Validar endpoints existentes (regresión mínima).
5. Documentar cambios técnicos internos.

## Workflow D – Seguridad incremental

**Uso**: endurecer la API gradualmente.

**Pasos**:
1. Ajustar CORS con whitelist.
2. Definir/ajustar autenticación y autorización por rol.
3. Proteger rutas sensibles.
4. Registrar eventos críticos sin exponer datos sensibles.
5. Actualizar `docs/04-seguridad.md`.

## Workflow E – Validación y pruebas mínimas

**Uso**: cerrar cambios con evidencia.

**Casos mínimos**:
1. Happy path.
2. Validación fallida.
3. Recurso inexistente.
4. Flujo extremo a extremo mínimo:
   - empleado → novedad → liquidación de nómina → consulta.

## Workflow F – Documentación funcional/técnica

**Uso**: al cerrar un lote de cambios.

**Pasos**:
1. Actualizar rutas y ejemplos JSON en `docs/backend.md`.
2. Actualizar guía de ejecución en `docs/07-implementacion.md`/`README.md` si aplica.
3. Verificar consistencia entre prompts y documentación.

---

## Uso recomendado de prompts por objetivo

1. `prompt-skill.md`: contexto base + protocolo desde cero.
2. `prompt-backend.md`: cambios de API y modelo.
3. `prompt-frontend.md`: cambios UI/Vue.
4. `prompt-funcional.md`: reglas de negocio de nómina.
5. `prompt-seguridad.md`: controles y riesgos.
6. `prompt-calidad.md`: validación y estrategia de pruebas.
7. `prompt-implementacion.md`: despliegue/operación.
8. `prompt-arquitectura.md`: decisiones estructurales.

## Regla de oro para agentes

Ningún cambio se considera terminado si no puede ser ejecutado desde cero por otra persona siguiendo la documentación paso a paso.

## Notas de alineación con el código
- **Autenticación:** JWT ya está integrado en `backend/app/core/auth.py` y se usa en dependencias `require_roles` en routers críticos.
- **Novedades:** `POST /api/novedades/` hace upsert por `(empleado_id, periodo)`; no hay endpoint público para filtrar novedades por `empleado_id` y/o `periodo`.
- **Nóminas:** Orquestación en `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve historial completo sin query `periodo` por ahora.
- **Términos:** estandarizar a `tipo_salario` en documentación y prompts.
