"""
Módulo de utilidades generales (Helpers).

Módulo con funciones de apoyo no ligadas a la lógica de la aplicación,
como generación de ids, manejo de directorios, etc.
"""

import hashlib
import uuid
import webbrowser
from datetime import date
from pathlib import Path


def abrir_navegador(ruta: str):
    try:
        path = Path(ruta).resolve().as_uri()
        exito = webbrowser.open(path)
        if not exito:
            raise Exception("Error al abrir el navegador")
    except Exception:
        pass


def dias_desde_hoy(fecha: str) -> int:
    """Cantidad de días entre la fecha indicada en formato dd-mm-aaaa y hoy."""
    try:
        fecha_formateada = date.strptime(fecha, "%d-%m-%Y")
        return (fecha_formateada - date.today()).days
    except ValueError as e:
        raise ValueError("Fecha con formato inválido.") from e


def generar_hash(clave: str) -> str:
    """Genera un hash para la clave del usuario."""
    return hashlib.sha256(clave.encode("utf-8")).hexdigest()


def generar_id() -> str:
    """Genera un identificador único."""
    return str(uuid.uuid4())
