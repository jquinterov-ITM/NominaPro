"""
Pruebas de estrés para NominaPro.
Ejecutar con: python tests/stress/stress_test.py
Este script simula carga progresiva para encontrar el punto de quiebre.
"""

import statistics
import threading
import time
from typing import Dict, List

import requests

BASE_URL = "http://127.0.0.1:9000"
results: List[Dict] = []
lock = threading.Lock()


def get_token() -> str:
    """Obtiene token de autenticación."""
    response = requests.post(
        f"{BASE_URL}/api/auth/token",
        data={"username": "admin", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["access_token"]


def make_request(endpoint: str, token: str):
    """Ejecuta una petición y guarda el resultado."""
    start = time.time()
    try:
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        elapsed = time.time() - start
        with lock:
            results.append(
                {
                    "status": response.status_code,
                    "time": elapsed,
                    "success": 200 <= response.status_code < 400,
                }
            )
    except Exception as e:
        elapsed = time.time() - start
        with lock:
            results.append(
                {"status": 0, "time": elapsed, "success": False, "error": str(e)}
            )


def stress_test(endpoint: str, duration_sec: int, threads: int, token: str):
    """Ejecuta prueba de estrés por duración determinada."""
    print(f"\nIniciando estrés: {endpoint}")
    print(f"Duración: {duration_sec}s | Hilos: {threads}")

    start_time = time.time()
    request_count = 0

    while time.time() - start_time < duration_sec:
        threads_list = []
        for _ in range(threads):
            t = threading.Thread(target=make_request, args=(endpoint, token))
            t.start()
            threads_list.append(t)

        for t in threads_list:
            t.join()

        request_count += threads
        time.sleep(0.1)

    return request_count


def print_results(total_requests: int):
    """Imprime estadísticas de resultados."""
    if not results:
        print("Sin resultados")
        return

    times = [r["time"] for r in results]
    successes = sum(1 for r in results if r["success"])

    print("\n--- Resultados ---")
    print(f"Total requests: {total_requests}")
    print(f"Exitosos: {successes} ({successes/total_requests*100:.1f}%)")
    print(
        f"Fallidos: {total_requests - successes} ({(total_requests-successes)/total_requests*100:.1f}%)"
    )
    print(f"Tiempo promedio: {statistics.mean(times)*1000:.2f}ms")
    print(f"Tiempo p95: {statistics.quantiles(times, n=20)[18]*1000:.2f}ms")
    print(f"Tiempo máximo: {max(times)*1000:.2f}ms")


if __name__ == "__main__":
    print("Pruebas de Estrés - NominaPro")
    print("Asegúrate de tener el backend ejecutándose en el puerto 9000")
    print("Presiona Ctrl+C para detener\n")

    try:
        token = get_token()
        print(f"Token obtenido: {token[:20]}...")

        # Prueba 1: Carga moderada
        print("\n=== Prueba 1: Carga moderada (60s, 20 hilos) ===")
        stress_test("/api/empleados/", duration_sec=60, threads=20, token=token)
        print_results(len(results))
        results.clear()

        # Prueba 2: Carga alta
        print("\n=== Prueba 2: Carga alta (30s, 50 hilos) ===")
        stress_test("/api/empleados/", duration_sec=30, threads=50, token=token)
        print_results(len(results))
        results.clear()

        # Prueba 3: Carga extrema
        print("\n=== Prueba 3: Carga extrema (20s, 100 hilos) ===")
        stress_test("/api/empleados/", duration_sec=20, threads=100, token=token)
        print_results(len(results))

    except KeyboardInterrupt:
        print("\nPrueba interrumpida por el usuario")
    except Exception as e:
        print(f"Error: {e}")
