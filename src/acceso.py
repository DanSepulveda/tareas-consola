import src.repositorio as repo
import src.utilidades.consola as cli
import src.utilidades.helpers as utils
from src.schemas import Usuario


def crear_usuario(nombre_usuario: str) -> Usuario | None:
    """
    Registrar nuevo usuario en el sistema.

    Args:
        nombre_usuario (str): Nombre del usuario a crear.

    Returns:
        (Usuario | None): El usuario creado o None si hubo algún problema.
    """
    nombre = cli.input_texto("Ingrese su nombre", 3)
    clave = cli.input_texto("Ingrese su clave", 5)
    usuario = repo.crear_usuario(
        {"id": "", "nombre": nombre, "nombre_usuario": nombre_usuario, "clave": clave}
    )

    if usuario:
        return usuario

    cli.print_error("Ha ocurrido un error")
    return None


def login():
    """
    Autentica a un usuario mediante nombre de usuario y contraseña.
    En caso de no existir, deriva al proceso de registro.

    Returns:
        (Usuario | None): Usuario, si el login es correcto. None, en caso contrario.
    """
    nombre_usuario = cli.input_texto("Nombre de usuario", 5, 20)
    usuario_buscado = repo.buscar_usuario(nombre_usuario)

    if usuario_buscado and match_clave(usuario_buscado["clave"]):
        return usuario_buscado

    if not usuario_buscado:
        confirmacion = cli.input_confirmar("¿Desea crear el usuario?")
        if not confirmacion:
            return None
        usuario = crear_usuario(nombre_usuario)
        return usuario

    return None


def match_clave(hash: str, intentos: int = 3) -> bool:
    intentos_restantes = intentos

    while intentos_restantes > 0:
        clave_ingresada = cli.input_texto("Ingrese su clave", 5)

        if utils.hash_clave(clave_ingresada) == hash:
            cli.print_exito("¡Acceso concedido!")
            return True

        intentos_restantes -= 1

        if intentos_restantes > 0:
            cli.print_error(
                f"Clave incorrecta. Le queda(n) {intentos_restantes} intento(s)."
            )
        else:
            cli.print_error("Acceso denegado. Ha agotado todos los intentos.")

    return False
