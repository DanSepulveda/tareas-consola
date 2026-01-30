"""
Módulo de Navegación y Flujo de Usuario (Controlador)

Este módulo actúa como el orquestador principal de la aplicación.
Gestiona el ciclo de vida de la interacción con el usuario mediante la
presentación de menús, solicitud de datos, la lógica de navegación entre
pantallas y la invocación de servicios.
"""

import src.lib.consola as cli
import src.servicios as servicios
import src.utils as utils
from src.definiciones.constantes import Config
from src.definiciones.schemas import EstadoGlobal, Extension, Form, Menu


def menu_acceso():
    bienvenida = f"Bienvenido a [green_yellow]{Config.NOMBRE_APP}[/], el programa N°1 para la Administración de Tareas.\n\n"

    menu: Menu = {
        "titulo": Config.NOMBRE_APP,
        "opciones": [
            bienvenida + "🔸 1. Iniciar Sesión",
            "🔸 2. Crear Cuenta",
            "🔸 3. Salir del sistema",
        ],
    }
    opcion = utils.obtener_opcion_menu(menu)

    match opcion:
        case 1:
            iniciar_sesion()
        case 2:
            crear_cuenta()
        case 3:
            return

    menu_acceso()


def iniciar_sesion():
    usuario = cli.input_texto("Nombre de usuario", 4, 20).lower()
    clave = cli.input_texto("Ingrese su clave", 1, 20)

    respuesta = servicios.login(usuario, clave)

    if isinstance(respuesta, str):
        cli.print_panel("INFORMACIÓN", respuesta)
        return

    cli.print_exito("¡Acceso concedido!")
    cli.input_continuar("continuar")
    menu_principal(respuesta)


def crear_cuenta():
    usuario = cli.input_texto("Nombre de usuario", 5, 20).lower()
    nombre = cli.input_texto("Ingrese su nombre", 3)
    clave = cli.input_texto("Ingrese su clave", 5)

    respuesta = servicios.crear_usuario(usuario, nombre, clave)

    if isinstance(respuesta, str):
        cli.print_panel("INFORMACIÓN", respuesta)
        return

    cli.print_exito("Usuario creado exitosamente.")
    cli.input_continuar("continuar")
    menu_principal(respuesta)


def menu_principal(estado: EstadoGlobal):
    menu: Menu = {
        "titulo": "🔸 MENÚ PRINCIPAL 🔸",
        "opciones": [
            "📌 1. Agregar tarea",
            "📋 2. Listar tareas",
            "💾 3. Exportar datos",
            "🚪 4. Cerrar sesión",
        ],
    }
    opcion = utils.obtener_opcion_menu(menu)

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
                # "valor": "comienza nulo y se llena con lo ingresado en el input"
            },
            {
                "label": "Categoría(s)",
                "placeholder": "Ej. Desarrollo, Testing, etc.",
                "nombre": "categoria",
                "input": cli.input_texto,
                # "valor": "comienza nulo y se llena con lo ingresado en el input"
            },
            {
                "label": "Fecha límite",
                "placeholder": "Ej. 24-02-2026 o vacío",
                "nombre": "fecha_vencimiento",
                "input": cli.input_fecha,
                # "valor": "comienza nulo y se llena con lo ingresado en el input"
            },
        ],
    }

    # 1) Se muestra el "formulario" inicialmente mostrando los valores del placeholder
    titulo, campos = formulario["titulo"], formulario["campos"]
    cli.print_panel(titulo=titulo, contenido=utils.formatear_form(campos))

    # 2) A medida que se solicitan los datos, se agrega al formulario los valores
    # ingresados, y se muestran en reemplazo del placeholder
    for indice, campo in enumerate(campos):
        solicitar_dato, label = campo["input"], campo["label"]
        valor_ingresado = solicitar_dato(f"Ingrese {label}")
        campos[indice]["valor"] = valor_ingresado
        cli.print_panel(titulo=titulo, contenido=utils.formatear_form(campos))

    # 3) Se arma la tarea iterando cada campo y extrayendo su "nombre" y "valor"
    nueva_tarea = {c["nombre"]: c.get("valor") for c in campos}
    servicios.crear_tarea(tareas, nueva_tarea, usuario)

    cli.print_exito("Tarea agregada correctamente 🎉")
    cli.input_continuar("volver al menú principal")


def listar_tareas(estado: EstadoGlobal):
    tareas = estado["tareas"]

    # 1) SI NO HAY TAREAS -> se muestra mensaje y regresa al menú
    if not tareas:
        cli.print_panel("INFORMACIÓN", "No hay tareas registradas")
        cli.input_continuar("volver al menú principal")
        return

    # 2) SI HAY TAREAS -> se muestran en una tabla
    columnas, filas = utils.generar_datos_tabla(tareas)
    cli.print_tabla("LISTA DE TAREAS", columnas, filas)

    # 3) SI NO DESEA HACER MODIFICACIONES -> se vuelve al menú
    modificar = cli.input_confirmar("¿Desea realizar una modificación?")
    if not modificar:
        return

    # 4) SI DESEA HACER MODIFICACIONES -> se muestra el menú para modificar
    menu_modificar(estado)

    # 5) AL TERMINAR DE MODIFICAR -> se vuelve a mostrar el listado
    listar_tareas(estado)


def menu_modificar(estado: EstadoGlobal):
    menu: Menu = {
        "titulo": "📝 MODIFICAR TAREAS 📝",
        "opciones": [
            "🔸 1. Cambiar estado de tarea",
            "🔸 2. Eliminar tareas finalizadas",
            "🔸 3. Cancelar",
        ],
    }
    opcion = utils.obtener_opcion_menu(menu)

    match opcion:
        case 1:
            cambiar_estado(estado)
        case 2:
            eliminar_finalizadas(estado)
        case 3:
            return


def cambiar_estado(estado: EstadoGlobal):
    tareas = estado["tareas"]

    # 1) LISTAR TAREAS
    columnas, filas = utils.generar_datos_tabla(tareas)
    cli.print_tabla("LISTA DE TAREAS", columnas, filas)

    # 2) SE SOLICITA EL PSEUDO ID (ÍNDICE) DE LA TAREA Y EL NUEVO ESTADO
    texto_id = "ID de la tarea a modificar"
    texto_estado = "N° del nuevo estado 1=Pendiente 2=En proceso 3=Finalizada"
    indice_tarea = cli.input_entero(texto_id, min=1, max=len(tareas)) - 1
    nuevo_estado = cli.input_entero(texto_estado, min=1, max=3)

    # 3) MEDIANTE EL ÍNDICE SE OBTIENE LA TAREA (LA CUAL CONTIENE EL ID REAL)
    tarea = tareas[indice_tarea]

    # 4) SE EJECUTA EL SERVICIO Y SE MUESTRA EL RESULTADO
    respuesta = servicios.cambiar_estado_tarea(tareas, tarea, nuevo_estado)
    cli.print_panel("INFORMACIÓN", respuesta)
    cli.input_continuar("volver al listado")


def eliminar_finalizadas(estado: EstadoGlobal):
    tareas, usuario = estado["tareas"], estado["usuario"]

    # 1) SI NO HAY TAREAS FINALIZADAS -> se muetra mensaje y regresa al menú
    hay_finalizadas = any(t["estado"] == "Finalizada" for t in tareas)
    if not hay_finalizadas:
        cli.print_panel("INFORMACIÓN", "No hay tareas finalizadas")
        cli.input_continuar("volver al listado")
        return

    # 2) SI HAY TAREAS FINALIZADAS -> se listan, destacando las que serán eliminadas
    columnas, filas = utils.generar_datos_tabla(tareas, True)
    cli.print_tabla(
        titulo="LISTA DE TAREAS",
        columnas=columnas,
        filas=filas,
        caption="[black on red bold]Tareas a eliminar[/]",
    )

    # 3) SI NO CONFIRMA LA ELIMINACIÓN -> se cancela la operación
    confirmacion = cli.input_confirmar("¿Confirma eliminación?")
    if not confirmacion:
        cli.print_panel("INFORMACIÓN", "Operación cancelada")
        cli.input_continuar("volver al listado")
        return

    # 4) SI CONFIRMA LA ELIMINACIÓN -> se muestra el resultado
    respuesta = servicios.eliminar_finalizadas(tareas, usuario)
    cli.print_panel("INFORMACIÓN", respuesta)
    cli.input_continuar("volver al listado")


def exportar_datos(estado: EstadoGlobal):
    tareas = estado["tareas"]

    # 1) SI NO HAY TAREAS -> se muestra mensaje y regresa al menú
    if not tareas:
        cli.print_panel("INFORMACIÓN", "No hay datos para exportar")
        cli.input_continuar("volver al menú principal")
        return

    # 2) SI HAY TAREAS -> solicitar tipo de archivos a exportar
    cli.print_panel("EXPORTAR DATOS", "Indique los formatos que necesita.")

    extensiones: tuple[Extension, ...] = (".csv", ".json", ".html")
    extensiones_incluidas: tuple[Extension, ...] = tuple(
        opcion
        for indice, opcion in enumerate(extensiones, 1)
        if cli.input_confirmar(
            f"({indice}/{len(extensiones)}) ¿Desea incluir [green]{opcion}[/green]?"
        )
    )
    carpeta = cli.input_texto("Nombre de la carpeta de destino")

    abrir = False
    if ".html" in extensiones_incluidas:
        abrir = cli.input_confirmar("¿Desea ver la versión web al finalizar?")

    # 3) EJECUTAR EL SERVICIO Y MOSTRAR RESPUESTA
    respuesta = servicios.exportar_tareas(
        tareas, extensiones_incluidas, carpeta, abrir
    )
    cli.print_panel("INFORMACIÓN", respuesta)
    cli.input_continuar("volver al menú principal")
