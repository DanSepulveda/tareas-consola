"""
Configuración de constantes globales del sistema.

Define enumeraciones estáticas utilizadas para mantener la consistencia
en toda la aplicación (rutas, configuraciones, etc).
"""

from enum import StrEnum


class Rutas(StrEnum):
    USUARIOS = "datos/usuarios.csv"
    TAREAS = "datos/tareas.json"
    EXPORTACIONES = "exportaciones/"


class Config(StrEnum):
    NOMBRE_APP = "tareApp"
