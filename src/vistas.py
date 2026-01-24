"""
Definición de Menús y Componentes Visuales.

Este módulo contiene los diccionarios de configuración para los menús de
la aplicación. Se utiliza en conjunto con el Módulo Consola para mostrar
las opciones de navegación, asegurando un formato visual consistente.
"""

from src.schemas import Menu


MENU_PRINCIPAL: Menu = {
    "titulo": "🔸 GESTIÓN DE TAREAS 🔸",
    "opciones": [
        "📌 1. Agregar tarea",
        "📋 2. Listar tareas",
        "📊 3. Generar reporte",
        "🚪 4. Cerrar sesión",
    ],
}

MENU_LISTADO: Menu = {
    "titulo": "📋 Listar Tareas 📋",
    "opciones": [
        "🟢 1. Ver en consola",
        "🟢 2. Ver en navegador",
        "🟠 3. Volver al menú principal",
    ],
}
