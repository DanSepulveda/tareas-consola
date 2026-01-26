"""
Módulo de Persistencia de Datos.

Módulo que actúa como la Capa de Acceso a Datos (DAL), encargándose de la
comunicación con el sistema de almacenamiento. Centraliza las consultas,
el filtrado y el registro de la información de la aplicación.
"""

import src.lib.archivos as gestor
from src.constantes import Rutas
from src.schemas import EstadoTarea, Tarea, Usuario


def buscar_usuario(nombre_usuario: str) -> Usuario | None:
    """Busca un usuario registrado (mediante nombre de usuario)."""
    usuarios: list[Usuario] = gestor.leer_csv(Rutas.USUARIOS)
    return next(
        (u for u in usuarios if (u["nombre_usuario"] == nombre_usuario)), None
    )


def crear_usuario(usuario: Usuario):
    """
    Crea un usuario en el sistema de almacenamiento. Nota: *Esta función
    se ejecuta después de haber intentado iniciar sesión, por lo tanto
    ya se ha validado que el usuario no existe (evitar duplicados)*.
    """
    usuarios: list[Usuario] = gestor.leer_csv(Rutas.USUARIOS)
    usuarios.append(usuario)
    encabezados = list(usuario.keys())
    gestor.guardar_csv(Rutas.USUARIOS, encabezados, usuarios)


def crear_tarea(tarea: Tarea):
    """Crea una tarea en el sistema de almacenamiento."""
    tareas: list[Tarea] = gestor.leer_json(Rutas.TAREAS) or []
    tareas.append(tarea)
    gestor.guardar_json(Rutas.TAREAS, tareas)


def obtener_tareas_usuario(id_usuario: str) -> list[Tarea]:
    """Obtiene las tareas de un usuario mediante el id_usuario."""
    tareas: list[Tarea] = gestor.leer_json(Rutas.TAREAS) or []
    tareas_usuario = [t for t in tareas if t["id_usuario"] == id_usuario]
    return tareas_usuario


def eliminar_tareas_finalizadas(id_usuario: str):
    """Elimina las tareas finalizadas de un usuario."""
    tareas: list[Tarea] = gestor.leer_json(Rutas.TAREAS) or []
    filtradas = [
        t
        for t in tareas
        if not (t["id_usuario"] == id_usuario and t["estado"] == "Finalizada")
    ]
    gestor.guardar_json(Rutas.TAREAS, filtradas)


def cambiar_estado_tarea(id_tarea: str, nuevo_estado: EstadoTarea):
    """Cambia el estado de una tarea."""
    tareas: list[Tarea] = gestor.leer_json(Rutas.TAREAS) or []
    actualizadas = [
        {**tarea, "estado": nuevo_estado} if tarea["id"] == id_tarea else tarea
        for tarea in tareas
    ]
    gestor.guardar_json(Rutas.TAREAS, actualizadas)
