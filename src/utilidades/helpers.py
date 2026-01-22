import hashlib
import uuid


def hash_clave(clave: str) -> str:
    """
    Obtiene el hash para la clave del usuario.

    Args:
        clave (str): Clave del usuario.

    Returns:
        str: Hash de la clave.
    """
    hash_objeto = hashlib.sha256(clave.encode("utf-8"))
    return hash_objeto.hexdigest()


def generar_id() -> str:
    """
    Genera un identificador único.

    Returns:
        str: Identificador único (id).
    """
    return str(uuid.uuid4())


def contar_palabras(texto: str) -> int:
    """
    Cuenta la cantidad de palabras en un texto ignorando espacios extras.

    Args:
        texto (str): Texto a evaluar.

    Returns:
        int: Cantidad de palabras.
    """
    return len([p for p in texto.split(" ") if p != ""])
