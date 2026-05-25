"""
os_utils.py - Utilidades de sistema operativo para el SysAdmin Toolkit.
Módulo 2: Automatización del sistema operativo.
"""

import os
import shutil
import subprocess


def check_ping(ip: str) -> bool:
    """
    Ejecuta un ping -c 1 al host indicado.
    Devuelve True si responde, False si falla.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except FileNotFoundError:
        # ping no disponible en el sistema
        print("[ERROR] El comando 'ping' no está disponible en este sistema.")
        return False


def check_disk_space(partition: str = "/") -> dict[str, float | str | bool]:
    """
    Comprueba el espacio libre en disco de la partición indicada.
    Lanza una alerta si el espacio libre es menor al 20%.

    Devuelve un diccionario con:
      - partition: ruta de la partición
      - total_gb: espacio total en GB
      - used_gb: espacio usado en GB
      - free_gb: espacio libre en GB
      - free_pct: porcentaje libre
      - alert: True si el espacio libre es < 20%
    """
    try:
        usage = shutil.disk_usage(partition)
    except FileNotFoundError:
        print(f"[ERROR] La partición '{partition}' no existe.")
        return {}

    total_gb: float = usage.total / (1024 ** 3)
    used_gb: float = usage.used / (1024 ** 3)
    free_gb: float = usage.free / (1024 ** 3)
    free_pct: float = (usage.free / usage.total) * 100
    alert: bool = free_pct < 20.0

    info: dict[str, float | str | bool] = {
        "partition": partition,
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2),
        "free_pct": round(free_pct, 2),
        "alert": alert,
    }

    if alert:
        print(
            f"[ALERTA] Espacio libre en '{partition}': {free_pct:.1f}% "
            f"({free_gb:.2f} GB) — por debajo del umbral del 20%."
        )
    return info


def print_disk_info(info: dict[str, float | str | bool]) -> None:
    """Imprime el resumen de uso de disco en consola."""
    if not info:
        return
    print(f"\n{'='*45}")
    print(f"  Partición : {info['partition']}")
    print(f"  Total     : {info['total_gb']} GB")
    print(f"  Usado     : {info['used_gb']} GB")
    print(f"  Libre     : {info['free_gb']} GB  ({info['free_pct']}%)")
    estado = "⚠️  ALERTA" if info["alert"] else "✅ OK"
    print(f"  Estado    : {estado}")
    print(f"{'='*45}\n")
