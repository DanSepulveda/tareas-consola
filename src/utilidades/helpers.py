"""
Módulo de utilidades generales (Helpers).

Módulo con funciones de apoyo no ligadas a la lógica de la aplicación,
como generación de ids, manejo de directorios, etc.
"""

import hashlib
import uuid
from datetime import date
from pathlib import Path


def contar_dias_entre(fecha_final: str, fecha_inicial: str) -> int:
    """Obtiene la cantidad de días entre dos fechas con formato dd-mm-aaaa"""
    formato = "%d-%m-%Y"
    try:
        inicial_formateada = date.strptime(fecha_inicial, formato)
        final_formateada = date.strptime(fecha_final, formato)
        return (final_formateada - inicial_formateada).days
    except ValueError as e:
        raise ValueError("Fechas con formato inválido.") from e


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
