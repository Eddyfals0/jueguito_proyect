import flet as ft

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Mi Primera App con Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Crear un botón
    def button_clicked(e):
        text.value = "¡Hola desde Flet!"
        page.update()

    text = ft.Text()
    button = ft.ElevatedButton("¡Haz clic aquí!", on_click=button_clicked)

    # Agregar elementos a la página
    page.add(
        ft.Text("Bienvenido a mi aplicación web", size=30, weight=ft.FontWeight.BOLD),
        ft.Text("Esta es una aplicación creada con Flet", size=16),
        button,
        text
    )

ft.app(target=main, view=ft.WEB_BROWSER)
