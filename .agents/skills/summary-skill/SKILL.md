---
title: Skill - Resumen Interactivo de Tareas
description: Muestra un resumen enumerado de acciones propuestas y permite seleccionar (números o letras).
---

# Resumen Interactivo (Skill)

Este skill presenta un resumen enumerado de las tareas a ejecutar y solicita al usuario que seleccione una o varias opciones antes de ejecutar.

Comportamiento:
- Recibe una lista de tareas (title, summary, description).
- Muestra la lista enumerada por números (1,2,3...) o letras (a,b,c...).
- Acepta selección por números o letras, simples o múltiples (separadas por coma).
- Devuelve la(s) tarea(s) seleccionada(s) para la ejecución por el agente.

Uso recomendado:
- Integrar con un script runner que lea un JSON con las tareas y muestre la UI de selección (ver `scripts/agent_summary.py`).

Ejemplo de prompt para agentes:
"""
Voy a ejecutar cambios; muéstrame un resumen enumerado de las acciones propuestas (título y resumen) y pídeme seleccionar por número o letra. Después de la selección, confirma las tareas elegidas con sus descripciones completas.
"""
