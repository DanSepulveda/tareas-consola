import src.lib.consola as cli
import src.servicios as servicios
import src.utils as utils
from src.schemas import EstadoGlobal, Form, Menu


def menu_principal(estado: EstadoGlobal):
    menu: Menu = {
        "titulo": "🔸 GESTIÓN DE TAREAS 🔸",
        "opciones": [
            "📌 1. Agregar tarea",
            "📋 2. Listar tareas",
            "💾 3. Exportar datos",
            "🚪 4. Cerrar sesión",
        ],
    }
    opcion = utils.opcion_desde_menu(menu)

    match opcion:
        case 1:
            formulario_agregar(estado)
        case 2:
            listar_tareas(estado)
        case 3:
            exportar_datos(estado)
        case 4:
            cli.print_alerta("Ha cerrado la sesión.")
            return

    menu_principal(estado)


# TODO: agregar regex para validar fecha y otros inputs
# TODO: revisar color de placeholder o label, para que no se confundan
def formulario_agregar(estado: EstadoGlobal):
    tareas, usuario = estado["tareas"], estado["usuario"]
    formulario: Form = {
        "titulo": "📌 AGREGAR TAREA 📌",
        "campos": [
            {
                "label": "Título",
                "placeholder": "Ej. Terminar proyecto 1",
                "nombre": "titulo",
                "input": cli.input_texto,
            },
            {
                "label": "Categoría(s)",
                "placeholder": "Ej. Urgente, Desarrollo, Proyecto.",
                "nombre": "categoria",
                "input": cli.input_texto,
            },
            {
                "label": "Fecha límite",
                "placeholder": "Ej. 24-02-2026 o vacío",
                "nombre": "fecha_vencimiento",
                "input": cli.input_texto,
            },
        ],
    }

    titulo, campos = formulario["titulo"], formulario["campos"]
    cli.print_panel(titulo=titulo, contenido=utils.formatear_form(campos))

    for indice, campo in enumerate(campos):
        valor = campo["input"](f"Ingrese {campo['label']}")
        campos[indice]["valor"] = valor
        cli.print_panel(titulo=titulo, contenido=utils.formatear_form(campos))

    nueva_tarea = {c["nombre"]: c.get("valor") for c in campos}
    servicios.crear_tarea(tareas, nueva_tarea, usuario)

    cli.print_exito("Tarea agregada correctamente 🎉")
    cli.input_continuar("volver al menú principal")


def listar_tareas(estado: EstadoGlobal):
    tareas = estado["tareas"]

    # 1) Si no hay tareas, se muestra un mensaje
    if not tareas:
        cli.print_panel(
            titulo="MIS TAREAS",
            contenido="👻 No hay tareas registradas 👻".center(48),
        )
        cli.input_continuar("volver al menú principal")
        return

    # 2) Si hay tareas, se muestran las tareas en formato tabla
    columnas, filas = utils.generar_tabla_tareas(tareas)
    cli.print_table(f"Lista de tareas ({len(tareas)})", columnas, filas)

    # 3) Si el usuario no desea hacer modificaciones, se vuelve al menú
    modificar = cli.input_confirmar("¿Desea realizar una modificación?")
    if not modificar:
        return

    # 4) Si desea modificar, se muestra el menú para modificar
    menu_modificar(estado)

    # 5) Al terminar la modificación se vuelve a mostrar el listado
    listar_tareas(estado)


def menu_modificar(estado: EstadoGlobal):
    tareas, usuario = estado["tareas"], estado["usuario"]

    menu: Menu = {
        "titulo": "📝 MODIFICAR TAREAS 📝",
        "opciones": [
            "🟢 1. Cambiar estado de tarea",
            "🟢 2. Eliminar tareas finalizadas",
            "🟠 3. Cancelar",
        ],
    }
    opcion = utils.opcion_desde_menu(menu)

    # 5) Finalmente se ejecuta la opción elegida
    match opcion:
        case 1:
            pass
        case 2:
            respuesta = servicios.eliminar_finalizadas(tareas, usuario)
            cli.print_panel("Resultado", respuesta)
            cli.input_continuar("continuar")
        case 3:
            return


def exportar_datos(estado: EstadoGlobal):
    pass
