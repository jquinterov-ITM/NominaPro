---
description: workflows y guías de agentes para el proyecto NominaPro
---

# Workflows de NominaPro para Agentes

Compatibilidad multiplataforma: los pasos de arranque funcionan en Windows (PowerShell/CMD), macOS y Linux (bash/zsh). Ejemplo mínimo para crear/activar `venv`:

- PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

- macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Documento operativo para que los agentes ejecuten NominaPro **desde cero**, realicen cambios con bajo riesgo y cierren tareas con trazabilidad.

---

## Flujo maestro obligatorio (orden estricto)

### Paso 1. Cargar contexto base
1.  Leer el skill de contexto del proyecto en `prompts/01-prompt-skill.md`.
2. Revisar `README.md` (arranque y troubleshooting).
3. Revisar `docs/07-implementacion.md` (instalación guiada).

### Paso 2. Preflight de entorno
1. Verificar versiones: Python, pip, Node, npm.
2. Confirmar ubicación en la raíz del proyecto.
3. Confirmar que no hay procesos previos bloqueando puertos 9000/5173.

### Paso 3. Levantar backend primero
1. Crear y activar `.venv`.
2. Instalar `backend/requirements.txt`.
3. Configurar SQLite local (`DATABASE_URL=sqlite:///./nominapro.db`) cuando aplique.
4. Ejecutar:
   - `uvicorn app.main:app --reload --app-dir backend`
   - Antes de ejecutar, asegúrate de haber copiado `.env.example` a `.env` y, si corresponde, haber aplicado migraciones:
     - `python -m alembic -c backend/alembic.ini upgrade head`
   - Ejecuta `pre-commit run --all-files` para aplicar formato/imports antes de trabajar en el código.
5. Validar:
   - `/docs`
   - endpoints principales bajo `/api`.

### Paso 4. Levantar frontend después
1. Entrar a `frontend/`.
2. Ejecutar `npm install`.
3. Ejecutar `npm run dev`.
4. Validar navegación de vistas y comunicación con backend.

### Paso 5. Ejecutar tarea de desarrollo
1. Definir alcance en lote pequeño.
2. Editar solo archivos necesarios.
3. Mantener contratos API o documentar cualquier cambio explícito.
4. Validar funcionalidad afectada.

### Paso 6. Cierre y evidencia
1. Actualizar documentación impactada (`README`, `prompts/*`, `docs/*`).
2. Registrar estado en `TODO.md`.
3. Confirmar criterios de terminado:
   - ejecución local reproducible,
   - flujo mínimo funcional,
   - documentación coherente con el código.

---

## Workflows y Guías de Ejecución

El proyecto cuenta con comandos y directrices específicas. Si estás en un entorno nuevo, estas son las instrucciones funcionales para cada workflow (alineadas con los comandos en `.agents/workflows`):

### 1. `/crear-modulo-crud-backend` (Crear nuevo módulo CRUD backend)

**Uso**: agregar un recurso nuevo (ej: centros de costo).

**Pasos**:
1. Crear router en `backend/app/api/{modulo}.py`.
2. Crear/ajustar esquemas en `backend/app/schemas.py` (o archivo equivalente).
3. Crear lógica de negocio en capa de servicio (si aplica).
4. Ajustar modelos/tablas en `backend/app/db/models.py` y sesión según necesidad.
5. Registrar router en `backend/app/main.py` bajo `/api/{modulo}`.
6. Validar casos: éxito, validación inválida, no encontrado.
7. Documentar endpoints y reglas en `docs/05-backend.md` y `docs/02-funcional.md`.

### 2. `/agregar-endpoint` (Ampliar módulo existente)

**Uso**: ampliar o modificar módulos actuales (`empleados`, `novedades`, `nominas`, `parametros`).

**Pasos**:
1. Revisar router actual en `backend/app/api/{modulo}.py`.
2. Revisar modelos/esquemas impactados.
3. Implementar validación de entrada y manejo homogéneo de errores.
4. Probar compatibilidad con frontend existente.
5. Para pruebas locales rápidas puedes generar un token con `scripts/get_token.py` o usar el endpoint `POST /api/auth/token` (ver `demo_api.ps1`).
5. Actualizar documentación del módulo.

### 3. `/code-review` (Refactor por capas sin romper API)

**Uso**: mejorar mantenibilidad sin cambiar contratos y corregir código.

**Pasos**:
1. Identificar lógica extensa en rutas.
2. Extraer a funciones o servicios reutilizables.
3. Mantener payloads de request/response.
4. Validar endpoints existentes (regresión mínima).
5. Documentar cambios técnicos internos.

### 4. Seguridad incremental (Manual)

**Uso**: endurecer la API gradualmente.

**Pasos**:
1. Ajustar CORS con whitelist.
2. Definir/ajustar autenticación y autorización por rol.
3. Proteger rutas sensibles.
4. Registrar eventos críticos sin exponer datos sensibles.
5. Actualizar `docs/04-seguridad.md`.

### 5. `/escribir-tests` (Validación y pruebas mínimas)

**Uso**: cerrar cambios con evidencia técnica de funcionamiento.

**Casos mínimos**:
1. Happy path.
2. Validación fallida.
3. Recurso inexistente.
4. Flujo extremo a extremo mínimo:
   - empleado → novedad → liquidación de nómina → consulta.

### 6. `/documentar-modulo` (Documentación funcional/técnica)

**Uso**: al cerrar un lote de cambios.

**Pasos**:
1. Actualizar rutas y ejemplos JSON en `docs/05-backend.md`.
2. Actualizar guía de ejecución en `docs/07-implementacion.md`/`README.md` si aplica.
3. Verificar consistencia entre prompts y documentación.

---

## Expectativas de Comportamiento (Skills de Agente)

Si estás configurando este proyecto en un entorno vacío o autoinstruyéndote como agente, debes adoptar de manera obligatoria las siguientes disciplinas (o descargar los skills equivalentes si los soporta tu plataforma):

### 7. Comportamiento: Diseño Frontend (`frontend-design`)
**Enfoque**: Crear interfaces de usuario (Vue 3) que se sientan de alta gama ("premium"), evitando el típico aspecto de "MVP genérico" o IA básica.
**Pautas**:
1. Emplear paletas de colores armónicas (rechazar colores primarios planos del navegador).
2. Utilizar tipografía moderna (ej: Inter, Roboto) e implementar micro-animaciones fluidas (hover, focus).
3. Asegurar que cada nueva vista cuente con la más alta atención al detalle visual y "glassmorphism" o diseño responsivo estético.

### 8. Comportamiento: Accesibilidad (`accessibility`)
**Enfoque**: Auditar constructivamente todo código HTML / Vue para su universalidad.
**Pautas**:
1. Asegurar cumplimiento de WCAG 2.2 (contrastes, `aria-labels`).
2. Soportar navegación íntegra por teclado en modales, formularios y tablas.

### 9. Comportamiento: Optimización SEO (`seo`)
**Enfoque**: Preparar la web para motores de búsqueda (en las vistas que sean públicas).
**Pautas**:
1. Manejar adecuadamente los tags `title`, descripciones `meta`, y semántica HTML (`H1`-`H6`).

> **Aclaración Técnica (Node.js vs Python)**: El motor **backend** de NominaPro es y seguirá siendo estrictamente **Python / FastAPI**. Por ello, no se deben usar reglas ni dependencias de servidor en Node.js (ej. *nodejs-backend-patterns* o *Express*). Sin embargo, **Node.js y `npm` SÍ son requeridos y correctos** para instalar dependencias y levantar el entorno del **frontend** (Vue 3 + Vite).

### 10. Resumen numerado al final de cada interaccion.
**Enfoque**: Prompt template para skill que presenta resumen numerado y solicita selección.
**Pautas**
Cuando ejecutes este skill, realiza lo siguiente:

1. Muestra un resumen breve y enumerado de las acciones propuestas (título + resumen).
2. Ofrece enumeración en formato numérico `1,2,3...` y alernativa alfabética `a,b,c...`.
3. Pide al usuario seleccionar una o varias opciones (acepta `1` o `a`, y múltiples separadas por coma).
4. Tras la selección, confirma mostrando la(s) tarea(s) seleccionada(s) con su descripción completa.

Ejemplo breve de prompt (para agentes):
"""
Tengo 3 cambios propuestos. Muestra la lista enumerada y pídele al usuario elegir por número o letra. Luego confirma las selecciones con detalles.
"""

---

## Uso recomendado de prompts por objetivo

1. `01-prompt-skill.md`: contexto base + protocolo desde cero.
2. `03-prompt-backend.md`: cambios de API y modelo.
3. `04-prompt-frontend.md`: cambios UI/Vue.
4. `02-prompt-funcional.md`: reglas de negocio de nómina.
5. `05-prompt-seguridad.md`: controles y riesgos.
6. `06-prompt-calidad.md`: validación y estrategia de pruebas.
7. `07-prompt-implementacion.md`: despliegue/operación.
8. `08-prompt-arquitectura.md`: decisiones estructurales.

## Regla de oro para agentes

Ningún cambio se considera terminado si no puede ser ejecutado desde cero por otra persona siguiendo la documentación paso a paso.

## Notas de alineación con el código
- **Autenticación:** JWT ya está integrado en `backend/app/core/auth.py` y se usa en dependencias `require_roles` en routers críticos.
- **Novedades:** `POST /api/novedades/` hace upsert por `(empleado_id, periodo)`; no hay endpoint público para filtrar novedades por `empleado_id` y/o `periodo`.
- **Nóminas:** Orquestación en `POST /api/nominas/liquidar`; `GET /api/nominas/` devuelve historial completo sin query `periodo` por ahora.
- **Términos:** estandarizar a `tipo_salario` en documentación y prompts.
 
## Cambios recientes (resumen)

- Se centralizó la gestión de secretos en variables de entorno; existe `.env.example` con valores recomendados.
- Se añadió soporte de migraciones con Alembic (`backend/alembic/`) y se proporcionaron pasos reproducibles en `docs/07-implementacion.md`.
- Añadido `scripts/get_token.py` para generar JWT de prueba desde la CLI y ejemplos de obtención de token via API (`demo_api.ps1`).
- Se integró `pre-commit` (black, isort, ruff) y se añadió un workflow CI básico.

Incluye en tus runbooks los pasos de arranque de `docs/07-implementacion.md` para asegurar reproducibilidad desde cero.
