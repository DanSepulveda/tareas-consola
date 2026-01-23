"""
Configuración de constantes globales del sistema.

Define rutas de archivos y enumeraciones estáticas utilizadas
para mantener la consistencia en toda la aplicación.
"""

from enum import StrEnum


class Rutas(StrEnum):
    """Rutas de los archivos (datos), y de las carpetas 'reportes' y 'logs'"""

    USUARIOS = "datos/usuarios.csv"
    TAREAS = "datos/tareas.json"
    REPORTES = "reportes/"
    LOGS = "logs/"
