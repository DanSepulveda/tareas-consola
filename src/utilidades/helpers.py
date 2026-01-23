"""
Módulo de utilidades generales (Helpers).

Módulo con funciones de apoyo no ligadas a la lógica de la aplicación,
como generación de ids, manejo de directorios, etc.
"""

import hashlib
import uuid
from pathlib import Path


def crear_directorio(ruta: str) -> None:
    """Crea las carpetas de la ruta indicada."""
    path = Path(ruta).parent
    path.mkdir(parents=True, exist_ok=True)


def generar_hash(clave: str) -> str:
    """Genera un hash para la clave del usuario."""
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


def generar_id() -> str:
    """Genera un identificador único."""
    return str(uuid.uuid4())
