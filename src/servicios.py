from datetime import date

import src.repositorio as repo
import src.utilidades.helpers as utils
from src.schemas import Tarea, Usuario


def crear_tarea(tareas: list[Tarea], nueva_tarea, usuario: Usuario):
    nueva_tarea.update(
        {
            "id": utils.generar_id(),
            "id_usuario": usuario["id"],
            "fecha_creacion": date.today().strftime("%d-%m-%Y"),
            "estado": "Pendiente",
        }
    )
    exito = repo.crear_tarea(nueva_tarea)
    if exito:
        tareas.append(nueva_tarea)
    return exito
