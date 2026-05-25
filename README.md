# 🛡️ SysAdmin Toolkit — ASIR

Kit de herramientas para administradores de sistemas en Python. Incluye un auditor de seguridad SSH, gestión de inventario de red con Excel, geolocalización de IPs amenazantes y un menú CLI interactivo.

---

## 📁 Estructura del proyecto

```
sys_toolkit/
├── sys_toolkit.py          # Menú interactivo principal (punto de entrada)
├── os_utils.py             # Ping y comprobación de disco
├── log_parser.py           # Auditor de logs SSH
├── network_models.py       # Clases OOP: Router y Server
├── threat_intel.py         # Geolocalización de IPs via ipinfo.io
├── generate_inventory.py   # Generador de inventario CSV (Faker)
├── inventory_manager.py    # Análisis de inventario con Pandas
├── report_generator.py     # Exportación a Excel ejecutivo
├── generate_auth_log.py    # Generador de auth.log simulado
├── test_toolkit.py         # Tests unitarios (pytest) — 18 tests
├── requirements.txt        # Dependencias del proyecto
├── .gitignore
├── inventory.csv           # Inventario generado (1000 servidores)
├── logs/
│   └── auth.log            # Log SSH simulado (850 entradas)
├── output/
│   └── informe_*.xlsx      # Informes Excel generados
└── docs/
    └── python-sysadmin.md  # Documentación técnica
```

---

## ⚙️ Instalación

### Requisitos
- Python 3.10 o superior
- pip

### Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/sys-toolkit.git
cd sys-toolkit

# 2. Crea el entorno virtual
python3 -m venv venv

# 3. Actívalo
# En Linux/macOS:
source venv/bin/activate
# En Windows (Git Bash):
source venv/Scripts/activate
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# 4. Instala las dependencias
pip install -r requirements.txt

# 5. Genera los archivos de datos iniciales
python generate_auth_log.py
python generate_inventory.py
```

---

## 🚀 Uso

### Menú interactivo

```bash
python sys_toolkit.py
```

Opciones disponibles:

| # | Función |
|---|---------|
| 1 | Ping a una IP |
| 2 | Espacio en disco |
| 3 | Auditar logs SSH |
| 4 | Geolocalizar IPs atacantes |
| 5 | Auditoría OOP de dispositivos |
| 6 | Generar inventario CSV |
| 7 | Analizar inventario con Pandas |
| 8 | Generar informe Excel |
| 9 | Ejecutar tests unitarios |

### Módulos de forma independiente

```bash
# Generar informe Excel directamente
python report_generator.py

# Ejecutar el planificador mensual automático
python report_generator.py --schedule

# Pasar los tests
python -m pytest test_toolkit.py -v
```

---

## 🧪 Tests

```bash
python -m pytest test_toolkit.py -v
```

**18 tests** cubriendo: `log_parser`, `network_models`, `inventory_manager` y `os_utils`.

```
18 passed in 0.64s
```

---

## 📦 Dependencias

| Librería | Uso |
|---|---|
| `requests` | Llamadas a la API de ipinfo.io |
| `pandas` | Análisis y filtrado del inventario |
| `openpyxl` | Generación de informes Excel |
| `Faker` | Datos ficticios para el inventario |
| `schedule` | Planificación mensual automática |
| `pytest` | Tests unitarios |
| `mypy` | Verificación de type hints |

---

## 📄 Documentación

- [Por qué un sysadmin necesita Python](docs/python-sysadmin.md)

---

## 👤 Autor

Alejandro Quintanilla Cobo — Ciclo Formativo de Grado Superior ASIR  
Prácticas en Corner Studios
