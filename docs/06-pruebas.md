# Documentación de Pruebas – NominaPro

## 1. Tipos de Pruebas Implementadas

### 1.1 Pruebas Unitarias (`tests/unit/`)
Validan la lógica de negocio aislada, sin dependencias externas.

| Archivo | Cobertura |
|---------|-----------|
| `test_nomina_service.py` | 100% - Cálculo de nómina (ordinario/integral, provisiones, deducciones) |
| `test_auditoria_repository.py` | Repositorio de auditoría |

**Ejecutar:**
```bash
.venv\Scripts\python -m pytest tests/unit/ -v
```

### 1.2 Pruebas de Integración (`tests/integration/`)
Validan endpoints HTTP reales con base de datos de prueba.

| Archivo | Descripción |
|---------|-------------|
| `test_empleados_novedades_integration.py` | CRUD empleados + novedades |
| `test_nominas_integration.py` | Liquidación de nómina |
| `test_filters_api.py` | Filtros y paginación |
| `test_security_roles.py` | Permisos y roles JWT |
| `test_auditoria_api.py` | Endpoints de auditoría |
| `test_novedades_uniqueness.py` | Upsert de novedades |

**Ejecutar:**
```bash
.venv\Scripts\python -m pytest tests/integration/ -v
```

### 1.3 Pruebas Frontend (`frontend/src/`)
Validan componentes y stores de Vue con Vitest.

| Archivo | Descripción |
|---------|-------------|
| `stores/auth.test.ts` | Store de autenticación Pinia |
| `services/api.test.ts` | Servicio API con Axios |

**Ejecutar:**
```bash
cd frontend
npm run test
```

---

## 2. Tipos de Pruebas por Implementar

### 2.1 Pruebas de Carga (Load Testing)
Simulan carga normal de usuarios concurrentes.

**Herramientas recomendadas:** Locust, k6, Apache Bench

**Escenarios:**
- Login de 50 usuarios concurrentes
- Consulta de nóminas con paginación
- Liquidación de nómina con 100 empleados

**Script ejemplo con k6 (`tests/load/login.js`):**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '30s',
};

export default function () {
  const params = {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  };
  const body = 'username=admin&password=secret';
  const res = http.post('http://127.0.0.1:9000/api/auth/token', body, params);
  check(res, { 'status 200': (r) => r.status === 200 });
  sleep(1);
}
```

**Ejecutar:**
```bash
k6 run tests/load/login.js
```

### 2.2 Pruebas de Estrés (Stress Testing)
Llevar el sistema al límite para encontrar puntos de quiebre.

**Escenarios:**
- 500+ empleados en liquidación simultánea
- picos de requests en endpoints de escritura
- saturación de conexión a base de datos

**Parámetros sugeridos:**
- Rampa: 0 → 200 VUs en 2 min → mantener 5 min → decrecer
- Timeout de requests: 30s máximo
- Umbral de error aceptable: < 1%

### 2.3 Pruebas UI/E2E
Validan el flujo completo desde el navegador.

**Herramientas:** Playwright, Cypress

**Flujos a probar:**
1. Login → Crear empleado → Liquidar nómina → Ver resultado
2. Login → Crear empleado inválido → Validar errores
3. Logout → Acceso a ruta protegida → Redirección a login

**Ejemplo Playwright (`tests/e2e/login.spec.ts`):**
```typescript
import { test, expect } from '@playwright/test';

test('login exitoso', async ({ page }) => {
  await page.goto('http://localhost:5173/login');
  await page.fill('input[type="text"]', 'admin');
  await page.fill('input[type="password"]', 'secret');
  await page.click('button');
  await expect(page).toHaveURL('http://localhost:5173/');
});
```

**Ejecutar:**
```bash
npx playwright test
```

### 2.4 Pruebas de Seguridad
Validan protección contra vulnerabilidades comunes.

**Categorías:**
- SQL Injection en filtros
- XSS en formularios
- Fuerza bruta en login
- Exposición de datos sensibles

**Herramientas:** OWASP ZAP, Burp Suite, SQLMap

### 2.5 Pruebas de Regresión
Aseguran que cambios nuevos no rompen funcionalidad existente.

**Estrategia:**
- Ejecutar suite completa antes de cada merge
- CI/CD con GitHub Actions
- Coverage mínimo: 90%

---

## 3. Ejecución de Pruebas

### 3.1 Todos los tests backend
```bash
.venv\Scripts\python -m pytest -q --cov=backend.app --cov-report=term-missing
```

### 3.2 Coverage específico
```bash
.venv\Scripts\python -m pytest --cov=backend.app.services.nomina_service --cov-report=term-missing --cov-fail-under=90
```

### 3.3 Frontend
```bash
cd frontend
npm run test        # Una vez
npm run test:watch  # Modo interactivo
```

### 3.4 Integración continua (GitHub Actions)
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements.txt
      - run: pytest -q --cov=backend.app --cov-fail-under=80

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm install
      - run: cd frontend && npm run test
```

---

## 4. Matriz de Cobertura

| Módulo | Unitarias | Integración | UI/E2E | Carga | Estrés |
|--------|-----------|--------------|--------|-------|--------|
| Auth/JWT | ✅ | ✅ | ✅ | ❌ | ❌ |
| Empleados | ✅ | ✅ | ❌ | ❌ | ❌ |
| Novedades | - | ✅ | ❌ | ❌ | ❌ |
| Nóminas | ✅ | ✅ | ❌ | ❌ | ❌ |
| Cálculos | ✅ | - | - | ❌ | ❌ |

---

## 5. Buenas Prácticas

1. **Aislamiento:** Cada test debe ser independiente y limpiar sus datos.
2. **Nombres descriptivos:** `test_crear_empleado_rechaza_salario_bajo_smmlv`
3. **Fixtures:** Usar `conftest.py` para datos comunes.
4. **Aserciones claras:** Mensajes de error útiles.
5. **Orden de ejecución:** Unitarias → Integración → E2E → Carga

---

## 6. Próximos Pasos

- [ ] Implementar pruebas de carga con k6
- [ ] Agregar tests E2E con Playwright
- [ ] Configurar CI/CD en GitHub Actions
- [ ] Pruebas de seguridad automatizadas
- [ ] Reporte de coverage en PRs
