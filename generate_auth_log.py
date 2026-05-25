#!/usr/bin/env python3
"""
generate_auth_log.py - Genera un auth.log simulado de Linux con intentos SSH.
Ejecuta este script una vez para crear logs/auth.log antes de usar log_parser.py.
"""

import random
from pathlib import Path

FAILED_IPS: list[str] = [
    "185.220.101.45",
    "192.168.1.105",
    "45.33.32.156",
    "103.21.244.0",
    "185.220.101.45",  # repetida para simular ataques continuados
    "198.51.100.77",
    "203.0.113.12",
    "45.33.32.156",
    "10.0.0.99",
    "185.220.101.45",
]

SUCCESS_IPS: list[str] = [
    "192.168.1.10",
    "10.10.0.5",
]

MONTHS: list[str] = ["May"] * 30
DAYS: list[int] = list(range(1, 31))
HOSTS: list[str] = ["srv-prod-01", "srv-db-02"]
USERS_FAILED: list[str] = ["root", "admin", "ubuntu", "pi", "test", "deploy"]
USERS_OK: list[str] = ["alejandro", "sysadmin"]

lines: list[str] = []

random.seed(42)

for _ in range(800):
    month = "May"
    day = random.choice(DAYS)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    host = random.choice(HOSTS)
    ip = random.choice(FAILED_IPS)
    user = random.choice(USERS_FAILED)
    port = random.randint(1024, 65535)
    timestamp = f"{month} {day:2d} {hour:02d}:{minute:02d}:{second:02d}"
    lines.append(
        f"{timestamp} {host} sshd[{random.randint(1000,9999)}]: "
        f"Failed password for {user} from {ip} port {port} ssh2"
    )

for _ in range(50):
    month = "May"
    day = random.choice(DAYS)
    hour = random.randint(8, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    host = random.choice(HOSTS)
    ip = random.choice(SUCCESS_IPS)
    user = random.choice(USERS_OK)
    port = random.randint(1024, 65535)
    timestamp = f"{month} {day:2d} {hour:02d}:{minute:02d}:{second:02d}"
    lines.append(
        f"{timestamp} {host} sshd[{random.randint(1000,9999)}]: "
        f"Accepted password for {user} from {ip} port {port} ssh2"
    )

# Mezclar líneas para simular un log real
random.shuffle(lines)

output_path = Path("logs/auth.log")
output_path.parent.mkdir(exist_ok=True)
output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"[OK] Generado {output_path} con {len(lines)} entradas.")
