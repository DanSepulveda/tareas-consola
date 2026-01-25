import csv
import json
from pathlib import Path
from typing import Any


def cargar_csv(ruta: str) -> list:
    """
    Obtiene el contenido de un archivo .csv

    Args:
        ruta (str): Ruta del archivo que desea leer.

    Returns:
        list[dict]: Lista de diccionarios con los datos encontrados.
    """
    try:
        with open(ruta, encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)
    except FileNotFoundError:
        crear_directorio(ruta)
        return []


def cargar_json(ruta: str) -> Any | None:
    """
    Obtiene el contenido de un archivo .json

    Args:
        ruta (str): Ruta del archivo que desea leer.

    Returns:
        (Any | None): Los datos en el formato encontrado o None si no hay datos.
    """
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        crear_directorio(ruta)
        return None
    except json.decoder.JSONDecodeError:
        return None


def guardar_json(ruta: str, datos: Any):
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except Exception:
        pass


def crear_directorio(ruta: str) -> None:
    """Crea las carpetas de la ruta indicada."""
    path = Path(ruta).parent
    path.mkdir(parents=True, exist_ok=True)


def generar_archivo_json(ruta: str, encabezados: list[str], datos: list):
    "Crea o sobreescribe un archivo .json en la ruta indicada."
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()
            escritor.writerows(datos)
    except Exception as e:
        raise Exception from e
