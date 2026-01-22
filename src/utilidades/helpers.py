import hashlib


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
