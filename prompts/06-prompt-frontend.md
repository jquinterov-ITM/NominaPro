# Prompt: Frontend – Vue.js para NominaPro

## Compatibilidad multiplataforma

Los comandos de arranque y pruebas son multiplataforma. Crear/activar `venv`:

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
- **Enfoque**: sistema educativo de nómina con evolución incremental hacia cumplimiento 2026

## Objetivo
Generar el archivo `/docs/03-frontend.md` de **NominaPro** con lineamientos de implementación y calidad para la interfaz de usuario.

## Instrucciones

Genera un documento en Markdown que incluya:

### 1. Arquitectura Frontend
- Estructura base de una SPA en Vue.
- Organización sugerida: `views`, `components`, `stores`, `services`.
- Estrategia de consumo API (`/api`) y manejo de errores.

### 2. Diseño de Módulos UI
- Empleados: alta, listado y validaciones.
- Novedades: registro por período (`YYYY-MM`) y edición.
- Nóminas: generación mensual y consulta por período.
- Estado visual de proceso: cargando, éxito, error y vacíos.

### 3. Validaciones y UX
- Validación de formularios en cliente con reglas mínimas.
- Reglas de consistencia con backend (tipos, rangos, obligatorios).
- Mensajes de error claros y accionables.

### 4. Seguridad Frontend
- Manejo de token JWT (si aplica en fases posteriores).
- Protección de rutas por rol.
- No exponer secretos en cliente.
 - Recomendación práctica: en desarrollo el script `scripts/get_token.py` puede facilitar pruebas, pero en producción evita `localStorage` para tokens; prefiere HttpOnly cookies o flujo de refresh tokens seguro.

### 5. Calidad Frontend
- Pruebas unitarias de componentes críticos (Vitest + Vue Test Utils).
- Pruebas de integración de flujo mensual.
- Reporte de cobertura mínima.
- Linting y formato.

### 6. Roadmap de Evolución
- Fase 1: MVP de operación mensual.
- Fase 2: mejoras de experiencia y validaciones avanzadas.
- Fase 3: soporte para estados de nómina electrónica y trazabilidad.

## Formato de Salida
- Markdown estructurado con secciones, tablas y checklist de implementación.

## Notas de alineación con el código
- **Autenticación:** El backend ya utiliza JWT (ver `backend/app/core/auth.py`); el frontend debe manejar tokens y roles (`RH_ADMIN`, `PAYROLL_USER`).
- **Endpoints:** El endpoint para liquidar es `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve historial completo y `GET /api/nominas/{id}` existe. No hay `GET /api/nominas?periodo=...` implementado actualmente.
- **Novedades:** `POST /api/novedades/` hace upsert por `(empleado_id, periodo)`; no hay endpoint público para listar por `empleado_id` y/o `periodo`.
 - **Endpoints:** El endpoint para liquidar es `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve historial y `GET /api/nominas/{id}` existe. La API soporta ahora `GET /api/nominas?periodo=YYYY-MM` para filtrar por período.
 - **Novedades:** `POST /api/novedades/` hace upsert por `(empleado_id, periodo)`; `GET /api/novedades/` soporta filtros `?empleado_id=` y `?periodo=` para consultas acotadas.
- **Términos sincronizados:** usar `tipo_salario` en formularios y validaciones del frontend.
 - **Términos sincronizados:** usar `tipo_salario` en formularios y validaciones del frontend.

## Pruebas Frontend existentes
- El frontend usa `vitest` (ver `frontend/package.json`) y contiene pruebas de componentes en `frontend/src/__tests__/` (Ej.: `EmpleadosView.spec.js`, `HomeView.spec.js`). Añadir cobertura e integración E2E según roadmap.

## Cambios recientes (resumen)

- Se añadió `scripts/get_token.py` para generar tokens de prueba desde la CLI; los ejemplos en `docs/07-implementacion.md` muestran cómo obtener token desde consola.
- Recomendado: evitar almacenar tokens en `localStorage` en producción; considerar HttpOnly cookies/refresh-token seguro.
- `pre-commit` y formateo aplicado al frontend/backend para mantener consistencia, y se agregó un workflow CI inicial.

Verifica que el `VITE_API_URL` o el proxy de Vite apunten al backend correcto tras aplicar migraciones o cambiar `DATABASE_URL`.
