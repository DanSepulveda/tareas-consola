import json
from pathlib import Path
from typing import Any

import src.utilidades.helpers as utils
from src.constantes import Rutas
from src.schemas import Usuario


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
        path = Path(ruta).parent
        path.mkdir(parents=True, exist_ok=True)
        return None
    except json.decoder.JSONDecodeError:
        return None


def buscar_usuario(nombre_usuario: str) -> Usuario | None:
    """
    Busca un usuario registrado según su "nombre_usuario".

    Args:
        nombre_usuario (str): Nombre de usuario a buscar.

    Returns:
        (Usuario | None): Usuario buscado. None en caso de no existir.
    """
    usuarios: list[Usuario] = cargar_json(Rutas.USUARIOS) or []
    return next((u for u in usuarios if (u["nombre_usuario"] == nombre_usuario)), None)


def crear_usuario(usuario: Usuario) -> Usuario | None:
    """
    Crea un usuario en la Base de Datos.

    Args:
        usuario (Usuario): Diccionario con el usuario a crear.

    Returns:
        (Usuario | None): Usuario creado. None en caso de error.
    """
    usuarios: list[Usuario] = cargar_json(Rutas.USUARIOS) or []

    usuario.update(id=utils.generar_id(), clave=utils.hash_clave(usuario["clave"]))
    usuarios.append(usuario)

    try:
        with open(Rutas.USUARIOS, "w", encoding="utf-8") as archivo:
            json.dump(usuarios, archivo, indent=4, ensure_ascii=False)
        return usuario
    except Exception:
        return None
