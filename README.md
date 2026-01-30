# tareApp (Gestor de tareas en consola)

Aplicación desarrollada en Python para la administración de tareas.

## Características

- **Gestión de Usuarios:** Registro y autenticación.
- **Control de Tareas:** Flujo completo de estados (_Pendiente, En proceso, Finalizada_).
- **Exportación Flexible:** Exporta tus datos a formatos `.csv`, `.json` o `.html`.
- **Interfaz Intuitiva:** Sistema de menús dinámicos por terminal.
- **Robustez:** Manejo de rutas inteligente mediante `pathlib`.

## Instalación

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/DanSepulveda/tareas-consola.git
    cd tareas-consola
    ```

2.  **Configura el entorno (opcional pero recomendado):**

    ```bash
    python -m venv .venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```

## Estructura del proyecto

```python
tareas-consola/
├── datos/                    # Almacena los datos que genera la APP (Base de datos)
│   ├── tareas.json                - almacena las tareas de todos los usuarios
│   └── usuarios.csv               - almacena los usuarios registrados
├── exportaciones/            # Carpeta donde se almacenan los datos exportados
├── src/                      # Código fuente de la aplicación
│   ├── definiciones/         # Definición de constantes (Rutas) y tipos de datos (Esquemas)
│   │   ├── constantes.py          - define las rutas de archivos y carpetas
│   │   └── schemas.py             - tipado de datos
│   ├── lib/                  # Conjunto de utilidades no ligadas a la lógica de la APP
│   │   ├── archivos.py            - leer/escribir archivos, crear directorios, etc
│   │   └── consola.py             - mostrar información en consola, o solicitar datos
│   ├── plantilla/            # Plantilla usada al exportar datos en formato web
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── navegacion.py         # Controla el flujo de la la app mediante las interacciones del usuario.
│   ├── repositorio.py        # Se encarga de obtener y almacenar información en "Base de datos"
│   ├── servicios.py          # Maneja la lógica de la app (login, creación tareas y usuarios, etc)
│   └── utils.py              # Conjunto de utilidades ligadas al proyecto (formato, filtros, etc)
└── main.py                   # Inicializa la aplicación
```
