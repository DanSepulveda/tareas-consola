import hashlib
import uuid


def hash_clave(clave: str):
    """
    Obtiene el hash para la clave del usuario.

    Args:
        clave (str): Clave del usuario.

    Returns:
        str: Hash de la clave.
    """
    hash_objeto = hashlib.sha256(clave.encode("utf-8"))
    return hash_objeto.hexdigest()


def generar_id():
    """
    Genera un identificador único.

    Returns:
        str: Identificador único (id).
    """
    return str(uuid.uuid4())
