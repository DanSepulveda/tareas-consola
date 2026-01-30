import src.lib.consola as cli
from src.definiciones.constantes import Config
from src.navegacion import menu_acceso


def main():
    try:
        menu_acceso()
    except Exception as e:
        cli.print_error(str(e))
    finally:
        cli.print_panel(
            titulo=Config.NOMBRE_APP,
            contenido="App finalizada. ¡Hasta pronto! 🤝",
            limpiar=False,
        )


if __name__ == "__main__":
    main()
