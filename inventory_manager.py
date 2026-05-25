"""
inventory_manager.py - Gestor de inventario con Pandas.
Módulo 6 (continuación): Carga, filtra, agrupa y analiza el inventario CSV.
"""

import pandas as pd
from pathlib import Path


def load_inventory(csv_path: str = "inventory.csv") -> pd.DataFrame:
    """Carga el inventario CSV en un DataFrame de Pandas."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontró '{csv_path}'. Ejecuta generate_inventory.py primero."
        )
    df = pd.read_csv(path, parse_dates=["last_update"])
    print(f"[OK] Inventario cargado: {len(df)} servidores.")
    return df


def filter_windows_servers(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve solo los servidores con Windows Server."""
    mask = df["os"].str.contains("Windows Server", case=False, na=False)
    result = df[mask].copy()
    print(f"[Filtro] Servidores Windows Server: {len(result)}")
    return result


def filter_low_ram(df: pd.DataFrame, threshold_gb: int = 4) -> pd.DataFrame:
    """Devuelve servidores con RAM menor o igual al umbral indicado."""
    result = df[df["ram_gb"] <= threshold_gb].copy()
    print(f"[Filtro] Servidores con ≤ {threshold_gb} GB de RAM: {len(result)}")
    return result


def filter_vulnerable(df: pd.DataFrame) -> pd.DataFrame:
    """
    Servidores considerados vulnerables u obsoletos:
    - Windows Server con cualquier versión, o
    - RAM ≤ 4 GB, o
    - Estado 'obsoleto'
    """
    mask = (
        df["os"].str.contains("Windows Server", case=False, na=False)
        | (df["ram_gb"] <= 4)
        | (df["status"] == "obsoleto")
    )
    result = df[mask].copy()
    print(f"[Filtro] Servidores vulnerables/obsoletos: {len(result)}")
    return result


def group_by_department(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa por departamento y cuenta cuántos servidores tiene cada área."""
    grouped = (
        df.groupby("department")
        .agg(
            total=("hostname", "count"),
            activos=("status", lambda s: (s == "activo").sum()),
            obsoletos=("status", lambda s: (s == "obsoleto").sum()),
            ram_media_gb=("ram_gb", "mean"),
        )
        .reset_index()
        .sort_values("total", ascending=False)
    )
    grouped["ram_media_gb"] = grouped["ram_media_gb"].round(1)
    return grouped


def print_dataframe(df: pd.DataFrame, title: str, max_rows: int = 10) -> None:
    """Imprime un DataFrame con un título y opcionalmente limita filas."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(df.head(max_rows).to_string(index=False))
    if len(df) > max_rows:
        print(f"  ... ({len(df) - max_rows} filas más)")
    print(f"{'='*60}\n")
