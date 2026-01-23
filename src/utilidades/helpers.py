"""
Módulo de utilidades generales (Helpers).

Módulo con funciones de apoyo no ligadas a la lógica de la aplicación,
como generación de ids, manejo de directorios, etc.
"""

import hashlib
import uuid
from pathlib import Path


def crear_directorio(ruta: str) -> None:
    """
    Crea las carpetas de una ruta en caso de no existir.

    Args:
        ruta (str): Ruta a crear.
    """
    path = Path(ruta).parent
    path.mkdir(parents=True, exist_ok=True)


def generar_id() -> str:
    """
    Genera un identificador único.

    Returns:
        str: Identificador único (id).
    """
    return str(uuid.uuid4())


def hash_clave(clave: str) -> str:
    """
    Obtiene el hash para la clave del usuario.

    Args:
        clave (str): Clave del usuario.

    Returns:
        str: Hash de la clave.
    """
    hash_objeto = hashlib.sha256(clave.encode("utf-8"))
    return hash_objeto.hexdigest()
