# Guía de Exposición: NominaPro API

Esta guía está diseñada para que puedas realizar una demostración profesional de cómo el sistema procesa la nómina desde el backend.

## 1. Introducción
- **Objetivo**: Mostrar la robustez del sistema y la separación de responsabilidades entre el core de cálculo y la API.
- **Contexto**: Reglas de negocio 2026 configurables dinámicamente.

---

## 2. El Flujo de la Demostración

### Paso 1: Seguridad y Autenticación (JWT)
**Narrativa**: "Para garantizar la integridad de los datos, todos nuestros endpoints sensibles están protegidos por JWT con roles definidos."

- **Intento Fallido (Error 401)**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/empleados" -Method Get
```
*(Mostrar la respuesta de 'Not authenticated')*

- **Obtención de Token**:
```powershell
$login = Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/auth/token" -Method Post -Body @{username="admin"; password="secret"}
$token = $login.access_token
$headers = @{Authorization = "Bearer $token"}
```

---

### Paso 2: Parametrización Dinámica
**Narrativa**: "A diferencia de sistemas rígidos, NominaPro permite actualizar las reglas de ley sin cambiar una sola línea de código."

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/parametros/2026" -Method Get -Headers $headers | ConvertTo-Json
```
*(Destacar campos como `smmlv_2026`, `porcentaje_salud`, etc.)*

---

### Paso 3: Gestión de Empleados
**Narrativa**: "Registramos un empleado ordinario y validamos el cumplimiento de salarios integrales."

```powershell
$empleado = @{
    nombre = "Expositor ITM"
    documento = "999999"
    salario_base = 2500000
    tipo_salario = "ORDINARIO"
}
Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/empleados/" -Method Post -Headers $headers -Body ($empleado | ConvertTo-Json) -ContentType "application/json"
```

---

### Paso 4: Novedades del Período
**Narrativa**: "Agregamos novedades que afectarán el cálculo final (ej. una bonificación)."

```powershell
$novedad = @{
    empleado_id = 1
    periodo = "2026-05"
    tipo = "BONIFICACION"
    valor = 200000
}
Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/novedades/" -Method Post -Headers $headers -Body ($novedad | ConvertTo-Json) -ContentType "application/json"
```

---

### Paso 5: Liquidación de Nómina
**Narrativa**: "Ejecutamos el motor de liquidación. El sistema aplicará retenciones, aportes y provisiones de forma automática."

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/nominas/liquidar" -Method Post -Headers $headers -Body (@{periodo="2026-05"} | ConvertTo-Json) -ContentType "application/json"
```

---

### Paso 6: Resultados y Cierre
**Narrativa**: "Consultamos el resultado final. Observen cómo el NETO coincide con la suma del salario base + novedades - deducciones de ley."

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9000/api/nominas?periodo=2026-05" -Method Get -Headers $headers | ConvertTo-Json
```

---

## 3. Conclusión
- Resaltar la **cobertura del 100%** en el motor de cálculo.
- Mencionar que el frontend utiliza estas mismas APIs validadas por pruebas de **Vitest**.
