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
    
    # Crear un contenedor para la ruleta
    ruleta = ft.Container(
        content=ft.Text("Ruleta", color="white"),
        bgcolor="blue",
        width=270,
        height=270,
        border_radius=150,
        alignment=ft.alignment.center,
        rotate=ft.Rotate(angle=0),
    )
    
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
        duracion_total = random.uniform(4, 9)
        tiempo_inicial = time.time()
        tiempo_transcurrido = 0
        tiempo_maximo = duracion_total

        velocidad_maxima = 0.009
        velocidad_minima = 0.2   

        while tiempo_transcurrido < tiempo_maximo:
            progreso = tiempo_transcurrido / tiempo_maximo  

           
            if progreso < 0.2:
                factor = (progreso / 0.2) ** 2
                tiempo_pausa = velocidad_minima - factor * (velocidad_minima - velocidad_maxima)
            
            elif progreso < 0.7:
                tiempo_pausa = velocidad_maxima
            
            else:
                factor = (progreso - 0.7) / 0.3
                tiempo_pausa = velocidad_maxima + factor * (velocidad_minima - velocidad_maxima)

            # Mis ajustes para la velocidad del giro  ------------------------------------------------------------------------------
            incremento_total = math.radians(10)
            pasos = 10 
            for _ in range(pasos):
                ruleta.rotate.angle += incremento_total / pasos
                page.update()
                time.sleep(tiempo_pausa / pasos)
            tiempo_transcurrido = time.time() - tiempo_inicial

        resultado = random.choice(opciones)
        resultado_text.value = f"La ruleta ha girado y ha salido: {resultado}"
        page.update()

    resultado_text = ft.Text(value="")
    girar_button = ft.ElevatedButton(text="Girar Ruleta", on_click=girar_ruleta)
    
    
    ruleta_boton = ft.Column(
        [
            ruleta,
            ft.Container(height=10),
            girar_button
        ], 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    Parte2 = ft.Row(
        [
            ruleta_boton,
            letras_colores, 
            ft.Column(
                [resultado_text],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ], 
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(Parte2)

if __name__ == "__main__":
    ft.app(target=main)
