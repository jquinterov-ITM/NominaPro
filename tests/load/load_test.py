"""
Pruebas de carga básicas para NominaPro.
Ejecutar con: python tests/load/load_test.py
Requiere: pip install requests
"""

import concurrent.futures
import statistics
import time
from typing import Dict, List

import requests

BASE_URL = "http://127.0.0.1:9000"


def get_token() -> str:
    """Obtiene token de autenticación."""
    response = requests.post(
        f"{BASE_URL}/api/auth/token",
        data={"username": "admin", "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["access_token"]


def test_endpoint(
    path: str, method: str = "GET", data: dict = None, token: str = None
) -> Dict:
    """Ejecuta una petición y mide el tiempo."""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    start = time.time()
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}", headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(
                f"{BASE_URL}{path}", json=data, headers=headers, timeout=30
            )
        elapsed = time.time() - start
        return {
            "status": response.status_code,
            "time": elapsed,
            "success": response.status_code < 400,
        }
    except Exception as e:
        return {
            "status": 0,
            "time": time.time() - start,
            "success": False,
            "error": str(e),
        }


def run_load_test(name: str, func, iterations: int, workers: int = 10):
    """Ejecuta prueba de carga."""
    print(f"\n{'='*50}")
    print(f"Prueba: {name}")
    print(f"Iteraciones: {iterations}, Workers: {workers}")
    print(f"{'='*50}")

    results: List[Dict] = []
    start_total = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(func) for _ in range(iterations)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    total_time = time.time() - start_total

    times = [r["time"] for r in results]
    successes = sum(1 for r in results if r["success"])

    print(f"Total tiempo: {total_time:.2f}s")
    print(
        f"Peticiones exitosas: {successes}/{iterations} ({successes/iterations*100:.1f}%)"
    )
    print(f"Tiempo promedio: {statistics.mean(times)*1000:.2f}ms")
    print(f"Tiempo mínimo: {min(times)*1000:.2f}ms")
    print(f"Tiempo máximo: {max(times)*1000:.2f}ms")
    print(f"Req/sec: {iterations/total_time:.2f}")

    return results


def test_health():
    """Test endpoint de salud."""
    return test_endpoint("/health")


def test_login():
    """Test de autenticación."""
    return test_endpoint(
        "/api/auth/token",
        method="POST",
        data={"username": "admin", "password": "secret"},
    )


def test_list_empleados():
    """Test listado de empleados."""
    token = get_token()
    return test_endpoint("/api/empleados/", token=token)


def test_list_nominas():
    """Test listado de nóminas."""
    token = get_token()
    return test_endpoint("/api/nominas/", token=token)


if __name__ == "__main__":
    print("Pruebas de Carga - NominaPro")
    print("Asegúrate de tener el backend ejecutándose en el puerto 9000")

    run_load_test("Health Check", test_health, iterations=100, workers=20)
    run_load_test("Login", test_login, iterations=50, workers=10)
    run_load_test("Listar Empleados", test_list_empleados, iterations=50, workers=10)
    run_load_test("Listar Nóminas", test_list_nominas, iterations=50, workers=10)

    print("\nPruebas de carga completadas.")
