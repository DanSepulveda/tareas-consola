import src.repositorio as repo
import src.utilidades.consola as cli
from src.acceso import login
from src.constantes import Config
from src.navegacion import menu_principal


def main():
    cli.print_panel(
        titulo=Config.NOMBRE_APP,
        contenido=f"Bienvenido a [green_yellow]{Config.NOMBRE_APP}[/], el programa N°1 para la Administración de Tareas.",
        subtitulo="Inicie sesión para continuar",
    )

    usuario_logueado = login()
    if not usuario_logueado:
        cli.print_alerta("No se ha iniciado sesión con ningún usuario.")
        return

    tareas = repo.obtener_tareas_usuario(usuario_logueado["id"])
    cli.input_continuar("¡Acceso concedido!")
    menu_principal({"usuario": usuario_logueado, "tareas": tareas})


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        cli.print_error(str(e))
    finally:
        cli.print_panel(
            titulo=Config.NOMBRE_APP,
            contenido="App finalizada. ¡Hasta pronto! 🤝",
            limpiar=False,
        )
