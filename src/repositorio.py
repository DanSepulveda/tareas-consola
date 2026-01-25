import src.utilidades.archivos as gestor
import src.utilidades.helpers as utils
from src.constantes import Rutas
from src.schemas import Tarea, Usuario


def buscar_usuario(nombre_usuario: str) -> Usuario | None:
    """
    Busca un usuario registrado según su "nombre_usuario".

    Args:
        nombre_usuario (str): Nombre de usuario a buscar.

    Returns:
        (Usuario | None): Usuario buscado. None en caso de no existir.
    """
    usuarios: list[Usuario] = gestor.cargar_csv(Rutas.USUARIOS)
    return next(
        (u for u in usuarios if (u["nombre_usuario"] == nombre_usuario)), None
    )


def crear_usuario(nombre: str, nombre_usuario: str, clave: str) -> Usuario:
    """
    Crea un usuario en la Base de Datos.

    Args:
        usuario (Usuario): Diccionario con el usuario a crear.

    Returns:
        (Usuario | None): Usuario creado. None en caso de error.
    """
    usuarios: list[Usuario] = gestor.cargar_csv(Rutas.USUARIOS)
    nuevo_usuario: Usuario = {
        "id": utils.generar_id(),
        "nombre": nombre,
        "nombre_usuario": nombre_usuario,
        "hash": utils.generar_hash(clave),
    }
    usuarios.append(nuevo_usuario)
    encabezados = list(nuevo_usuario.keys())

    gestor.generar_archivo_json(Rutas.USUARIOS, encabezados, usuarios)
    return nuevo_usuario


def crear_tarea(tarea: Tarea) -> bool:
    """
    Agrega una tarea a la base de datos. Retorna una respuesta
    booleana dependiendo del éxito de la operación
    """
    try:
        tareas: list[Tarea] = gestor.cargar_json(Rutas.TAREAS) or []
        tareas.append(tarea)
        gestor.guardar_json(Rutas.TAREAS, tareas)
        return True
    except Exception:
        return False


def obtener_tareas_usuario(id_usuario: str) -> list[Tarea]:
    """
    Obtiene las tareas de un usuario mediante el id_usuario.

    Args:
        id_usuario (str): Id del usuario.

    Returns:
        list[Tarea]: Lista de tareas pertenecientes al usuario.
    """
    tareas: list[Tarea] = gestor.cargar_json(Rutas.TAREAS) or []
    tareas_usuario = [t for t in tareas if t["id_usuario"] == id_usuario]
    return tareas_usuario
