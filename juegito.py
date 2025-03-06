import random
import flet as ft
import time
import math
import keyboard

def main(page: ft.Page):
    page.window_center()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Ruleta"
    
    opciones = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    colores = {letra: random.choice(["red", "black", "green"]) for letra in opciones}
    
    # Crear un contenedor para la ruleta
    ruleta = ft.Container(
        content=ft.Text("Ruleta", color="white"),
        bgcolor="blue",
        width=200,
        height=200,
        border_radius=100,
        alignment=ft.alignment.center,
        rotate=ft.Rotate(angle=0),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )
    
    # Crear contenedores de colores con letras a la derecha, dividiendo en 4 columnas
    columnas = 7
    colores_pastel = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
    colores_vivos = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
    colores = {letra: random.choice(colores_pastel + colores_vivos) for letra in opciones}
    
    letras_colores = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(letra, color="black", weight=ft.FontWeight.BOLD, size=18),
                        bgcolor=colores[letra],
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,
                        border_radius=15
                    ) for letra in opciones[i::columnas]
                ],
                alignment=ft.MainAxisAlignment.START
            ) for i in range(columnas)
        ],
        alignment=ft.MainAxisAlignment.START
    )

    def on_key_press(e):
        letra = e.name.upper()
        ascii_code = ord(letra)
        print(f"Tecla presionada: {letra}, Código ASCII: {ascii_code}")  # Imprimir la letra presionada y su código ASCII en la consola
        if letra in colores:
            for columna in letras_colores.controls:
                for contenedor in columna.controls:
                    if contenedor.content.value == letra:
                        contenedor.bgcolor = "gray"
                        contenedor.update()
            page.update()

    # Configurar el detector de teclas
    keyboard.on_press(on_key_press)
    
    def girar_ruleta(e):
        duracion_giro = random.uniform(5, 10)  # Duración aleatoria entre 5 y 10 segundos
        tiempo_inicial = time.time()
        tiempo_pausa = 0.01  # Velocidad inicial del giro
        
        while time.time() - tiempo_inicial < duracion_giro:
            ruleta.rotate.angle += math.radians(3.6)  # Ajusta el ángulo para un giro más suave
            page.update()
            time.sleep(tiempo_pausa)  # Pausa para simular el giro
            tiempo_pausa *= 0.91  # Incrementa el tiempo de pausa para disminuir la velocidad
        
        resultado = random.choice(opciones)
        resultado_text.value = f"La ruleta ha girado y ha salido: {resultado}"
        page.update()

    resultado_text = ft.Text(value="")
    girar_button = ft.ElevatedButton(text="Girar Ruleta", on_click=girar_ruleta)
    
    page.add(ft.Row([ruleta, letras_colores, ft.Column([girar_button, resultado_text], alignment=ft.MainAxisAlignment.CENTER)], alignment=ft.MainAxisAlignment.CENTER))

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)