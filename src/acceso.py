import src.repositorio as repo
import src.utilidades.consola as cli
import src.utilidades.helpers as utils
from src.schemas import Usuario


def crear_usuario(nombre_usuario: str) -> Usuario:
    """Registra un nuevo usuario y lo retorna."""
    nombre = cli.input_texto("Ingrese su nombre", 3)
    clave = cli.input_texto("Ingrese su clave", 5)
    return repo.crear_usuario(nombre, nombre_usuario, clave)


def login():
    """Hace login de un usuario. Si no existe, deriva a su creación."""
    nombre_usuario = cli.input_texto("Nombre de usuario", 5, 20)
    usuario_buscado = repo.buscar_usuario(nombre_usuario)

    if usuario_buscado and es_clave_correcta(usuario_buscado["hash"]):
        return usuario_buscado

    if not usuario_buscado:
        cli.print_alerta("Usuario no registrado.")
        confirmacion = cli.input_confirmar("¿Desea crearlo?")

        if confirmacion:
            return crear_usuario(nombre_usuario)

    return None


def es_clave_correcta(hash: str) -> bool:
    """Solicta clave al usuario y la compara con el hash almacenado (3 intentos)"""
    intentos = 3
    while intentos > 0:
        clave_ingresada = cli.input_texto("Ingrese su clave", 1, 20)

        if utils.generar_hash(clave_ingresada) == hash:
            return True

        intentos -= 1
        cli.print_error(
            f"Clave incorrecta. Queda(n) {intentos} intento(s)."
            if intentos > 0
            else "Acceso denegado. No quedan intentos."
        )

    return False
