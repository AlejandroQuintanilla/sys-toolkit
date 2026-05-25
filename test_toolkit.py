"""
test_toolkit.py - Tests unitarios del SysAdmin Toolkit.
Módulo 8: Fiabilidad, pruebas unitarias y manejo de errores.

Ejecutar con: pytest test_toolkit.py -v
"""

import pytest
import tempfile
import os
from pathlib import Path


# ── Fixtures ──────────────────────────────────────────────────────────────────

SAMPLE_LOG_LINES = """May  5 03:21:10 srv-prod-01 sshd[4321]: Failed password for root from 185.220.101.45 port 52100 ssh2
May  5 03:22:01 srv-prod-01 sshd[4322]: Failed password for admin from 45.33.32.156 port 52200 ssh2
May  5 03:23:14 srv-prod-01 sshd[4323]: Failed password for root from 185.220.101.45 port 52300 ssh2
May  5 08:10:05 srv-prod-01 sshd[4324]: Accepted password for alejandro from 192.168.1.10 port 60000 ssh2
May  5 03:24:00 srv-prod-01 sshd[4325]: Failed password for ubuntu from 45.33.32.156 port 52400 ssh2
May  5 03:25:11 srv-prod-01 sshd[4326]: Failed password for pi from 10.0.0.99 port 52500 ssh2
"""


@pytest.fixture
def temp_log_file(tmp_path: Path) -> str:
    """Crea un archivo de log temporal con líneas de prueba."""
    log_file = tmp_path / "test_auth.log"
    log_file.write_text(SAMPLE_LOG_LINES, encoding="utf-8")
    return str(log_file)


@pytest.fixture
def temp_csv(tmp_path: Path) -> str:
    """Crea un CSV de inventario mínimo para tests."""
    csv_content = (
        "hostname,ip,mac,os,ram_gb,cpu_cores,disk_gb,department,services,status,responsible,last_update\n"
        "srv-INF-0001,10.0.0.1,AA:BB:CC:DD:EE:01,Ubuntu Server 22.04,16,4,200,INF,SSH|Nginx,activo,Ana López,2024-01-15\n"
        "srv-INF-0002,10.0.0.2,AA:BB:CC:DD:EE:02,Windows Server 2022,8,2,100,INF,RDP|IIS,activo,Carlos Ruiz,2024-02-20\n"
        "srv-DES-0001,10.0.1.1,AA:BB:CC:DD:EE:03,Ubuntu Server 20.04,2,1,50,DES,SSH,obsoleto,María García,2022-06-01\n"
        "srv-DES-0002,10.0.1.2,AA:BB:CC:DD:EE:04,Windows Server 2019,4,2,100,DES,RDP,mantenimiento,Pedro Sánchez,2023-11-10\n"
        "srv-SEG-0001,10.0.2.1,AA:BB:CC:DD:EE:05,Debian 11,32,8,500,SEG,SSH|Docker,activo,Laura Martín,2024-03-01\n"
    )
    csv_file = tmp_path / "test_inventory.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    return str(csv_file)


# ── Tests: log_parser ─────────────────────────────────────────────────────────

class TestLogParser:

    def test_parse_returns_dict(self, temp_log_file: str) -> None:
        """parse_failed_logins debe devolver un diccionario."""
        from log_parser import parse_failed_logins
        result = parse_failed_logins(temp_log_file)
        assert isinstance(result, dict)

    def test_correct_ip_count(self, temp_log_file: str) -> None:
        """La IP 185.220.101.45 aparece 2 veces y 45.33.32.156 aparece 2 veces."""
        from log_parser import parse_failed_logins
        result = parse_failed_logins(temp_log_file)
        assert result["185.220.101.45"] == 2
        assert result["45.33.32.156"] == 2
        assert result["10.0.0.99"] == 1

    def test_accepted_logins_excluded(self, temp_log_file: str) -> None:
        """Las IPs con 'Accepted password' no deben aparecer en el conteo."""
        from log_parser import parse_failed_logins
        result = parse_failed_logins(temp_log_file)
        assert "192.168.1.10" not in result

    def test_sorted_descending(self, temp_log_file: str) -> None:
        """El diccionario debe estar ordenado de mayor a menor intentos."""
        from log_parser import parse_failed_logins
        result = parse_failed_logins(temp_log_file)
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True)

    def test_unique_ips_set(self, temp_log_file: str) -> None:
        """get_unique_ips debe devolver un set con exactamente 3 IPs."""
        from log_parser import get_unique_ips
        result = get_unique_ips(temp_log_file)
        assert isinstance(result, set)
        assert len(result) == 3

    def test_file_not_found_raises(self) -> None:
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        from log_parser import parse_failed_logins
        with pytest.raises(FileNotFoundError):
            parse_failed_logins("ruta/que/no/existe.log")


# ── Tests: network_models ─────────────────────────────────────────────────────

class TestNetworkModels:

    def test_router_creation(self) -> None:
        """Router debe crearse con todos sus atributos."""
        from network_models import Router
        r = Router("router-01", "192.168.1.1", "AA:BB:CC", "Cisco ISR", "1.2.3.4", "v1.0")
        assert r.hostname == "router-01"
        assert r.wan_ip == "1.2.3.4"

    def test_server_creation(self) -> None:
        """Server debe crearse con todos sus atributos."""
        from network_models import Server
        s = Server("srv-01", "10.0.0.1", "BB:CC:DD", "Ubuntu 22.04", 16, ["SSH"])
        assert s.ram_gb == 16
        assert "SSH" in s.services

    def test_polymorphism_audit(self, capsys: pytest.CaptureFixture[str]) -> None:
        """audit_device() debe imprimir texto diferente según la clase."""
        from network_models import Router, Server
        r = Router("router-01", "192.168.1.1", "AA:BB", "Cisco", "1.2.3.4", "v1")
        s = Server("srv-01", "10.0.0.1", "BB:CC", "Ubuntu", 8, ["SSH"])
        r.audit_device()
        s.audit_device()
        captured = capsys.readouterr()
        assert "ROUTER" in captured.out
        assert "SERVER" in captured.out

    def test_inheritance(self) -> None:
        """Router y Server deben ser instancias de NetworkDevice."""
        from network_models import NetworkDevice, Router, Server
        r = Router("r", "1.1.1.1", "AA", "Cisco", "2.2.2.2", "v1")
        s = Server("s", "1.1.1.2", "BB", "Linux", 8, [])
        assert isinstance(r, NetworkDevice)
        assert isinstance(s, NetworkDevice)


# ── Tests: inventory_manager ──────────────────────────────────────────────────

class TestInventoryManager:

    def test_load_inventory(self, temp_csv: str) -> None:
        """load_inventory debe devolver un DataFrame con las filas correctas."""
        from inventory_manager import load_inventory
        df = load_inventory(temp_csv)
        assert len(df) == 5

    def test_filter_windows(self, temp_csv: str) -> None:
        """filter_windows_servers debe devolver solo los Windows Server."""
        from inventory_manager import load_inventory, filter_windows_servers
        df = load_inventory(temp_csv)
        result = filter_windows_servers(df)
        assert len(result) == 2
        assert all("Windows" in os for os in result["os"])

    def test_filter_low_ram(self, temp_csv: str) -> None:
        """filter_low_ram debe devolver solo los servidores con ≤ 4 GB."""
        from inventory_manager import load_inventory, filter_low_ram
        df = load_inventory(temp_csv)
        result = filter_low_ram(df, threshold_gb=4)
        assert all(r <= 4 for r in result["ram_gb"])

    def test_group_by_department(self, temp_csv: str) -> None:
        """group_by_department debe tener 3 grupos (INF, DES, SEG)."""
        from inventory_manager import load_inventory, group_by_department
        df = load_inventory(temp_csv)
        grouped = group_by_department(df)
        assert len(grouped) == 3
        assert set(grouped["department"]) == {"INF", "DES", "SEG"}

    def test_load_nonexistent_raises(self) -> None:
        """Debe lanzar FileNotFoundError si el CSV no existe."""
        from inventory_manager import load_inventory
        with pytest.raises(FileNotFoundError):
            load_inventory("no_existe.csv")


# ── Tests: os_utils ───────────────────────────────────────────────────────────

class TestOsUtils:

    def test_disk_check_returns_dict(self) -> None:
        """check_disk_space debe devolver un diccionario con las claves esperadas."""
        from os_utils import check_disk_space
        info = check_disk_space("/")
        assert "total_gb" in info
        assert "free_pct" in info
        assert "alert" in info

    def test_disk_check_invalid_partition(self) -> None:
        """check_disk_space debe devolver un dict vacío para particiones inexistentes."""
        from os_utils import check_disk_space
        info = check_disk_space("/particion/que/no/existe")
        assert info == {}

    def test_ping_invalid_ip(self) -> None:
        """check_ping a una IP inválida/inalcanzable debe devolver False."""
        from os_utils import check_ping
        result = check_ping("192.0.2.1")  # IP reservada para documentación, nunca responde
        assert result is False
