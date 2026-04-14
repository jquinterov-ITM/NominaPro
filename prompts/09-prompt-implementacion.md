# Prompt: Documentación de Implementación – NominaPro

## Compatibilidad multiplataforma

Los pasos de instalación y arranque de este prompt están diseñados para funcionar en Windows (PowerShell/CMD) y macOS/Linux. Ejemplo mínimo:

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
- **Infraestructura**: ejecución local (sin contenedores obligatorios)

## Objetivo
Generar el archivo `/docs/07-implementacion.md` de **NominaPro**.

## Estado actual del punto 1
- El frontend ya no debe depender de datos simulados.
- Los botones de eliminar empleados y novedades deben llamar a DELETE real.
- La nómina debe cargarse y liquidarse sólo desde el backend FastAPI.

## Instrucciones

Genera un documento de implementación en Markdown que incluya:

### 1. Requisitos Previos
- Python 3.11+ y `pip`.
- Git.
- Sistema operativo compatible (Windows/Linux/macOS).

### 2. Estructura del Proyecto
```text
NominaPro/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── services/
│   │   └── db/
│   └── requirements.txt
├── frontend/
│   └── src/
├── docs/
├── prompts/
└── README.md
```

### 3. Configuración Inicial

#### 3.1 Variables de entorno
Documenta variables mínimas como:
- `PORT` (puerto del servidor)
- `DATABASE_URL` (cadena de conexión a PostgreSQL)

Incluye ejemplo de `.env`:
```env
PORT=3000
DATABASE_URL=sqlite:///./nominapro.db (Local) / postgresql+psycopg:// (Prod)postgres:postgres@localhost:5432/nominapro
```

#### 3.2 Instalación y ejecución
```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

### 4. Verificación de Arranque
- Health check: `GET /health`.
- Frontend: `http://localhost:3000`.
- API: rutas bajo `/api`.

### 5. Flujo de Prueba Manual
- Crear empleado.
- Registrar novedades del período.
- Generar nómina mensual.
- Consultar nóminas por período.
- Eliminar empleado y novedad desde la UI para validar los nuevos endpoints.

Incluye ejemplos de requests/responses JSON para cada paso.

### 6. Comandos Útiles
| Comando         | Descripción                          |
|-----------------|--------------------------------------|
| `pip install -r backend/requirements.txt` | Instala dependencias backend |
| `uvicorn app.main:app --reload --app-dir backend` | Inicia API en desarrollo |
| `pytest` | Ejecuta pruebas backend |

### 7. Troubleshooting
- Puerto ocupado.
- PostgreSQL no disponible o credenciales inválidas en `DATABASE_URL`.
- Errores por datos inválidos o faltantes en requests.

## Formato de Salida
- Markdown con pasos numerados, comandos bash y tablas de referencia.


## Progreso de Implementación Consolidado
- Las carpetas /frontend y /backend han sido correctamente inicializadas.
- Vistas de Vue.js operativas y con ciclo de pruebas cerrado (Vitest).
- Backend refactorizado con patrón Repository/Service y parámetros legales dinámicos (R12 avanzado).
- Integración de cors en main.py de FastAPI para comunicación al puerto de Vite (5173).
- Sistema base operante: Empleados creados exitosamente salvaguardando inconsistencias de datos.
- Cobertura de pruebas crítica validada al 100%.

## Notas de alineación con el código
- **Endpoints reales y pruebas:** usar `POST /api/nominas/liquidar` para generación; documentar tokens JWT de demo para pruebas automatizadas.
- **Novedades:** `POST /api/novedades/` realiza upsert; los tests de integración deben crear/limpiar datos para evitar conflictos por unique constraints `(empleado_id, periodo)`.
- **Filtros en API:** si la implementación del frontend necesita `GET /api/nominas?periodo=...` o `GET /api/novedades?empleado_id=...`, se deberán añadir esos filtros en los routers o implementar endpoints dedicados.
