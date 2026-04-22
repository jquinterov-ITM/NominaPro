#!/usr/bin/env python3
import argparse
import json
import string
import sys


def load_tasks(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def print_tasks(tasks, style="1"):
    for i, t in enumerate(tasks, start=1):
        label = str(i) if style == "1" else string.ascii_lowercase[i - 1]
        print(f"[{label}] {t.get('title')} - {t.get('summary','')}")
    print()


def parse_selection(sel, tasks, style):
    sel = sel.strip().lower()
    if not sel:
        return []
    parts = [s.strip() for s in sel.replace(";", ",").split(",")]
    results = []
    for p in parts:
        if p == "":
            continue
        # numeric selection
        if p.isdigit():
            try:
                idx = int(p) - 1
                if 0 <= idx < len(tasks):
                    results.append(tasks[idx])
            except:
                pass
        else:
            # letter selection (take first character)
            ch = p[0]
            if ch in string.ascii_lowercase:
                idx = ord(ch) - ord("a")
                if 0 <= idx < len(tasks):
                    results.append(tasks[idx])
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Resumen interactivo de tareas (elige por número o letra)."
    )
    parser.add_argument(
        "tasks",
        nargs="?",
        default="scripts/tasks_example.json",
        help="Archivo JSON con lista de tareas",
    )
    parser.add_argument(
        "--style",
        choices=["1", "a"],
        default="1",
        help='Formato de enumeración: "1" números, "a" letras',
    )
    args = parser.parse_args()
    try:
        tasks = load_tasks(args.tasks)
    except Exception as e:
        print(f"Error cargando tareas: {e}")
        sys.exit(1)
    print("Resumen de tareas a ejecutar:")
    print_tasks(tasks, style=args.style)
    sel = input("Seleccione opción(es) (ej: 1 o a, múltiples separadas por coma): ")
    chosen = parse_selection(sel, tasks, args.style)
    if not chosen:
        print("No se seleccionó ninguna tarea válida.")
        sys.exit(1)
    print("\nSeleccionaste:")
    for t in chosen:
        print(f"- {t.get('title')}: {t.get('description','(sin detalles)')}")
    print("\nAcción: ejecutar tareas seleccionadas (stub).")


if __name__ == "__main__":
    main()
