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
- **Términos sincronizados:** usar `tipo_salario` en formularios y validaciones del frontend.
