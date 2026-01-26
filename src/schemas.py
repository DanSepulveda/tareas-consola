"""
Definición de estructuras de datos y tipos (Schemas).

Este módulo define la forma de los objetos de datos para asegurar la
consistencia y facilitar el autocompletado.
"""

from collections.abc import Callable
from typing import Literal, NotRequired, TypedDict


class Menu(TypedDict):
    titulo: str
    opciones: list[str]


class Campo(TypedDict):
    label: str
    placeholder: str
    nombre: str
    valor: NotRequired[str]
    input: Callable


class Form(TypedDict):
    titulo: str
    campos: list[Campo]


class Usuario(TypedDict):
    id: str
    nombre: str
    nombre_usuario: str
    hash: str


EstadoTarea = Literal["Pendiente", "En proceso", "Finalizada"]


class Tarea(TypedDict):
    id: str
    id_usuario: str
    fecha_creacion: str
    fecha_vencimiento: str | None
    titulo: str
    categoria: str
    estado: EstadoTarea


class EstadoGlobal(TypedDict):
    usuario: Usuario
    tareas: list[Tarea]
