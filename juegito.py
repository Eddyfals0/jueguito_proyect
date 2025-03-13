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
    page.theme_mode = ft.ThemeMode.DARK

    opciones = list("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")

    notification_text = ft.Text("Presiona espacio para girar la ruleta", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD, size=22)
    notification_container = ft.Container(
        content=notification_text,
        bgcolor="orange",
        width=630,
        height=50,
        alignment=ft.alignment.center,
        border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=20, bottom_right=20)
    )

    # Ruleta inicial sin rotación
    ruleta = ft.Container(
        content=ft.Image(src="Rulete.png", width=400, height=400),
        rotate=ft.Rotate(angle=0),
        width=400, height=400,
        margin=0,
        padding=0,
    )

    # Imagen pequeña que se mostrará arriba de la ruleta
    flecha_img = ft.Image(src="flecha.png", width=70, height=70, fit="contain")

    columnas = 7
    colores_pastel = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
    colores_vivos = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
    colores = {letra: random.choice(colores_pastel + colores_vivos) for letra in opciones}

    letras_colores = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(letra, color="black", weight=ft.FontWeight.BOLD, size=30),
                        bgcolor=colores[letra],
                        width=80,
                        height=80,
                        alignment=ft.alignment.center,
                        border_radius=15
                    ) for letra in opciones[i::columnas]
                ],
                alignment=ft.MainAxisAlignment.START
            ) for i in range(columnas)
        ],
        alignment=ft.MainAxisAlignment.START
    )

    puntaje_text = ft.Text(value="Puntaje: 0", color="white", font_family="Bold", size=17)
    tiempo_text = ft.Text(value="Tiempo: 0s", color="white", font_family="Bold", size=17)
    
    categoria_ganadora_text = ft.Text(value="Ciencia y Tecnología", color="white", font_family="Bold", size=20)
    categoria_container = ft.Container(
        content=categoria_ganadora_text,
        bgcolor="#393c40",
        width=630,
        height=50,
        alignment=ft.alignment.center,
        border_radius=20
    )

    def actualizar_tiempo():
        segundos = 0
        while True:
            time.sleep(1)
            segundos += 1
            tiempo_text.value = f"Tiempo: {segundos}s"
            page.update()

    threading.Thread(target=actualizar_tiempo, daemon=True).start()

    def on_key_press(e):
        if e.name == "space":
            girar_ruleta(None)
            return
        letra = e.name.upper()
        if letra in colores:
            for columna in letras_colores.controls:
                for contenedor in columna.controls:
                    if contenedor.content.value == letra:
                        contenedor.content.color = "white"
                        contenedor.bgcolor = "transparent"
                        contenedor.update()
            page.update()

    keyboard.on_press(on_key_press)

    def girar_ruleta(e):
        duracion_total = random.uniform(4, 9)
        tiempo_inicial = time.time()
        tiempo_transcurrido = 0
        velocidad_maxima = 0.009
        velocidad_minima = 0.2   

        while tiempo_transcurrido < duracion_total:
            progreso = tiempo_transcurrido / duracion_total  
            if progreso < 0.2:
                factor = (progreso / 0.2) ** 2
                tiempo_pausa = velocidad_minima - factor * (velocidad_minima - velocidad_maxima)
            elif progreso < 0.7:
                tiempo_pausa = velocidad_maxima
            else:
                factor = (progreso - 0.7) / 0.3
                tiempo_pausa = velocidad_maxima + factor * (velocidad_minima - velocidad_maxima)

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

    # Se utiliza solo la barra espaciadora para activar el giro.
    # La imagen se coloca encima de la ruleta con espacio mínimo entre ellas.
    ruleta_boton = ft.Column(
        controls=[
            flecha_img,
            ruleta
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0  # Espaciado mínimo entre la imagen y la ruleta
    )

    Parte1 = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text("Categorías", color="white", font_family="Bold", size=20),
                bgcolor="#393c40",
                width=270,
                height=40,
                border_radius=20,
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(content=puntaje_text, width=130, height=40, alignment=ft.alignment.center, bgcolor="#393c40", border_radius=20),
                        ft.Container(content=tiempo_text, width=130, height=40, alignment=ft.alignment.center, bgcolor="#393c40", border_radius=20)
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
        controls=[
            ruleta_boton,
            letras_colores,
        ],
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

    page.add(contenido_principal)

if __name__ == "__main__":
    ft.app(target=main)
