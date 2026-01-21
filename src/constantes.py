from enum import StrEnum


# Rutas de los distintos archivos (datos), y de las carpetas "reportes" y "logs"
class Rutas(StrEnum):
    USUARIOS = "datos/usuarios.json"
    TAREAS = "datos/tareas.xlsx"
    REPORTES = "reportes/"
    LOGS = "logs/"


# Mensajes de éxito/error para dar feedback a los usuarios dependiendo de las acciones
class Mensajes(StrEnum):
    INVALID_INT = "Opción inválida. Posibles valores:"
    NO_INT = "Debe ingresar un número entero."
