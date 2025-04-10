import random
import flet as ft
import time
import math
import keyboard
import threading

def get_category(effective_angle):
    if 0 <= effective_angle < 36:
        return "Historia"
    elif 36 <= effective_angle < 72:
        return "Geografía"
    elif 72 <= effective_angle < 108:
        return "Ciencia y Tecnología"
    elif 108 <= effective_angle < 144:
        return "Arte y Literatura"
    elif 144 <= effective_angle < 180:
        return "Deportes"
    elif 180 <= effective_angle < 216:
        return "Entretenimiento y Cultura musical"
    elif 216 <= effective_angle < 252:
        return "Filosofía y Pensamiento"
    elif 252 <= effective_angle < 288:
        return "Cultura Popular y Curiosidades"
    elif 288 <= effective_angle < 324:
        return "Cálculo rápido y matemáticas mentales"
    elif 324 <= effective_angle < 360:
        return "Pensamiento lateral y creatividad"
    return ""

def main(page: ft.Page):
    page.title = "Ruleta"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FFF8E1"

    # Letras válidas (excluyendo Ñ, X, Y, Z, Q)
    opciones = [letra for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if letra not in "ÑXYZQ"]

    notification_text = ft.Text("Presiona espacio para girar la ruleta", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=22)
    notification_container = ft.Container(
        content=notification_text,
        bgcolor="#BDB2FF",
        width=630,
        height=50,
        alignment=ft.alignment.center,
        border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=20, bottom_right=20)
    )

    ruleta = ft.Container(
        content=ft.Image(src="Rulete.png", width=400, height=400),
        rotate=ft.Rotate(angle=0),
        width=400, height=400,
        margin=0,
        padding=0,
    )

    flecha_img = ft.Image(src="flecha.png", width=70, height=70, fit="contain")

    colores_pastel = ["#FFB3BA", "#FFDFBA", "#D8BFD8", "#BAFFC9", "#BAE1FF"]
    colores = {letra: random.choice(colores_pastel) for letra in opciones}

    # Reorganizar letras en una cuadrícula rectangular
    filas = 4
    columnas = math.ceil(len(opciones) / filas)

    letras_colores = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            opciones[i * columnas + j],
                            color="black",
                            weight=ft.FontWeight.BOLD,
                            size=30
                        ),
                        bgcolor=colores[opciones[i * columnas + j]],
                        width=80,
                        height=80,
                        alignment=ft.alignment.center,
                        border_radius=15
                    )
                    for j in range(columnas)
                    if i * columnas + j < len(opciones)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            for i in range(filas)
        ]
    )

    puntaje_text = ft.Text(value="Puntaje: 0", color="black", font_family="Bold", size=17)
    tiempo_text = ft.Text(value="Tiempo: 0s", color="black", font_family="Bold", size=17)

    categoria_ganadora_text = ft.Text(value="Ciencia y Tecnología", color="black", font_family="Bold", size=20)
    categoria_container = ft.Container(
        content=categoria_ganadora_text,
        bgcolor="#B5EAD7",
        width=630,
        height=50,
        alignment=ft.alignment.center,
        border_radius=20
    )

    timer_started = False

    def actualizar_tiempo():
        segundos = 0
        while True:
            time.sleep(1)
            segundos += 1
            tiempo_text.value = f"Tiempo: {segundos}s"
            page.update()

    def on_key_press(e):
        if e.name == "space":
            girar_ruleta()
            return
        letra = e.name.upper()
        if letra in colores:
            for fila in letras_colores.controls:
                for contenedor in fila.controls:
                    if contenedor.content.value == letra:
                        contenedor.content.value = ""  # ← Solo borramos el texto, no ocultamos el contenedor
                        contenedor.bgcolor = "transparent" 
                        contenedor.update()
            page.update()


    keyboard.on_press(on_key_press)

    def girar_ruleta():
        nonlocal timer_started
        duracion_total = random.uniform(4, 9)
        tiempo_inicial = time.time()
        tiempo_transcurrido = 0
        tiempo_inicio = 0.005
        tiempo_fin = random.uniform(0.05, 0.2)

        while tiempo_transcurrido < duracion_total:
            progreso = tiempo_transcurrido / duracion_total
            tiempo_pausa = tiempo_inicio + progreso * (tiempo_fin - tiempo_inicio)

            incremento_total = math.radians(10)
            pasos = 10
            for _ in range(pasos):
                ruleta.rotate.angle += incremento_total / pasos
                current_angle = math.degrees(ruleta.rotate.angle) % 360
                effective_angle = (current_angle + 90) % 360
                current_category = get_category(effective_angle)
                categoria_ganadora_text.value = f"{current_category}"
                page.update()
                time.sleep(tiempo_pausa / pasos)
            tiempo_transcurrido = time.time() - tiempo_inicial

        if not timer_started:
            timer_started = True
            threading.Thread(target=actualizar_tiempo, daemon=True).start()

    ruleta_boton = ft.Column(
        controls=[flecha_img, ruleta],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0
    )

    Parte1 = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text("Categorías", color="black", font_family="Bold", size=20),
                bgcolor="#A0C4FF",
                width=270,
                height=40,
                border_radius=20,
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(content=puntaje_text, width=130, height=40, alignment=ft.alignment.center, bgcolor="#A0C4FF", border_radius=20),
                        ft.Container(content=tiempo_text, width=130, height=40, alignment=ft.alignment.center, bgcolor="#A0C4FF", border_radius=20)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                ),
                width=630,
                height=50,
                alignment=ft.alignment.center
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    Parte2 = ft.Row(
        controls=[ruleta_boton, letras_colores],
        alignment=ft.MainAxisAlignment.CENTER
    )

    Parte3 = ft.Row(
        controls=[categoria_container],
        alignment=ft.MainAxisAlignment.CENTER
    )

    contenido_principal = ft.Column(
        controls=[
            notification_container,
            ft.Column(
                controls=[Parte1, Parte2, Parte3],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Seleccione el modo de juego", size=20, weight=ft.FontWeight.BOLD),
        content=ft.Row(
            controls=[
                ft.ElevatedButton("Online", on_click=lambda _: setattr(dialog, "open", False) or page.update()),
                ft.ElevatedButton("Local", on_click=lambda _: setattr(dialog, "open", False) or page.update())
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        shape=ft.RoundedRectangleBorder(radius=15),
        content_padding=15
    )

    page.dialog = dialog
    dialog.open = True
    page.add(contenido_principal)
    page.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER) 
