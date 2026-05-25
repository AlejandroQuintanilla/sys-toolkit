"""
network_models.py - Modelos de red orientados a objetos.
Módulo 4: Programación orientada a objetos en redes.

Clase base NetworkDevice con subclases Router y Server.
Demuestra herencia y polimorfismo mediante audit_device().
"""


class NetworkDevice:
    """Clase base que representa cualquier dispositivo de red."""

    def __init__(self, hostname: str, ip: str, mac: str) -> None:
        self.hostname: str = hostname
        self.ip: str = ip
        self.mac: str = mac

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(hostname={self.hostname!r}, ip={self.ip!r})"

    def audit_device(self) -> None:
        """Muestra directrices de seguridad genéricas. Sobreescrito en subclases."""
        print(f"\n[AUDIT] {self.hostname} ({self.ip})")
        print("  - Verificar que el firmware está actualizado.")
        print("  - Comprobar que los puertos innecesarios están cerrados.")
        print("  - Revisar los logs de acceso.")


class Router(NetworkDevice):
    """Representa un router de red con atributos específicos."""

    def __init__(
        self,
        hostname: str,
        ip: str,
        mac: str,
        model: str,
        wan_ip: str,
        firmware_version: str,
    ) -> None:
        super().__init__(hostname, ip, mac)
        self.model: str = model
        self.wan_ip: str = wan_ip
        self.firmware_version: str = firmware_version

    def audit_device(self) -> None:
        """Directrices de seguridad específicas para routers."""
        print(f"\n[AUDIT ROUTER] {self.hostname} | Modelo: {self.model}")
        print(f"  IP LAN : {self.ip}  |  IP WAN: {self.wan_ip}")
        print(f"  Firmware: {self.firmware_version}")
        print("  Directrices:")
        print("  ✔ Deshabilitar administración remota por HTTP (usar HTTPS).")
        print("  ✔ Cambiar credenciales por defecto del panel de administración.")
        print("  ✔ Activar firewall perimetral y bloquear puertos no usados.")
        print("  ✔ Revisar reglas NAT y port-forwarding activas.")
        print("  ✔ Actualizar firmware si la versión es anterior a la última estable.")


class Server(NetworkDevice):
    """Representa un servidor con atributos específicos."""

    def __init__(
        self,
        hostname: str,
        ip: str,
        mac: str,
        os: str,
        ram_gb: int,
        services: list[str],
    ) -> None:
        super().__init__(hostname, ip, mac)
        self.os: str = os
        self.ram_gb: int = ram_gb
        self.services: list[str] = services

    def audit_device(self) -> None:
        """Directrices de seguridad específicas para servidores."""
        print(f"\n[AUDIT SERVER] {self.hostname} | OS: {self.os}")
        print(f"  IP: {self.ip}  |  RAM: {self.ram_gb} GB")
        print(f"  Servicios activos: {', '.join(self.services)}")
        print("  Directrices:")
        print("  ✔ Mantener el sistema operativo y paquetes actualizados.")
        print("  ✔ Deshabilitar el acceso SSH como root (usar usuarios con sudo).")
        print("  ✔ Configurar fail2ban para bloquear IPs con intentos fallidos.")
        if "ssh" in [s.lower() for s in self.services]:
            print("  ✔ [SSH detectado] Usar autenticación por clave pública, no contraseña.")
        if "http" in [s.lower() for s in self.services]:
            print("  ✔ [HTTP detectado] Redirigir todo el tráfico a HTTPS.")
        print("  ✔ Revisar usuarios del sistema y eliminar cuentas inactivas.")


def demo_audit() -> None:
    """Crea dispositivos de ejemplo y ejecuta la auditoría."""
    devices: list[NetworkDevice] = [
        Router(
            hostname="router-core-01",
            ip="192.168.1.1",
            mac="AA:BB:CC:DD:EE:01",
            model="Cisco ISR 4321",
            wan_ip="203.0.113.1",
            firmware_version="16.09.04",
        ),
        Server(
            hostname="srv-web-01",
            ip="192.168.1.10",
            mac="AA:BB:CC:DD:EE:10",
            os="Ubuntu Server 22.04",
            ram_gb=16,
            services=["SSH", "HTTP", "HTTPS", "Nginx"],
        ),
        Server(
            hostname="srv-db-02",
            ip="192.168.1.11",
            mac="AA:BB:CC:DD:EE:11",
            os="Windows Server 2022",
            ram_gb=32,
            services=["RDP", "MSSQL", "WinRM"],
        ),
    ]

    print("\n" + "=" * 55)
    print("  AUDITORÍA DE DISPOSITIVOS DE RED")
    print("=" * 55)
    for device in devices:
        device.audit_device()  # Polimorfismo: cada clase imprime lo suyo
    print("\n" + "=" * 55)
