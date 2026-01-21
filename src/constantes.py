from enum import StrEnum


# MENSAJES DE ÉXITO/ERROR PARA DAR FEEDBACK A LOS USUARIOS AL REALIZAR CIERTAS ACCIONES
class Mensajes(StrEnum):
    INVALID_INT = "Opción inválida. Posibles valores:"
    NO_INT = "Debe ingresar un número entero."
