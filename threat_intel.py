"""
threat_intel.py - Inteligencia de amenazas mediante geolocalización de IPs.
Módulo 5: Integración de APIs y seguridad.

Consulta ipinfo.io para obtener país y organización de IPs atacantes
y genera una tabla de amenazas en consola.
"""

import requests
from log_parser import parse_failed_logins


def geolocate_ip(ip: str) -> dict[str, str]:
    """
    Consulta ipinfo.io para obtener información geográfica de una IP.

    Devuelve un diccionario con country, org y city.
    En caso de error devuelve valores 'N/A'.
    """
    default: dict[str, str] = {"country": "N/A", "org": "N/A", "city": "N/A"}
    try:
        response = requests.get(
            f"https://ipinfo.io/{ip}/json",
            timeout=5,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        data: dict[str, str] = response.json()
        return {
            "country": data.get("country", "N/A"),
            "org": data.get("org", "N/A"),
            "city": data.get("city", "N/A"),
        }
    except requests.exceptions.ConnectionError:
        print(f"  [WARN] Sin conexión a internet para geolocalizar {ip}.")
        return default
    except requests.exceptions.Timeout:
        print(f"  [WARN] Timeout al consultar {ip}.")
        return default
    except requests.exceptions.HTTPError as e:
        print(f"  [WARN] Error HTTP para {ip}: {e}")
        return default
    except Exception as e:
        print(f"  [WARN] Error inesperado para {ip}: {e}")
        return default


def build_threat_table(
    log_path: str = "logs/auth.log",
    top_n: int = 10,
) -> list[dict[str, str | int]]:
    """
    Combina el análisis de logs con la geolocalización.

    Devuelve una lista de dicts con ip, intentos, país, ciudad y organización.
    Limita la consulta a las top_n IPs más activas para no saturar la API.
    """
    ip_counts: dict[str, int] = parse_failed_logins(log_path)
    top_ips: list[tuple[str, int]] = list(ip_counts.items())[:top_n]

    table: list[dict[str, str | int]] = []
    print(f"\n[*] Geolocalizando {len(top_ips)} IPs atacantes...")

    for ip, count in top_ips:
        print(f"  → Consultando {ip}...", end=" ", flush=True)
        geo = geolocate_ip(ip)
        print(f"{geo['country']} / {geo['org']}")
        table.append(
            {
                "ip": ip,
                "intentos": count,
                "pais": geo["country"],
                "ciudad": geo["city"],
                "organizacion": geo["org"],
            }
        )

    return table


def print_threat_table(table: list[dict[str, str | int]]) -> None:
    """Imprime la tabla de amenazas formateada en consola."""
    col_ip = 20
    col_int = 10
    col_pais = 8
    col_ciudad = 15
    col_org = 35
    total = col_ip + col_int + col_pais + col_ciudad + col_org + 10

    print(f"\n{'='*total}")
    print(f"  TABLA DE AMENAZAS SSH")
    print(f"{'='*total}")
    header = (
        f"  {'IP':<{col_ip}} {'Intentos':>{col_int}}  "
        f"{'País':<{col_pais}}  {'Ciudad':<{col_ciudad}}  {'Organización':<{col_org}}"
    )
    print(header)
    print(f"{'-'*total}")
    for row in table:
        org = str(row["organizacion"])[:col_org]
        ciudad = str(row["ciudad"])[:col_ciudad]
        print(
            f"  {row['ip']:<{col_ip}} {row['intentos']:>{col_int}}  "
            f"{row['pais']:<{col_pais}}  {ciudad:<{col_ciudad}}  {org:<{col_org}}"
        )
    print(f"{'='*total}\n")
