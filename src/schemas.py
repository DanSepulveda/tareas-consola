"""
Definición de estructuras de datos y tipos (Schemas).

Este módulo define la forma de los objetos de datos para
asegurar la consistencia y facilitar el autocompletado.
"""

from typing import Literal, TypedDict


class Menu(TypedDict):
    """Type para los menús de navegación."""

    titulo: str
    opciones: list[str]


class Usuario(TypedDict):
    """Type para usuarios almacenados en usuarios.csv"""

    id: str
    nombre: str
    nombre_usuario: str
    clave: str


class Tarea(TypedDict):
    """Type para tareas registradas en tareas.json"""

    id: str
    id_usuario: str
    fecha_creacion: str
    fecha_vencimiento: str | None
    titulo: str
    categoria: str
    estado: Literal["Pendiente", "En proceso", "Finalizada"]


class Estado(TypedDict):
    """Type para el estado de la App (usuario logueado y sus tareas)"""

    usuario: Usuario
    tareas: list[Tarea]
