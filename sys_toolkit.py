"""
sys_toolkit.py - SysAdmin Toolkit: menú interactivo CLI.
Módulo 1: Punto de entrada principal con type hints estrictos.

Ejecutar con: python sys_toolkit.py
"""

import sys
from typing import Callable


# ── Tipo para opciones del menú ───────────────────────────────────────────────

MenuItem = tuple[str, Callable[[], None]]


# ── Funciones de cada opción ──────────────────────────────────────────────────

def menu_ping() -> None:
    """Opción 1: Comprobar conectividad con ping."""
    from os_utils import check_ping
    ip: str = input("  Introduce la IP o hostname a comprobar: ").strip()
    if not ip:
        print("  [ERROR] IP vacía.")
        return
    print(f"  Haciendo ping a {ip}...")
    ok: bool = check_ping(ip)
    if ok:
        print(f"  ✅ {ip} responde correctamente.")
    else:
        print(f"  ❌ {ip} no responde o es inalcanzable.")


def menu_disk() -> None:
    """Opción 2: Comprobar espacio en disco."""
    from os_utils import check_disk_space, print_disk_info
    partition: str = input("  Partición a comprobar [/]: ").strip() or "/"
    info: dict = check_disk_space(partition)
    print_disk_info(info)


def menu_parse_logs() -> None:
    """Opción 3: Auditar logs SSH."""
    from log_parser import parse_failed_logins, print_failed_summary
    log_path: str = input(
        "  Ruta del log [logs/auth.log]: "
    ).strip() or "logs/auth.log"
    try:
        counts: dict[str, int] = parse_failed_logins(log_path)
        print_failed_summary(counts)
    except FileNotFoundError as e:
        print(f"  [ERROR] {e}")


def menu_threat_intel() -> None:
    """Opción 4: Geolocalizar IPs atacantes (requiere internet)."""
    from threat_intel import build_threat_table, print_threat_table
    log_path: str = input(
        "  Ruta del log [logs/auth.log]: "
    ).strip() or "logs/auth.log"
    raw: str = input("  ¿Cuántas IPs top consultar? [10]: ").strip()
    top_n: int = int(raw) if raw.isdigit() else 10
    try:
        table = build_threat_table(log_path, top_n)
        print_threat_table(table)
    except FileNotFoundError as e:
        print(f"  [ERROR] {e}")


def menu_network_audit() -> None:
    """Opción 5: Auditoría de dispositivos de red (demo)."""
    from network_models import demo_audit
    demo_audit()


def menu_generate_inventory() -> None:
    """Opción 6: Generar inventario CSV de servidores ficticios."""
    from generate_inventory import generate_inventory
    raw: str = input("  Número de servidores a generar [1000]: ").strip()
    rows: int = int(raw) if raw.isdigit() else 1000
    generate_inventory(rows=rows)


def menu_analyze_inventory() -> None:
    """Opción 7: Analizar inventario CSV con Pandas."""
    from inventory_manager import (
        load_inventory,
        filter_windows_servers,
        filter_low_ram,
        group_by_department,
        print_dataframe,
    )
    csv_path: str = input(
        "  Ruta del CSV [inventory.csv]: "
    ).strip() or "inventory.csv"
    try:
        df = load_inventory(csv_path)
        print_dataframe(filter_windows_servers(df), "Servidores Windows Server")
        print_dataframe(filter_low_ram(df), "Servidores con ≤ 4 GB de RAM")
        print_dataframe(group_by_department(df), "Servidores por departamento")
    except FileNotFoundError as e:
        print(f"  [ERROR] {e}")


def menu_generate_report() -> None:
    """Opción 8: Generar informe Excel ejecutivo."""
    from report_generator import generate_excel_report
    csv_path: str = input(
        "  Ruta del CSV [inventory.csv]: "
    ).strip() or "inventory.csv"
    try:
        path: str = generate_excel_report(csv_path)
        print(f"  📄 Informe disponible en: {path}")
    except FileNotFoundError as e:
        print(f"  [ERROR] {e}")


def menu_run_tests() -> None:
    """Opción 9: Ejecutar tests unitarios con pytest."""
    import subprocess
    subprocess.run(["python", "-m", "pytest", "test_toolkit.py", "-v"])


# ── Menú principal ────────────────────────────────────────────────────────────

MENU_OPTIONS: list[MenuItem] = [
    ("Comprobar ping a una IP", menu_ping),
    ("Comprobar espacio en disco", menu_disk),
    ("Auditar logs SSH (parser)", menu_parse_logs),
    ("Geolocalizar IPs atacantes (requiere internet)", menu_threat_intel),
    ("Auditoría de dispositivos de red (demo OOP)", menu_network_audit),
    ("Generar inventario CSV ficticio", menu_generate_inventory),
    ("Analizar inventario CSV con Pandas", menu_analyze_inventory),
    ("Generar informe Excel ejecutivo", menu_generate_report),
    ("Ejecutar tests unitarios (pytest)", menu_run_tests),
]


def print_menu() -> None:
    """Imprime el menú principal."""
    print("\n" + "╔" + "═" * 55 + "╗")
    print("║" + "  🛡️  SYSADMIN TOOLKIT — ASIR Practices".center(55) + "║")
    print("╠" + "═" * 55 + "╣")
    for i, (label, _) in enumerate(MENU_OPTIONS, start=1):
        print(f"║  {i:>2}. {label:<49}║")
    print("║" + "─" * 55 + "║")
    print("║   0. Salir" + " " * 44 + "║")
    print("╚" + "═" * 55 + "╝")


def main() -> None:
    """Bucle principal del menú interactivo."""
    print("\n  Bienvenido al SysAdmin Toolkit.")

    while True:
        print_menu()
        raw: str = input("\n  Elige una opción: ").strip()

        if raw == "0":
            print("\n  Hasta luego.\n")
            sys.exit(0)

        if not raw.isdigit() or not (1 <= int(raw) <= len(MENU_OPTIONS)):
            print(f"  [ERROR] Opción no válida. Introduce un número del 0 al {len(MENU_OPTIONS)}.")
            continue

        option_index: int = int(raw) - 1
        label, func = MENU_OPTIONS[option_index]
        print(f"\n{'─'*55}")
        print(f"  ▶ {label}")
        print(f"{'─'*55}")
        func()
        input("\n  [Enter para continuar]")


if __name__ == "__main__":
    main()
