---
description: crear una vista Vue 3 en el frontend de NominaPro
---

# Crear página CRUD en frontend

Usar cuando necesites agregar la UI de un módulo ya existente en el backend de NominaPro.

## Pasos

1. Crear el componente en frontend/src/views/{Modulo}View.vue (<script setup>).
2. Definir interfaz (PicnicCSS).
3. Consumir la API usando Axios pre-configurado (api.js).
4. Si requiere campos monetarios, usar Number(val).toLocaleString('es-CO').
5. Gestionar captura de errores 400/422.
6. Agregar la ruta en frontend/src/router/index.js.
