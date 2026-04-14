#!/usr/bin/env bash
# Script de demostración para macOS / Linux
# Requiere: curl, jq (opcional para parseo)

BASE_URL="http://127.0.0.1:9000"

echo "Obteniendo token demo..."
RESP=$(curl -s -X POST "$BASE_URL/api/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=secret")
echo "Respuesta del login: $RESP"

# Extraer token con jq si está disponible, si no imprimir y pedir copiar manualmente
if command -v jq >/dev/null 2>&1; then
  TOKEN=$(echo "$RESP" | jq -r .access_token)
else
  echo "Instala 'jq' para extracción automática del token, o copia el access_token desde la respuesta anterior."
  echo "Respuesta completa: $RESP"
  exit 0
fi

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  echo "No se obtuvo token. Revisa que la API esté levantada y las credenciales sean correctas."
  exit 1
fi

AUTH_HEADER="Authorization: Bearer $TOKEN"

echo "Token obtenido. Cabecera: $AUTH_HEADER"

echo "Listado de empleados (GET /api/empleados/)"
curl -s -H "$AUTH_HEADER" "$BASE_URL/api/empleados/" | jq .

echo "Liquidando nómina (POST /api/nominas/liquidar) para periodo 2026-01"
curl -s -X POST -H "Content-Type: application/json" -H "$AUTH_HEADER" -d '{"periodo":"2026-01"}' "$BASE_URL/api/nominas/liquidar" | jq .

echo "Completado."
