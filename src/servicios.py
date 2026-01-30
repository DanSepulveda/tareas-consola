"""
Módulo de Servicios (Capa de Lógica de Negocio)

Este módulo contiene las funciones core de la aplicación, encargándose de
procesar la información y aplicar las reglas de negocio antes de la
persistencia de datos.
"""

import json
from datetime import date

import src.lib.archivos as gestor
import src.lib.consola as cli
import src.repositorio as repo
import src.utils as utils
from src.definiciones.constantes import Rutas
from src.definiciones.schemas import EstadoTarea, Extension, Tarea, Usuario


def es_clave_correcta(hash: str) -> bool:
    """Solicita clave al usuario y la compara con el hash almacenado (3 intentos)"""
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


def login():
    """Hace login de un usuario. Si no existe, deriva a su creación."""
    nombre_usuario = cli.input_texto("Nombre de usuario", 5, 20).lower()
    usuario_buscado = repo.buscar_usuario(nombre_usuario)

    if usuario_buscado and es_clave_correcta(usuario_buscado["hash"]):
        return usuario_buscado

    if not usuario_buscado:
        cli.print_alerta("Usuario no registrado.")
        confirmacion = cli.input_confirmar("¿Desea crearlo?")

        if confirmacion:
            return crear_usuario(nombre_usuario)

    return None


def crear_usuario(nombre_usuario: str):
    """Crea un nuevo usuario en el sistema."""
    nombre = cli.input_texto("Ingrese su nombre", 3)
    clave = cli.input_texto("Ingrese su clave", 5)

    nuevo_usuario: Usuario = {
        "id": utils.generar_id(),
        "nombre": nombre,
        "nombre_usuario": nombre_usuario.lower(),
        "hash": utils.generar_hash(clave),
    }
    repo.crear_usuario(nuevo_usuario)
    return nuevo_usuario


def crear_tarea(tareas: list[Tarea], form, usuario: Usuario):
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
    if not cantidad_tareas:
        return "No hay tareas con estado 'Finalizada'"

    repo.eliminar_tareas_finalizadas(usuario["id"])
    palabras = ("han", "tareas") if cantidad_tareas > 1 else ("ha", "tarea")
    for i in indices_finalizadas:
        tareas.pop(i)
    return f"Se {palabras[0]} eliminado {cantidad_tareas} {palabras[1]}"


def cambiar_estado_tarea(
    tareas: list[Tarea], tarea: Tarea, estado: int
) -> str:
    """Cambia el estado de una única tarea."""
    estados: list[EstadoTarea] = ["Pendiente", "En proceso", "Finalizada"]
    nuevo_estado = estados[estado - 1]

    if tarea["estado"] == nuevo_estado:
        return "Sin cambios. El estado no se ha modificado."

    repo.cambiar_estado_tarea(tarea["id"], nuevo_estado)
    for t in tareas:
        if t["id"] == tarea["id"]:
            t["estado"] = nuevo_estado
    return "Tarea modificada correctamente."


def exportar_tareas(
    tareas: list[Tarea],
    extensiones: tuple[Extension, ...],
    carpeta: str,
    abrir_web: bool,
) -> str:
    """Exporta los datos en los formatos especificados."""
    if not extensiones:
        return "No seleccionó ningún formato."

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

    return "Datos exportados correctamente"
