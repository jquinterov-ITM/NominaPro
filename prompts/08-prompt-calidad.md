# Prompt: Documentación de Calidad – NominaPro

## Compatibilidad multiplataforma

Los ejemplos de ejecución de tests y comandos de calidad son multiplataforma. Ejemplo mínimo para crear/activar `venv`:

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
- **Infraestructura**: ejecución local simple

## Objetivo
Generar el archivo `/docs/06-calidad.md` de **NominaPro**.

## Criterio operativo actual
- No se aceptan fallbacks que creen datos en memoria cuando un endpoint falla.
- Si un endpoint no existe, la solución debe ser implementarlo o documentar el bloqueo, no simular el flujo.
- Los tests deben cubrir el flujo real contra la API y la base de datos.

## Instrucciones

Genera un documento de calidad en Markdown que incluya:

### 1. Estrategia de Testing

#### 1.1 Pirámide de Tests
- **Unitarios**: lógica de negocio (`calcularNomina`) y utilitarios.
- **Frontend**: pruebas de componentes con Vitest y `@vue/test-utils`.
- **Integración**: endpoints FastAPI con base de datos de prueba.
- **E2E** (opcional): flujo completo desde UI hacia API.

### 2. Tests del Backend (Python + FastAPI)

#### 2.1 Estructura sugerida
```text
tests/
├── unit/
│   └── test_nomina_service.py
├── integration/
│   ├── test_empleados.py
│   ├── test_novedades.py
│   └── test_nominas.py
└── setup/
	└── test_db.py
```

#### 2.2 Casos obligatorios por módulo
| Módulo     | Happy path                                | Casos de error principales                          |
|------------|--------------------------------------------|-----------------------------------------------------|
| Empleados  | Crear y listar empleado                    | Campos faltantes, documento duplicado               |
| Novedades  | Crear/listar/eliminar novedad por período   | Empleado no existe, período ausente                 |
| Nóminas    | Generar, consultar y eliminar nómina       | Sin período, sin empleados activos, período duplicado |
| Cálculo    | Liquidación correcta con redondeo esperado | Valores inválidos o límites no permitidos           |

#### 2.3 Criterios de aceptación funcional
- Dada una entrada fija, el neto calculado debe ser determinístico.
- La generación de nómina debe poder ejecutarse más de una vez sin duplicados por empleado/período.
- Las respuestas de error deben usar formato estándar.

### 3. Calidad de Código
| Práctica                  | Recomendación                                    |
|---------------------------|--------------------------------------------------|
| Linting                   | Ruff/Flake8 para backend y ESLint para frontend  |
| Formato                   | Black (backend) y Prettier (frontend)            |
| Convención de commits     | `feat:`, `fix:`, `chore:`, `docs:`              |
| Revisión de cambios       | PR con checklist técnico y funcional             |

### 4. Cobertura y Automatización
- Cobertura inicial objetivo: **60%** en servicios críticos.
- Cobertura objetivo intermedio: **80%** en reglas de negocio de nómina.
- Ejecución automática de pruebas antes de merge.

### 5. Comandos Recomendados
Incluye comandos sugeridos (según herramientas elegidas), por ejemplo:
- ejecutar tests unitarios,
- ejecutar tests de integración,
- reporte de cobertura,
- lint y formato.

## Formato de Salida
- Markdown con tablas, checklist y ejemplos de casos de prueba.

## Notas de alineación con el código
- **Tests existentes:** Hay tests unitarios en `tests/unit/test_nomina_service.py` que cubren `liquidar_todos_empleados`.
- **Práctica requerida:** las pruebas de integración deben usar endpoints reales (`/api`) y una DB de pruebas; evitar simulaciones en memoria.
- **Endpoints y validaciones:** documentar en los tests el comportamiento *upsert* de `POST /api/novedades/` y la ausencia de `GET /api/nominas?periodo` si se confía en esa funcionalidad.
