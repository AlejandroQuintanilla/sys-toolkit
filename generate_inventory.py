"""
generate_inventory.py - Generador de inventario CSV de servidores ficticios.
Módulo 6: Manipulación masiva de inventarios.

Usa Faker, csv y random para generar 1000 filas de servidores de empresa.
"""

import csv
import random
from pathlib import Path
from faker import Faker

fake = Faker("es_ES")
random.seed(0)

OS_OPTIONS: list[str] = [
    "Ubuntu Server 22.04",
    "Ubuntu Server 20.04",
    "CentOS 7",
    "Debian 11",
    "Windows Server 2022",
    "Windows Server 2019",
    "Windows Server 2016",
    "Red Hat Enterprise Linux 9",
]

DEPARTMENTS: list[str] = [
    "Infraestructura",
    "Desarrollo",
    "Base de Datos",
    "Seguridad",
    "Finanzas",
    "RRHH",
    "Operaciones",
    "Marketing",
]

SERVICES: list[list[str]] = [
    ["SSH", "Nginx", "Docker"],
    ["SSH", "Apache", "MySQL"],
    ["RDP", "IIS", "MSSQL"],
    ["SSH", "PostgreSQL"],
    ["SSH", "MongoDB", "Redis"],
    ["RDP", "Active Directory"],
    ["SSH", "Kubernetes", "Prometheus"],
    ["SSH", "Jenkins", "Git"],
]

RAM_OPTIONS: list[int] = [2, 4, 8, 16, 32, 64, 128]
CPU_OPTIONS: list[int] = [1, 2, 4, 8, 16, 32]
DISK_OPTIONS: list[int] = [50, 100, 200, 500, 1000, 2000]
STATUS_OPTIONS: list[str] = ["activo", "activo", "activo", "mantenimiento", "obsoleto"]


def generate_ip() -> str:
    return f"10.{random.randint(0,10)}.{random.randint(0,255)}.{random.randint(1,254)}"


def generate_mac() -> str:
    return ":".join(f"{random.randint(0,255):02X}" for _ in range(6))


def generate_inventory(rows: int = 1000, output_path: str = "inventory.csv") -> None:
    """Genera un CSV de inventario con el número de filas indicado."""
    fieldnames: list[str] = [
        "hostname",
        "ip",
        "mac",
        "os",
        "ram_gb",
        "cpu_cores",
        "disk_gb",
        "department",
        "services",
        "status",
        "responsible",
        "last_update",
    ]

    path = Path(output_path)
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, rows + 1):
            dept_code = random.choice(DEPARTMENTS)[:3].upper()
            hostname = f"srv-{dept_code}-{i:04d}"
            os_choice = random.choice(OS_OPTIONS)
            services = random.choice(SERVICES)

            writer.writerow(
                {
                    "hostname": hostname,
                    "ip": generate_ip(),
                    "mac": generate_mac(),
                    "os": os_choice,
                    "ram_gb": random.choice(RAM_OPTIONS),
                    "cpu_cores": random.choice(CPU_OPTIONS),
                    "disk_gb": random.choice(DISK_OPTIONS),
                    "department": dept_code,
                    "services": "|".join(services),
                    "status": random.choice(STATUS_OPTIONS),
                    "responsible": fake.name(),
                    "last_update": fake.date_between(
                        start_date="-3y", end_date="today"
                    ).strftime("%Y-%m-%d"),
                }
            )

    print(f"[OK] Inventario generado: {path} ({rows} servidores)")


if __name__ == "__main__":
    generate_inventory()
