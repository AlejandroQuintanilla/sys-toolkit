"""
log_parser.py - Auditor de logs SSH.
Módulo 3: Parseo de logs y estructuras de datos.

Lee auth.log línea a línea (sin saturar RAM), extrae IPs fallidas,
las almacena en un Set para eliminar duplicados y construye un
diccionario con el conteo de intentos por IP.
"""

from pathlib import Path


def parse_failed_logins(log_path: str = "logs/auth.log") -> dict[str, int]:
    """
    Lee el archivo de log línea a línea y cuenta los intentos fallidos por IP.

    Devuelve un diccionario {ip: num_intentos} ordenado de mayor a menor.
    """
    failed_ips: set[str] = set()
    ip_count: dict[str, int] = {}

    path = Path(log_path)
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo de log: '{log_path}'. "
            "Ejecuta primero generate_auth_log.py"
        )

    with open(path, "r", encoding="utf-8") as log_file:
        for line in log_file:
            line = line.strip()
            # Filtramos solo las líneas con intentos fallidos
            if "Failed password" not in line:
                continue

            # Extraemos la IP: el token tras "from"
            parts: list[str] = line.split()
            try:
                from_index: int = parts.index("from")
                ip: str = parts[from_index + 1]
            except (ValueError, IndexError):
                continue

            # Set: elimina duplicados automáticamente
            failed_ips.add(ip)

            # Dict: conteo de intentos
            ip_count[ip] = ip_count.get(ip, 0) + 1

    # Devolvemos ordenado de mayor a menor número de intentos
    sorted_counts: dict[str, int] = dict(
        sorted(ip_count.items(), key=lambda x: x[1], reverse=True)
    )
    return sorted_counts


def get_unique_ips(log_path: str = "logs/auth.log") -> set[str]:
    """Devuelve el conjunto de IPs únicas con intentos fallidos."""
    counts = parse_failed_logins(log_path)
    return set(counts.keys())


def print_failed_summary(ip_counts: dict[str, int]) -> None:
    """Imprime un resumen en consola con las IPs atacantes y sus intentos."""
    print(f"\n{'='*50}")
    print(f"  RESUMEN DE INTENTOS SSH FALLIDOS")
    print(f"{'='*50}")
    print(f"  IPs únicas detectadas: {len(ip_counts)}")
    print(f"  Total de intentos    : {sum(ip_counts.values())}")
    print(f"{'-'*50}")
    print(f"  {'IP':<20} {'Intentos':>10}")
    print(f"{'-'*50}")
    for ip, count in ip_counts.items():
        print(f"  {ip:<20} {count:>10}")
    print(f"{'='*50}\n")
