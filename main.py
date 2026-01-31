import src.lib.consola as cli
from src.controlador import menu_acceso
from src.definiciones.constantes import Config


def main():
    try:
        menu_acceso()
    except KeyboardInterrupt:
        pass
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
