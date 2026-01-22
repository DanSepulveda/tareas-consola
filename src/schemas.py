from typing import TypedDict


# Type para menús que despliegan opciones
class Menu(TypedDict):
    titulo: str
    opciones: list[str]


# Type para usuarios almacenados en usuarios.json
class Usuario(TypedDict):
    id: str
    nombre: str
    nombre_usuario: str
    clave: str
