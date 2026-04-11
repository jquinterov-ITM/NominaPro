# Documentación de Implementación – NominaPro

## Requisitos Previos
- Python 3.11+.
- `pip` y Git.
- Node.js 18+.
- Windows, Linux o macOS.

## Estructura
```text
NominaPro/
├── backend/
├── frontend/
├── docs/
├── prompts/
└── README.md
```

## Arranque en Windows
### Backend

#### Primera vez
```cmd
cd "\NominaPro"             [Raiz del proyecto]

python -m venv .venv        [si no aparece (.venv)]
.venv\Scripts\Activate.ps1  

python -m pip install -r backend\requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 9000 --app-dir backend
```

#### Segunda vez
```cmd
.venv\Scripts\Activate.ps1

python -m uvicorn app.main:app --host 127.0.0.1 --port 9000 --app-dir backend
```

### Frontend
Abrir nueva terminal.
#### Primera vez
```cmd
cd "\NominaPro\frontend" [Moverse al Front]
npm install
npm run dev
```

#### Segunda vez
```cmd
cd .\frontend
npm run dev
```

Si PowerShell bloquea la activación del entorno, usa `.venv\Scripts\Activate.bat` desde una terminal nueva.

## Configuración Inicial
### Variables de entorno
- `PORT`
- `DATABASE_URL`
- `SECRET_KEY`
- `ALLOWED_ORIGINS`
- `VITE_API_URL` solo si quieres apuntar el frontend a otro backend distinto del proxy local.

### Qué hacer con las variables de entorno
- Copia `.env.example` a `.env` en la raíz del proyecto si quieres dejar valores explícitos.
- Si trabajas en local con SQLite y el login de demo, los valores por defecto ya alcanzan.
- En el frontend, usa `frontend/.env.example` solo si no vas a usar el proxy de Vite.
- Si el login queda como invitado, revisa primero que el backend esté corriendo y que la URL del API sea la correcta.
- Si el navegador conserva una sesión anterior, cierra sesión o borra el almacenamiento local del sitio para forzar un nuevo inicio.

### Modo demo
- Usuario: `admin`
- Clave: `secret`
- Roles: `RH_ADMIN`, `PAYROLL_USER`
- El formulario de inicio de sesión está en la portada; al entrar correctamente, la barra superior deja de mostrar `Invitado`.



## Verificacion de Arranque
- API Docs (Swagger): [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs)
- Frontend: [http://localhost:5173](http://localhost:5173/)

## Flujo de Verificacion Manual (API)
Para verificar el funcionamiento core desde la terminal (PowerShell):

1. **Autenticacion**:
   ```powershell
   $res = Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/auth/token" -Method Post -Body @{username="admin"; password="secret"}
   $headers = @{Authorization = "Bearer $($res.access_token)"}
   ```

2. **Crear Empleado**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/empleados/" -Method Post -Headers $headers -Body (@{nombre="Test"; documento="123"; salario_base=1500000; tipo_salario="ORDINARIO"} | ConvertTo-Json) -ContentType "application/json"
   ```

3. **Liquidar Nomina**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/nominas/liquidar" -Method Post -Headers $headers -Body (@{periodo="2026-01"} | ConvertTo-Json) -ContentType "application/json"
   ```

> [!TIP]
> Para una demostracion completa e interactiva, usa el script `demo_api.ps1` en la raiz del proyecto.
- Si el puerto 9000 está ocupado, cambia el puerto con `--port 9001`.
- Si aparece `WinError 10013`, arranca sin `--reload`.
- Si el frontend no levanta, verifica `npm install` y que el backend siga en ejecución.
- Si falta el token, genera uno con el login demo antes de llamar rutas protegidas.

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

## Calidad y Pruebas
### Backend
```cmd
.venv\Scripts\python -m pytest -q
```

```cmd
.venv\Scripts\python -m pytest --cov=backend.app.services.nomina_service --cov-report=term-missing --cov-fail-under=90
```

### Frontend
```cmd
cd frontend
npm run test
```

## Evolución: Parámetros Dinámicos
Se ha implementado la migración de constantes legales de código a base de datos. 
- Tabla: `parametros_legales`
- Campos dinámicos: salud, pensión, FSP, recargos, provisión prima/cesantía/int/vac.
- Migración: Automática en el arranque mediante `session.py`.

## Cierre Formal
- Alcance cubierto: backend, frontend, seguridad, calidad y documentación operativa.
- Validación final: pruebas unitarias e integración ejecutadas con resultado satisfactorio.
- Cobertura crítica: `backend.app.services.nomina_service` validado al 100%.
- Estado de entrega: proyecto listo para uso local y para seguimiento evolutivo.