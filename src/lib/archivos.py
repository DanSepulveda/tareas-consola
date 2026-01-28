"""
Módulo para la Administración de Archivos.

Centraliza todas las operaciones de manejo de archivos y directorios,
tales como lectura y escritura de CSV y JSON, creación de directorios, y
la copia de archivos de un directorio a otro.
"""

import csv
import json
import shutil
from pathlib import Path
from typing import Any


def crear_directorio(ruta: str) -> None:
    """Crea las carpetas (en caso de no existir) de la ruta indicada."""
    path = Path(ruta)
    path = path.parent if path.suffix else path
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def copiar_archivo(ruta_archivo: str, ruta_destino: str):
    """Copia un archivo a la ruta de destino indicada."""
    try:
        path_archivo = Path(ruta_archivo)
        path_destino = Path(ruta_destino)
        crear_directorio(ruta_destino)
        shutil.copy(path_archivo, path_destino)
    except Exception as e:
        raise Exception("Error al copiar archivo.") from e


def leer_csv(ruta: str) -> list:
    """Lee y retorna el contenido de un archivo .csv"""
    try:
        with open(ruta, encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            return list(lector)
    except FileNotFoundError:
        return []


def guardar_csv(ruta: str, encabezados: list[str], datos: list):
    """Crea o sobrescribe un archivo .csv en la ruta indicada."""
    try:
        crear_directorio(ruta)
        with open(ruta, "w", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()
            escritor.writerows(datos)
    except Exception as e:
        raise Exception("Error al guardar CSV.") from e


def leer_json(ruta: str) -> Any | None:
    """Lee y retorna el contenido de un archivo .json"""
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def guardar_json(ruta: str, datos: Any):
    """Crea o sobrescribe un archivo .json en la ruta indicada."""
    try:
        crear_directorio(ruta)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        raise Exception("Error al guardar JSON.") from e


def guardar_texto_plano(ruta: str, contenido: str):
    """Crea o sobrescribe un archivo de texto (.txt, .js) en la ruta indicada."""
    try:
        crear_directorio(ruta)
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
    except Exception as e:
        raise Exception("Error al guardar archivo.") from e
