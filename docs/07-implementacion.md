
# Documentación de Implementación – NominaPro

## 1. Requisitos Previos
- Python 3.11+
- pip y Git
- Node.js 18+
- Windows, Linux o macOS

## 2. Estructura del Proyecto
```text
NominaPro/
├── backend/
├── frontend/
├── docs/
├── prompts/
└── README.md
```

## 3. Configuración Inicial


### 3.1. Crear y activar entorno virtual

**Windows PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```


### 3.2. Instalar dependencias backend

**Windows PowerShell / CMD:**
```powershell
pip install -r backend/requirements.txt
```

**macOS / Linux:**
```bash
pip install -r backend/requirements.txt
```


## 4. Migraciones de Base de Datos (Alembic)
Debes ejecutar ese comando de migración con Alembic en estos casos principales:

1. La primera vez que configuras el proyecto en tu máquina, para crear todas las tablas necesarias en la base de datos.
2. Cada vez que el código del backend recibe nuevas migraciones (por ejemplo, si alguien del equipo agrega o modifica modelos y crea un nuevo archivo de migración en `backend/app/db/migrations/`), para actualizar la estructura de la base de datos con esos cambios.
3. Después de hacer un pull o actualizar tu repositorio y ves que hay cambios en las migraciones.
4. Cuando tú mismo generas una nueva migración (por ejemplo, tras modificar modelos y ejecutar alembic revision --autogenerate).
No es necesario ejecutarlo todos los días ni cada vez que inicias el backend, solo cuando hay cambios en la estructura de la base de datos (nuevas migraciones).

Notas:
- Activa el virtualenv antes de ejecutar `alembic`.
- Puedes ejecutar el comando desde la raíz del repositorio o desde `backend/` (usa `alembic -c alembic.ini upgrade head`).
- En Windows PowerShell, si tienes problemas con PATH, usa `python -m alembic -c backend\\alembic.ini upgrade head`.


**Windows PowerShell:**
```powershell
# Desde la raíz del repositorio (asegúrate de que el venv esté activado y 'alembic' en PATH):
alembic -c backend/alembic.ini upgrade head
# Alternativa si alembic no está en PATH dentro del venv:
python -m alembic -c backend/alembic.ini upgrade head
```

**Windows CMD:**
```cmd
alembic -c backend\alembic.ini upgrade head
python -m alembic -c backend\alembic.ini upgrade head
```

**macOS / Linux:**
```bash
# Desde la raíz del repositorio (asegúrate de que el venv esté activado y 'alembic' en PATH):
alembic -c backend/alembic.ini upgrade head
# Alternativa si alembic no está en PATH dentro del venv:
python3 -m alembic -c backend/alembic.ini upgrade head
```


## 5. Formateo y calidad de código (opcional)
```powershell
pre-commit install
pre-commit run --all-files
```


## 6. Arranque del Backend

**Windows PowerShell:**
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 9000 --reload
```

**Windows CMD:**
```cmd
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 9000 --reload
```

**macOS / Linux:**
```bash
cd backend
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 9000 --reload
```

Nota: Para desarrollo puedes añadir `--reload`. En algunas máquinas Windows `--reload` puede causar `WinError 10013`; si ocurre, quita `--reload`.


## 7. Arranque del Frontend

Abre una nueva terminal y desde la carpeta `frontend`:

**Windows PowerShell / CMD / macOS / Linux:**
```bash
cd frontend
npm install
npm run dev
```
Accede a: http://localhost:5173

Notas y ajustes reales del proyecto:

- El frontend está implementado con Vite + Vue 3 y requiere `@vitejs/plugin-vue` y `typescript` en `devDependencies`. Si el servidor Vite muestra errores sobre `.vue` al iniciar, ejecutar `npm install` en `frontend` para asegurar que las dependencias estén instaladas.
- Durante desarrollo el proxy está configurado en `vite.config.js` para reenviar `'/api'` a `http://localhost:9000`. El cliente usa `baseURL` por defecto `'/api'`. Para apuntar a otro backend en tiempo de ejecución, usar la variable de entorno `VITE_API_URL`.



## 8. Pruebas
### Backend

**Windows PowerShell:**
```powershell
pytest -q
pytest --cov=backend.app.services.nomina_service --cov-report=term-missing --cov-fail-under=90
```
Si `pytest` no se encuentra, activa el entorno virtual y ejecuta:
```powershell
pip install pytest
# o instala todas las dependencias del backend:
pip install -r backend/requirements.txt
```

**Windows CMD:**
```cmd
pytest -q
pytest --cov=backend.app.services.nomina_service --cov-report=term-missing --cov-fail-under=90
```
Si `pytest` no se encuentra, activa el entorno virtual y ejecuta:
```cmd
pip install pytest
pip install -r backend\requirements.txt
```

**macOS / Linux:**
```bash
pytest -q
pytest --cov=backend.app.services.nomina_service --cov-report=term-missing --cov-fail-under=90
```
Si `pytest` no se encuentra, activa el entorno virtual y ejecuta:
```bash
pip install pytest
pip install -r backend/requirements.txt
```

### Frontend

**Windows PowerShell / CMD / macOS / Linux:**
```bash
cd frontend
npm run build
```

Nota: actualmente `frontend/package.json` no define script `test`; los scripts disponibles son `dev`, `build` y `preview`.


## 9. Scripts y verificación rápida

En la raíz del proyecto hay scripts para probar la API automáticamente:

**Windows PowerShell:**
```powershell
./demo_api.ps1
```

**Windows CMD:**
```cmd
powershell -ExecutionPolicy Bypass -File demo_api.ps1
```

**macOS / Linux:**
```bash
chmod +x demo_api.sh
./demo_api.sh
```

> Estos scripts hacen llamadas demo a la API (login, crear empleado, liquidar nómina, etc.) y muestran la respuesta en consola.

Documentación interactiva de la API (Swagger): http://127.0.0.1:9000/docs

## 10. Ejemplos de uso y endpoints


### Flujo de verificación manual (API)

#### 1. Obtener token de autenticación

**Windows PowerShell:**
```powershell
$res = Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/auth/token" -Method Post -Body @{username="admin"; password="secret"}
$headers = @{Authorization = "Bearer $($res.access_token)"}
```

**Windows CMD:**
```cmd
curl -X POST http://127.0.0.1:9000/api/auth/token -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=secret"
:: Copia el access_token del resultado para usarlo en los siguientes pasos
```

**macOS / Linux:**
```bash
curl -X POST http://127.0.0.1:9000/api/auth/token -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=secret"
# Copia el access_token del resultado para usarlo en los siguientes pasos
```

#### 2. Crear Empleado

**Windows PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/empleados/" -Method Post -Headers $headers -Body (@{nombre="Test"; documento="123"; salario_base=1500000; tipo_salario="ORDINARIO"} | ConvertTo-Json) -ContentType "application/json"
```

**Windows CMD:**
```cmd
curl -X POST http://127.0.0.1:9000/api/empleados/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"nombre\":\"Test\",\"documento\":\"123\",\"salario_base\":1500000,\"tipo_salario\":\"ORDINARIO\"}"
```

**macOS / Linux:**
```bash
curl -X POST http://127.0.0.1:9000/api/empleados/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"nombre":"Test","documento":"123","salario_base":1500000,"tipo_salario":"ORDINARIO"}'
```

#### 3. Liquidar Nómina

**Windows PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/nominas/liquidar" -Method Post -Headers $headers -Body (@{periodo="2026-01"} | ConvertTo-Json) -ContentType "application/json"
```

**Windows CMD:**
```cmd
curl -X POST http://127.0.0.1:9000/api/nominas/liquidar -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"periodo\":\"2026-01\"}"
```

**macOS / Linux:**
```bash
curl -X POST http://127.0.0.1:9000/api/nominas/liquidar -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"periodo":"2026-01"}'
```

> [!TIP]
> - Si el puerto 9000 está ocupado, cambia el puerto con `--port 9001`.
> - Si aparece `WinError 10013`, arranca sin `--reload`.
> - Si el frontend no levanta, verifica `npm install` y que el backend siga en ejecución.
> - Si falta el token, genera uno con el login demo antes de llamar rutas protegidas.

### Ejemplos de Request y Response
#### Crear empleado
```http
POST /api/empleados/
Authorization: Bearer <token>
Content-Type: application/json

{
	"nombre": "Ana Perez",
	"documento": "123456789",
	"salario_base": "1500000",
	"tipo_salario": "ORDINARIO"
}
```

#### Registrar novedad
```http
POST /api/novedades/
Authorization: Bearer <token>
Content-Type: application/json

{
	"empleado_id": 1,
	"periodo": "2030-02",
	"tipo": "BONIFICACION",
	"valor": "50000"
}
```

#### Liquidar nómina
```http
POST /api/nominas/liquidar
Authorization: Bearer <token>
Content-Type: application/json

{
	"periodo": "2030-01"
}
```

Respuestas esperadas:
- `201` cuando la liquidación genera nóminas nuevas.
- `400` cuando el período ya fue liquidado.
- `422` cuando el payload no cumple el esquema.

## 11. Modo demo y validaciones
- Usuario: `admin`
- Clave: `secret`
- Roles: `RH_ADMIN`, `PAYROLL_USER`
- El formulario de inicio de sesión está en la portada; al entrar correctamente, la barra superior deja de mostrar `Invitado`.
- El módulo de empleados en frontend permite crear, listar y eliminar (con confirmación) usando los endpoints protegidos de `/api/empleados/`.

## 12. Notas adicionales y solución de problemas
- Health check: `GET /health` — devuelve `200 OK` con `{ "status": "ok" }` cuando la API está operativa.
- API Docs (Swagger): [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs)
- Frontend: [http://localhost:5173](http://localhost:5173)
- **Token demo y autenticación:** El endpoint `POST /api/auth/token` devuelve JWT de prueba; úsalo en `Authorization: Bearer <token>` para rutas protegidas en los ejemplos de esta guía.
- **Upsert de novedades:** `POST /api/novedades/` implementa *upsert* por `(empleado_id, periodo)`; los scripts de demostración y pruebas deben manejar la posibilidad de actualización en lugar de creación duplicada.
- **Nóminas:** Orquestación en `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve el historial y ahora soporta filtro por periodo `?periodo=YYYY-MM`.
- **Modelos:** `ParametrosLegales`, `Empleado`, `Novedad`, `Nomina` están implementados en `backend/app/db/models.py` y los esquemas en `backend/app/schemas.py`.
- **Filtros implementados:** `GET /api/nominas?periodo=YYYY-MM` y `GET /api/novedades?empleado_id=&periodo=` ya están disponibles en los routers; preferir uso de filtros desde el frontend para eficiencia.
- **Auditoría:** Se añadieron endpoints `POST /api/auditoria/` y `GET /api/auditoria/` para trazabilidad administrativa (acceso `RH_ADMIN`).

## 13. Evolución: Parámetros Dinámicos
Se ha implementado la migración de constantes legales de código a base de datos.
- Tabla: `parametros_legales`
- Campos dinámicos: salud, pensión, FSP, recargos, provisión prima/cesantía/int/vac.
- Migración: Automática en el arranque mediante `session.py`.

## 14. Cierre Formal
- Alcance cubierto: backend, frontend, seguridad, calidad y documentación operativa.
- Validación final: pruebas unitarias e integración ejecutadas con resultado satisfactorio.
- Cobertura crítica: `backend.app.services.nomina_service` validada localmente en pruebas específicas; ejecutar la suite completa para verificar la cobertura global.
- Nota: ejecutar `pip install pytest` en el entorno virtual si `pytest` no está instalado.
- Estado de entrega: proyecto listo para uso local y para seguimiento evolutivo.

## Migraciones, Alembic y pasos reproducibles desde cero

Estos pasos aseguran que puedas preparar la base de datos, ejecutar migraciones y verificar la aplicación en una máquina limpia.

1) Crear y activar entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```



2) Copiar archivo de ejemplo de variables y editar según entorno

```powershell
Copy-Item .env.example .env
```

3) Aplicar migraciones con Alembic

```powershell
# Desde la raíz del repositorio (asegúrate de que el venv esté activado y 'alembic' en PATH):
alembic -c backend/alembic.ini upgrade head
# Alternativa si alembic no está en PATH dentro del venv:
python -m alembic -c backend/alembic.ini upgrade head
```

Notas adicionales:
- Activa el virtualenv antes de ejecutar `alembic`.
- Puedes ejecutar el comando desde la raíz del repositorio o desde `backend/` (si estás en `backend/` usa `alembic -c alembic.ini upgrade head`).
- En Windows PowerShell, si tienes problemas con PATH, usa `python -m alembic -c backend\\alembic.ini upgrade head`.

5) Ejecutar pre-commit y formateo inicial (opcional pero recomendado)

```powershell
pre-commit install
pre-commit run --all-files
```

6) Iniciar la API y comprobar (puerto 9000 por defecto)

```powershell
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 9000
```

7) Pruebas y verificación

```powershell
pytest -q
```
si saca error de pytest no encontrado, instala pytest en el entorno virtual:

```powershell
pip install pytest
pip install httpx
pytest -q
```





---
### ¿Para qué sirve el token y cómo se usa?

El **token** (JWT) es una llave digital que te identifica y te da permisos para acceder a las rutas protegidas de la API.

- Cuando te logueas (ya sea desde el frontend o usando el endpoint `/api/auth/token`), el backend te entrega un token.
- Si usas el sistema desde el navegador (frontend), el token se guarda y se envía automáticamente en cada petición: ¡no tienes que hacer nada!
- Si quieres probar la API manualmente (con curl, Postman, PowerShell, etc.), debes copiar el token y ponerlo en el header:

```
Authorization: Bearer <token>
```

en cada petición protegida (por ejemplo, crear empleado, liquidar nómina, etc.).

**Resumen:**
- El token es tu “pase de acceso” a la API.
- Si entras por el frontend, todo es automático.
- Si haces pruebas manuales, copia el token y úsalo en las peticiones protegidas.

**Ejemplo de uso manual con curl:**

```bash
curl -X POST http://127.0.0.1:9000/api/empleados/ \
	-H "Authorization: Bearer <token>" \
	-H "Content-Type: application/json" \
	-d '{"nombre":"Test","documento":"123","salario_base":1500000,"tipo_salario":"ORDINARIO"}'
```

---

8) Obtener token de prueba (multiplataforma)

**Opción 1: Consola interactiva de Python**

1. Activa el entorno virtual:
		- **Windows PowerShell:**
			```powershell
			.\.venv\Scripts\Activate.ps1
			```
		- **Windows CMD:**
			```cmd
			.venv\Scripts\activate.bat
			```
		- **macOS / Linux:**
			```bash
			source .venv/bin/activate
			```
2. Inicia Python en la terminal:
		```powershell
		python
		```
3. Escribe y ejecuta línea por línea:
		```python
		from backend.app.core.auth import create_access_token
		print(create_access_token({"sub": "admin", "roles": ["RH_ADMIN"]}))
		```
		Presiona Enter y verás el token generado.

**Opción 2: Script Python**

1. Crea un archivo llamado `generar_token.py` en la raíz del proyecto con este contenido:
		```python
		from backend.app.core.auth import create_access_token
		print(create_access_token({"sub": "admin", "roles": ["RH_ADMIN"]}))
		```
2. Ejecuta el script desde la terminal:
		- **Windows PowerShell / CMD:**
			```powershell
			python generar_token.py
			```
		- **macOS / Linux:**
			```bash
			python3 generar_token.py
			```
		El token se mostrará en pantalla.

 ### Modo demo
 - Usuario: `admin`
 - Clave: `secret`
 - Roles: `RH_ADMIN`, `PAYROLL_USER`
 - El formulario de inicio de sesión está en la portada; al entrar correctamente, la barra superior deja de mostrar `Invitado`.




## Verificación de Arranque y Troubleshooting (multiplataforma)
- **Health check:**
	- Puedes probar la API con tu navegador o terminal:
		- **PowerShell:**
			```powershell
			Invoke-RestMethod -Uri "http://127.0.0.1:9000/health"
			```
		- **CMD / macOS / Linux:**
			```bash
			curl http://127.0.0.1:9000/health
			```
		- Espera respuesta: `{ "status": "ok" }`
- **API Docs (Swagger):** [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs)
- **Frontend:** [http://localhost:5173](http://localhost:5173)


## Flujo de Verificación Manual (API) multiplataforma
Para verificar el funcionamiento core desde la terminal:

### 1. Autenticación

- **Windows PowerShell:**
	```powershell
	$res = Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/auth/token" -Method Post -Body @{username="admin"; password="secret"}
	$headers = @{Authorization = "Bearer $($res.access_token)"}
	```
- **Windows CMD:**
	```cmd
	curl -X POST http://127.0.0.1:9000/api/auth/token -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=secret"
	:: Copia el access_token del resultado para usarlo en los siguientes pasos
	```
- **macOS / Linux:**
	```bash
	curl -X POST http://127.0.0.1:9000/api/auth/token -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=secret"
	# Copia el access_token del resultado para usarlo en los siguientes pasos
	```

Notas de integración con frontend:

- El frontend envía la petición de login con `application/x-www-form-urlencoded` (no JSON). Si implementas clientes adicionales, respeta ese formato para `POST /api/auth/token`.
- El token devuelto por la API se guarda en `localStorage` y en el store de Pinia (`src/stores/auth.ts`). El frontend añade automáticamente el header `Authorization: Bearer <token>` a todas las peticiones mediante un interceptor en `src/services/api.ts`.
- Se implementaron guardas de rutas en `src/router/guards.ts` que redirigen a `/login` cuando no existe token y evitan acceso a rutas protegidas. `Header` y navegación están condicionadas a la autenticación.
- Logout limpia el token en el store y `localStorage` y redirige a `/login`.

### 2. Crear Empleado

- **Windows PowerShell:**
	```powershell
	Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/empleados/" -Method Post -Headers $headers -Body (@{nombre="Test"; documento="123"; salario_base=1500000; tipo_salario="ORDINARIO"} | ConvertTo-Json) -ContentType "application/json"
	```
- **Windows CMD:**
	```cmd
	curl -X POST http://127.0.0.1:9000/api/empleados/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"nombre\":\"Test\",\"documento\":\"123\",\"salario_base\":1500000,\"tipo_salario\":\"ORDINARIO\"}"
	```
- **macOS / Linux:**
	```bash
	curl -X POST http://127.0.0.1:9000/api/empleados/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"nombre":"Test","documento":"123","salario_base":1500000,"tipo_salario":"ORDINARIO"}'
	```

### 3. Liquidar Nómina

- **Windows PowerShell:**
	```powershell
	Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/nominas/liquidar" -Method Post -Headers $headers -Body (@{periodo="2026-01"} | ConvertTo-Json) -ContentType "application/json"
	```
- **Windows CMD:**
	```cmd
	curl -X POST http://127.0.0.1:9000/api/nominas/liquidar -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d "{\"periodo\":\"2026-01\"}"
	```
- **macOS / Linux:**
	```bash
	curl -X POST http://127.0.0.1:9000/api/nominas/liquidar -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"periodo":"2026-01"}'
	```

> [!TIP]
> - Para una demostración completa e interactiva, usa el script `demo_api.ps1` (PowerShell) o `demo_api.sh` (macOS/Linux) en la raíz del proyecto.
> - Si el puerto 9000 está ocupado, cambia el puerto con `--port 9001`.
> - Si aparece `WinError 10013`, arranca sin `--reload`.
> - Si el frontend no levanta, verifica `npm install` y que el backend siga en ejecución.
> - Si falta el token, genera uno con el login demo antes de llamar rutas protegidas.

 ## Ejemplos de Request y Response
 ### Crear empleado
 ```http
 POST /api/empleados/
 Authorization: Bearer <token>
 Content-Type: application/json

 {
 	"nombre": "Ana Perez",
 	"documento": "123456789",
 	"salario_base": "1500000",
 	"tipo_salario": "ORDINARIO"
 }
 ```

 ### Registrar novedad
 ```http
 POST /api/novedades/
 Authorization: Bearer <token>
 Content-Type: application/json

 {
 	"empleado_id": 1,
 	"periodo": "2030-02",
 	"tipo": "BONIFICACION",
 	"valor": "50000"
 }
 ```

 ### Liquidar nómina
 ```http
 POST /api/nominas/liquidar
 Authorization: Bearer <token>
 Content-Type: application/json

 {
 	"periodo": "2030-01"
 }
 ```

 Respuestas esperadas:
 - `201` cuando la liquidación genera nóminas nuevas.
 - `400` cuando el período ya fue liquidado.
 - `422` cuando el payload no cumple el esquema.


## Calidad y Pruebas (multiplataforma)

### Backend

- **Windows PowerShell:**
	```powershell
	.venv\Scripts\python -m pytest -q
	.venv\Scripts\python -m pytest --cov=backend.app.services.nomina_service --cov-report=term-missing --cov-fail-under=90
	```
- **Windows CMD:**
	```cmd
	.venv\Scripts\python.exe -m pytest -q
	.venv\Scripts\python.exe -m pytest --cov=backend.app.services.nomina_service --cov-report=term-missing --cov-fail-under=90
	```
- **macOS / Linux:**
	```bash
	python3 -m pytest -q
	python3 -m pytest --cov=backend.app.services.nomina_service --cov-report=term-missing --cov-fail-under=90
	```

#### Asegurar `pytest` en el entorno
Si `pytest` no se encuentra, activa el entorno virtual y ejecuta:

- **Windows PowerShell / CMD:**
	```powershell
	pip install pytest
	pip install -r backend/requirements.txt
	```
- **macOS / Linux:**
	```bash
	pip install pytest
	pip install -r backend/requirements.txt
	```

### Frontend

- **Todos los sistemas:**
	```bash
	cd frontend
	npm run build
	```
	Nota: actualmente no existe script `test` en `frontend/package.json`; usar `npm run build` como validación rápida de integridad del frontend.

 ## Evolución: Parámetros Dinámicos
 Se ha implementado la migración de constantes legales de código a base de datos. 
 - Tabla: `parametros_legales`
 - Campos dinámicos: salud, pensión, FSP, recargos, provisión prima/cesantía/int/vac.
 - Migración: Automática en el arranque mediante `session.py`.

 ## Cierre Formal
 - Alcance cubierto: backend, frontend, seguridad, calidad y documentación operativa.
 - Validación final: pruebas unitarias e integración ejecutadas con resultado satisfactorio.
 - Cobertura crítica: `backend.app.services.nomina_service` validada localmente en pruebas específicas; ejecutar la suite completa para verificar la cobertura global.
 - Nota: ejecutar `pip install pytest` en el entorno virtual si `pytest` no está instalado.
 - Estado de entrega: proyecto listo para uso local y para seguimiento evolutivo.

 ## Notas de alineación con el código
 - **Token demo y autenticación:** El endpoint `POST /api/auth/token` devuelve JWT de prueba; úsalo en `Authorization: Bearer <token>` para rutas protegidas en los ejemplos de esta guía.
 - **Upsert de novedades:** `POST /api/novedades/` implementa *upsert* por `(empleado_id, periodo)`; los scripts de demostración y pruebas deben manejar la posibilidad de actualización en lugar de creación duplicada.
 - **Nóminas:** Orquestación en `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve el historial y ahora soporta filtro por periodo `?periodo=YYYY-MM`.
 - **Modelos:** `ParametrosLegales`, `Empleado`, `Novedad`, `Nomina` están implementados en `backend/app/db/models.py` y los esquemas en `backend/app/schemas.py`.
 - **Filtros implementados:** `GET /api/nominas?periodo=YYYY-MM` y `GET /api/novedades?empleado_id=&periodo=` ya están disponibles en los routers; preferir uso de filtros desde el frontend para eficiencia.
 - **Auditoría:** Se añadieron endpoints `POST /api/auditoria/` y `GET /api/auditoria/` para trazabilidad administrativa (acceso `RH_ADMIN`).
