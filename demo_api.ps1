# demo_api.ps1 - Script interactivo para Exposición NominaPro
# Ejecutar con: ./demo_api.ps1

$BASE_URL = "http://127.0.0.1:9000/api"

function Show-Header($title) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  $title" -ForegroundColor White -BackgroundColor DarkBlue
    Write-Host "========================================`n" -ForegroundColor Cyan
}

function Wait-Key {
    Write-Host "`n[Presiona cualquier tecla para continuar con el siguiente paso...]" -ForegroundColor Yellow
    $null = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Clear-Host
Show-Header "NOMINAPRO - DEMO TECNICA API"

# PASO 1: Autenticación
Write-Host "Paso 1: Obteniendo token de seguridad..." -ForegroundColor Green
try {
    $login = Invoke-RestMethod -Uri "$BASE_URL/auth/token" -Method Post -Body @{username="admin"; password="secret"}
    $token = $login.access_token
    $headers = @{Authorization = "Bearer $token"}
    Write-Host "TOKEN OBTENIDO: $($token.Substring(0,20))..." -ForegroundColor Gray
} catch {
    Write-Host "Error al autenticar. Asegúrate de que el backend esté corriendo en el puerto 9000." -ForegroundColor Red
    exit
}

Wait-Key

# PASO 2: Parámetros Legales
Show-Header "PASO 2: CONSULTA DE PARAMETROS LEGALES 2026"
Write-Host "Solicitando reglas de negocio dinámicas..." -ForegroundColor Green
$params = Invoke-RestMethod -Uri "$BASE_URL/parametros/2026" -Method Get -Headers $headers
$params | ConvertTo-Json | Write-Host -ForegroundColor White

Wait-Key

# PASO 3: Crear Empleado
Show-Header "PASO 3: CREACION DE EMPLEADO"
$empleado = @{
    nombre = "EXPOSITOR ITM $(Get-Date -Format 'HHmm')"
    documento = "EMP$(Get-Random -Minimum 1000 -Maximum 9999)"
    salario_base = 2500000
    tipo_salario = "ORDINARIO"
}
Write-Host "Enviando payload:" -ForegroundColor Gray
$empleado | ConvertTo-Json | Write-Host -ForegroundColor White

$resEmp = Invoke-RestMethod -Uri "$BASE_URL/empleados/" -Method Post -Headers $headers -Body ($empleado | ConvertTo-Json) -ContentType "application/json"
Write-Host "`nEMPLEADO CREADO EXITOSAMENTE (ID: $($resEmp.id))" -ForegroundColor Green

Wait-Key

# PASO 4: Registrar Novedad
Show-Header "PASO 4: REGISTRO DE NOVEDADES (BONIFICACION)"
$novedad = @{
    empleado_id = $resEmp.id
    periodo = "2026-05"
    tipo = "BONIFICACION"
    valor = 200000
}
Write-Host "Registrando $200.000 extra para el período 2026-05..." -ForegroundColor Green
Invoke-RestMethod -Uri "$BASE_URL/novedades/" -Method Post -Headers $headers -Body ($novedad | ConvertTo-Json) -ContentType "application/json" | Out-Null
Write-Host "Novedad registrada."

Wait-Key

# PASO 5: Liquidación
Show-Header "PASO 5: EJECUCION DEL MOTOR DE LIQUIDACION"
Write-Host "Calculando nómina para Mayo 2026..." -ForegroundColor Green
$null = Invoke-RestMethod -Uri "$BASE_URL/nominas/liquidar" -Method Post -Headers $headers -Body (@{periodo="2026-05"} | ConvertTo-Json) -ContentType "application/json"
Write-Host "Proceso completado." -ForegroundColor Green

Wait-Key

# PASO 6: Resultados
Show-Header "PASO 6: CONSULTA DE RESULTADOS FINALES"
Write-Host "Obteniendo resumen de nómina..." -ForegroundColor Green
$resultados = Invoke-RestMethod -Uri "$BASE_URL/nominas?periodo=2026-05" -Method Get -Headers $headers
$resultados | ConvertTo-Json -Depth 5 | Write-Host -ForegroundColor White

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "      FIN DE LA DEMOSTRACION" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan
