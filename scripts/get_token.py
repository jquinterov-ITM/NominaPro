#!/usr/bin/env python3
"""CLI helper to print a JWT token for local testing.

Usage:
  python scripts/get_token.py --sub admin --roles RH_ADMIN, PAYROLL_USER --minutes 60
"""
from __future__ import annotations

import argparse
from datetime import timedelta

from backend.app.core.auth import create_access_token


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Genera y muestra un JWT de prueba usando create_access_token()"
    )
    p.add_argument(
        "--sub", default="admin", help="Subject (sub) claim, por defecto 'admin'"
    )
    p.add_argument(
        "--roles",
        default="RH_ADMIN",
        help="Roles separados por coma (ej: RH_ADMIN,PAYROLL_USER)",
    )
    p.add_argument(
        "--minutes", type=int, default=60, help="Validez en minutos (por defecto 60)"
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    roles = [r.strip() for r in args.roles.split(",") if r.strip()]
    token = create_access_token(
        {"sub": args.sub, "roles": roles}, expires_delta=timedelta(minutes=args.minutes)
    )
    print(token)


if __name__ == "__main__":
    main()
