"""
Módulo de Persistencia de Datos.

Módulo que actúa como la Capa de Acceso a Datos (DAL), encargándose de la
comunicación con el sistema de almacenamiento. Centraliza las consultas,
el filtrado y el registro de la información de la aplicación.
"""

import src.utilidades.archivos as gestor
import src.utilidades.helpers as utils
from src.constantes import Rutas
from src.schemas import Tarea, Usuario


def buscar_usuario(nombre_usuario: str) -> Usuario | None:
    """Busca un usuario registrado (mediante nombre de usuario)."""
    usuarios: list[Usuario] = gestor.leer_csv(Rutas.USUARIOS)
    return next(
        (u for u in usuarios if (u["nombre_usuario"] == nombre_usuario)), None
    )


def crear_usuario(nombre: str, nombre_usuario: str, clave: str) -> Usuario:
    """Crea un usuario en el sistema de almacenamiento."""
    usuarios: list[Usuario] = gestor.leer_csv(Rutas.USUARIOS)
    nuevo_usuario: Usuario = {
        "id": utils.generar_id(),
        "nombre": nombre,
        "nombre_usuario": nombre_usuario,
        "hash": utils.generar_hash(clave),
    }
    usuarios.append(nuevo_usuario)
    encabezados = list(nuevo_usuario.keys())

    gestor.guardar_csv(Rutas.USUARIOS, encabezados, usuarios)
    return nuevo_usuario


def crear_tarea(tarea: Tarea) -> bool:
    """Crea una nueva tarea en el sistema de almacenamiento."""
    try:
        tareas: list[Tarea] = gestor.leer_json(Rutas.TAREAS) or []
        tareas.append(tarea)
        gestor.guardar_json(Rutas.TAREAS, tareas)
        return True
    except Exception:
        return False


def obtener_tareas_usuario(id_usuario: str) -> list[Tarea]:
    """Obtiene las tareas de un usuario mediante el id_usuario."""
    tareas: list[Tarea] = gestor.leer_json(Rutas.TAREAS) or []
    tareas_usuario = [t for t in tareas if t["id_usuario"] == id_usuario]
    return tareas_usuario
