"""
Módulo de Servicios (Capa de Lógica de Negocio)

Este módulo contiene las funciones core de la aplicación, encargándose de
procesar la información y aplicar las reglas de negocio antes de la
persistencia de datos.
"""

import json
from datetime import date

import src.lib.archivos as gestor
import src.repositorio as repo
import src.utils as utils
from src.definiciones.constantes import Rutas
from src.definiciones.schemas import (
    EstadoGlobal,
    EstadoTarea,
    Extension,
    Tarea,
    Usuario,
)


def login(nombre_usuario: str, clave: str) -> str | EstadoGlobal:
    """Autentica a un usuario registrado."""
    usuario = repo.buscar_usuario(nombre_usuario)

    if not usuario:
        return "error:El usuario no se encuentra registrado."

    if utils.generar_hash(clave) != usuario["hash"]:
        return "error:Clave incorrecta."

    tareas = repo.obtener_tareas_usuario(usuario["id"])
    return {"usuario": usuario, "tareas": tareas}


def crear_usuario(
    nombre_usuario: str, nombre: str, clave: str
) -> str | EstadoGlobal:
    """Crea un nuevo usuario en el sistema."""
    existe_usuario = bool(repo.buscar_usuario(nombre_usuario))

    if existe_usuario:
        return "error:El usuario ya se encuentra registrado"

    nuevo_usuario: Usuario = {
        "id": utils.generar_id(),
        "nombre": nombre,
        "nombre_usuario": nombre_usuario.lower(),
        "hash": utils.generar_hash(clave),
    }
    repo.crear_usuario(nuevo_usuario)
    return {"usuario": nuevo_usuario, "tareas": []}


def crear_tarea(tareas: list[Tarea], form, usuario: Usuario) -> str:
    """Crea una tarea a partir de los datos ingresados por el usuario."""
    nueva_tarea: Tarea = {
        "id": utils.generar_id(),
        "id_usuario": usuario["id"],
        "fecha_creacion": date.today().strftime("%d-%m-%Y"),
        "fecha_vencimiento": None
        if form["fecha_vencimiento"] == "-"
        else form["fecha_vencimiento"],
        "titulo": form["titulo"],
        "categoria": form["categoria"],
        "estado": "Pendiente",
    }

    repo.crear_tarea(nueva_tarea)
    tareas.append(nueva_tarea)
    return "ok:Tarea agregada exitosamente."


def eliminar_finalizadas(tareas: list[Tarea], usuario: Usuario) -> str:
    """Elimina las tareas con estado 'Finalizada' asociadas a un id_usuario."""
    indices_finalizadas = sorted(
        [
            indice
            for indice, tarea in enumerate(tareas)
            if tarea["estado"] == "Finalizada"
        ],
        reverse=True,
    )
    cantidad_tareas = len(indices_finalizadas)

    repo.eliminar_tareas_finalizadas(usuario["id"])
    palabras = ("han", "tareas") if cantidad_tareas > 1 else ("ha", "tarea")
    for i in indices_finalizadas:
        tareas.pop(i)
    return f"ok:Se {palabras[0]} eliminado {cantidad_tareas} {palabras[1]}"


def cambiar_estado_tarea(
    tareas: list[Tarea], tarea: Tarea, estado: int
) -> str:
    """Cambia el estado de una única tarea."""
    estados: list[EstadoTarea] = ["Pendiente", "En proceso", "Finalizada"]
    nuevo_estado = estados[estado - 1]

    if tarea["estado"] == nuevo_estado:
        return "info:El estado no ha sido modificado."

    repo.cambiar_estado_tarea(tarea["id"], nuevo_estado)
    for t in tareas:
        if t["id"] == tarea["id"]:
            t["estado"] = nuevo_estado
    return "ok:Tarea modificada exitosamente."


def exportar_tareas(
    tareas: list[Tarea],
    extensiones: tuple[Extension, ...],
    carpeta: str,
    abrir_web: bool,
) -> str:
    """Exporta los datos en los formatos especificados."""
    if not extensiones:
        return "error:No seleccionó ningún formato."

    ruta_base = f"{Rutas.EXPORTACIONES}/{carpeta}"

    if ".csv" in extensiones:
        encabezados = list(tareas[0].keys())
        gestor.guardar_csv(f"{ruta_base}/tareas.csv", encabezados, tareas)

    if ".json" in extensiones:
        gestor.guardar_json(f"{ruta_base}/tareas.json", tareas)

    if ".html" in extensiones:
        a_exportar = [
            {
                **t,
                "vigencia": utils.estilar_vigencia_tarea(
                    t["fecha_vencimiento"], t["estado"]
                ),
            }
            for t in tareas
        ]
        tareas_json = json.dumps(a_exportar, indent=4, ensure_ascii=False)
        contenido = f"const tareas = {tareas_json};"
        gestor.guardar_texto_plano(f"{ruta_base}/web/main.js", contenido)
        gestor.copiar_archivo(Rutas.PLANTILLA, f"{ruta_base}/web")
        gestor.copiar_archivo(Rutas.FAVICON, f"{ruta_base}/web")
        if abrir_web:
            utils.abrir_navegador(f"{ruta_base}/web/index.html")

    return "ok:Datos exportados exitosamente."
