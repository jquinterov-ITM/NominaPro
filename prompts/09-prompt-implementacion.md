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
- `DATABASE_URL` (cadena de conexión: SQLite en desarrollo local, PostgreSQL en producción)

Incluye ejemplo de `.env`:
```env
PORT=9000
# Desarrollo local (SQLite, sin instalar nada extra):
DATABASE_URL=sqlite:///./nominapro.db
# Producción (PostgreSQL):
# DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/nominapro
```

Nota: copia `.env.example` a `.env` y no subas el archivo `.env` al repositorio. Si vas a usar migraciones en entornos nuevos, agrega `alembic` a `backend/requirements.txt` y aplica las migraciones con `python -m alembic -c backend/alembic.ini upgrade head` antes de arrancar la API.

#### 3.2 Instalación y ejecución
Sigue estos pasos según tu sistema operativo. Se asume `python` apunta a Python 3.11+.

Windows (PowerShell):
```powershell
python -m venv .venv
# activar el entorno (nota: puede requerir permitir scripts para la sesión)
# si la activación falla por políticas: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
# Ejecutar la API usando el intérprete activo
python -m uvicorn app.main:app --reload --app-dir backend
```

Windows (CMD):
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --reload --app-dir backend
```

macOS / Linux (bash / zsh):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --reload --app-dir backend
```

Variables de entorno (ejemplos por plataforma):

PowerShell:
```powershell
$env:PORT = "9000"
$env:DATABASE_URL = "sqlite:///./nominapro.db"
```

CMD:
```cmd
set PORT=9000
set DATABASE_URL=sqlite:///./nominapro.db
```

bash / macOS / Linux:
```bash
export PORT=9000
export DATABASE_URL=sqlite:///./nominapro.db
```

Frontend (Node.js / Vite):
```bash
# Requiere Node.js 18+ (recomendado)
cd frontend
npm install
npm run dev
# Abre http://localhost:5173
```

Ejecutar pruebas backend (tras activar el venv):
```bash
pip install -r backend/requirements.txt
# ejecutar pytest desde la raíz del proyecto
pytest -q
```

Notas rápidas:
- Para asegurar que `uvicorn` se ejecute desde el entorno virtual usa `python -m uvicorn ...`.
- En PowerShell la activación es `\\.venv\\Scripts\\Activate.ps1`; si da error, ejecuta la línea de `Set-ExecutionPolicy` indicada arriba para la sesión actual.
- Si usas WSL en Windows, sigue las instrucciones de macOS/Linux dentro de la distro.

### 4. Verificación de Arranque
- Health check: `GET /health`.
- Frontend: `http://localhost:5173`.
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
- Base de datos no disponible: verificar que `DATABASE_URL` apunte a SQLite (local) o a PostgreSQL válido (producción). En local, basta con `sqlite:///./nominapro.db`.
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

## Cambios recientes (resumen)

- `.env.example` añadido y recomendación de usar variables de entorno para configuración y secretos.
- Alembic configurado en `backend/alembic/` con migración inicial; ver `docs/07-implementacion.md` para pasos reproducibles.
- `scripts/get_token.py` proporciona una forma rápida de generar JWTs de prueba; también existe `demo_api.ps1` para demostraciones interactivas.
- Ejecuta `pre-commit run --all-files` tras instalar dependencias para aplicar formato e import fixes antes de commits.

Estos cambios buscan que la implementación desde cero sea reproducible y segura en cualquier entorno de desarrollo.
