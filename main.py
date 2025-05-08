import random
import flet as ft
import time
import math
import threading
import os

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

    # Imprimir información del entorno para depuración
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Contenido del directorio: {os.listdir('.')}")
    
    # Intentar encontrar las imágenes en diferentes ubicaciones
    posibles_rutas_ruleta = ["Rulete.png", "./Rulete.png", "/Rulete.png", "assets/Rulete.png"]
    posibles_rutas_flecha = ["flecha.png", "./flecha.png", "/flecha.png", "assets/flecha.png"]
    
    # Buscar la imagen de la ruleta
    ruleta_path = None
    for ruta in posibles_rutas_ruleta:
        if os.path.exists(ruta):
            ruleta_path = ruta
            print(f"Encontrada ruleta en: {ruta}")
            break
    
    if not ruleta_path:
        print("No se encontró la imagen de la ruleta. Usando respaldo.")
        ruleta_path = "Rulete.png"  # Usamos la ruta estándar como respaldo
    
    # Buscar la imagen de la flecha
    flecha_path = None
    for ruta in posibles_rutas_flecha:
        if os.path.exists(ruta):
            flecha_path = ruta
            print(f"Encontrada flecha en: {ruta}")
            break
    
    # Hacemos focus para que la página reciba los eventos de teclado
    page.focus = True

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

    # Contenedor para la cuenta regresiva grande
    cuenta_regresiva_grande = ft.Container(
        content=ft.Text(
            "4",
            size=300,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,  # Texto en blanco
            text_align=ft.TextAlign.CENTER
        ),
        alignment=ft.alignment.center,
        visible=False,
        bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),  # Fondo negro semi-transparente
        expand=True,  # Hacer que se expanda para llenar el espacio disponible
        animate_opacity=300,
    )

    # Contenedor overlay para la cuenta regresiva
    overlay_container = ft.Container(
        content=cuenta_regresiva_grande,
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.with_opacity(0.3, ft.colors.BLACK),  # Mucho más transparente (0.3 en lugar de 0.5)
        visible=False,  # Inicialmente oculto
        animate_opacity=300,
        margin=0,
        padding=0,
    )

    # Contenedor para la ruleta
    ruleta = ft.Container(
        content=ft.Image(src=ruleta_path, width=400, height=400),
        rotate=ft.Rotate(angle=0),
        width=400, 
        height=400,
        margin=0,
        padding=0,
    )

    # Crear una flecha como respaldo usando formas en lugar de imagen
    flecha_dibujada = ft.Stack(
        controls=[
            ft.Container(
                width=70,
                height=70,
                bgcolor="#FF5252",  # Fondo rojo
                border_radius=35,   # Círculo
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.Icon(
                    name=ft.icons.ARROW_DOWNWARD,
                    size=40,
                    color=ft.colors.WHITE
                ),
                alignment=ft.alignment.center,
                width=70,
                height=70,
            )
        ]
    )
    
    # Intentar cargar la imagen pero usar la flecha dibujada como respaldo
    if flecha_path:
        try:
            flecha_container = ft.Container(
                content=ft.Image(src=flecha_path, width=70, height=70, fit="contain"),
                width=70,
                height=70,
                alignment=ft.alignment.center,
            )
        except Exception as e:
            print(f"Error al cargar la imagen de flecha: {e}")
            flecha_container = flecha_dibujada
    else:
        print("No se encontró la imagen de flecha. Usando flecha dibujada.")
        flecha_container = flecha_dibujada
    
    colores_pastel = ["#FFB3BA", "#FFDFBA", "#D8BFD8", "#BAFFC9", "#BAE1FF"]
    colores = {letra: random.choice(colores_pastel) for letra in opciones}
    colores_originales = colores.copy()  # Guardar colores originales

    # Reorganizar letras en una cuadrícula rectangular
    filas = 4
    columnas = math.ceil(len(opciones) / filas)

    # Contenedores de letras para acceso fácil
    contenedores_letras = {}

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

    # Guardar referencia a cada contenedor por su letra
    for fila in letras_colores.controls:
        for contenedor in fila.controls:
            letra = contenedor.content.value
            if letra in opciones:
                contenedores_letras[letra] = contenedor

    puntaje_text = ft.Text(value="Puntaje: 0", color="black", font_family="Bold", size=17)
    tiempo_text = ft.Text(value="Tiempo: 40s", color="black", font_family="Bold", size=17)

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
    seleccion_en_curso = False
    letra_seleccionada = None
    timer_thread = None
    timer_activo = False  # Nueva variable para controlar si el timer está activo
    
    # Diálogo para tiempo agotado
    dialogo_tiempo_agotado = ft.AlertDialog(
        modal=True,
        title=ft.Text("¡Tiempo agotado!", size=20, weight=ft.FontWeight.BOLD),
        content=ft.Text("El tiempo se ha acabado para esta ronda.", size=16),
        actions=[
            ft.TextButton("Aceptar", on_click=lambda e: setattr(dialogo_tiempo_agotado, "open", False) or page.update())
        ],
        shape=ft.RoundedRectangleBorder(radius=15),
        content_padding=15
    )

    def mostrar_cuenta_regresiva():
        # Espera inicial de 2 segundos
        time.sleep(2)
        
        # Mostrar la letra seleccionada
        cuenta_regresiva_grande.content.value = f"La letra es: {letra_seleccionada}"
        cuenta_regresiva_grande.content.size = 100  # Tamaño más pequeño para el texto
        overlay_container.visible = True
        cuenta_regresiva_grande.visible = True
        overlay_container.opacity = 1
        cuenta_regresiva_grande.opacity = 1
        page.update()
        time.sleep(2)  # Mostrar por 2 segundos
        
        # Restaurar tamaño para números
        cuenta_regresiva_grande.content.size = 300
        
        # Cuenta regresiva
        for numero in range(4, 0, -1):
            cuenta_regresiva_grande.content.value = str(numero)
            overlay_container.visible = True
            cuenta_regresiva_grande.visible = True
            overlay_container.opacity = 1
            cuenta_regresiva_grande.opacity = 1
            page.update()
            time.sleep(0.7)
            overlay_container.opacity = 0
            cuenta_regresiva_grande.opacity = 0
            page.update()
            time.sleep(0.3)
        overlay_container.visible = False
        cuenta_regresiva_grande.visible = False
        page.update()

    def temporizador_regresivo():
        nonlocal timer_activo
        
        try:
            # Mostrar cuenta regresiva grande
            mostrar_cuenta_regresiva()
            
            # Cuenta regresiva desde 40 segundos
            for segundos_restantes in range(40, -1, -1):
                if not timer_activo:  # Si el timer fue cancelado, salir
                    return
                    
                tiempo_text.value = f"Tiempo: {segundos_restantes}s"
                page.update()
                
                # Si llegamos a cero, mostrar diálogo
                if segundos_restantes == 0:
                    page.dialog = dialogo_tiempo_agotado
                    dialogo_tiempo_agotado.open = True
                    page.update()
                    break
                    
                time.sleep(1)
        finally:
            timer_activo = False  # Asegurarse de que el timer se marque como inactivo al terminar

    def seleccionar_letra_aleatoria():
        nonlocal seleccion_en_curso, letra_seleccionada, timer_thread, timer_activo
        
        if seleccion_en_curso:
            return
            
        seleccion_en_curso = True
        letras_disponibles = [letra for letra in opciones if contenedores_letras[letra].content.value]
        
        if not letras_disponibles:
            seleccion_en_curso = False
            return
            
        # Duración del ciclo de selección
        duracion_total = random.uniform(2, 4)
        tiempo_inicial = time.time()
        tiempo_transcurrido = 0
        
        # Color de resaltado
        color_resaltado = "#FF6B6B"
        
        indice_actual = 0
        ultima_letra_resaltada = None
        
        # Tiempo entre cambios (empieza rápido y luego se ralentiza)
        tiempo_cambio_inicial = 0.05
        tiempo_cambio_final = 0.3
        
        try:
            while tiempo_transcurrido < duracion_total:
                # Restaurar color anterior si hay una letra resaltada
                if ultima_letra_resaltada and ultima_letra_resaltada in contenedores_letras:
                    contenedor = contenedores_letras[ultima_letra_resaltada]
                    if contenedor.content.value:  # Si la letra aún está visible
                        contenedor.bgcolor = colores[ultima_letra_resaltada]
                
                # Calcular el índice actual (circular)
                indice_actual = indice_actual % len(letras_disponibles)
                letra_actual = letras_disponibles[indice_actual]
                
                # Cambiar color de la letra actual
                contenedor = contenedores_letras[letra_actual]
                contenedor.bgcolor = color_resaltado
                ultima_letra_resaltada = letra_actual
                
                # Actualizar la página
                page.update()
                
                # Calcular tiempo de pausa para el próximo cambio
                progreso = tiempo_transcurrido / duracion_total
                factor = math.pow(progreso, 1.5)  # Desaceleración no lineal
                tiempo_pausa = tiempo_cambio_inicial + factor * (tiempo_cambio_final - tiempo_cambio_inicial)
                
                # Pausa
                time.sleep(tiempo_pausa)
                
                # Avanzar a la siguiente letra
                indice_actual += 1
                tiempo_transcurrido = time.time() - tiempo_inicial
            
            # Letra final seleccionada
            if ultima_letra_resaltada:
                letra_seleccionada = ultima_letra_resaltada
                notification_text.value = f"Letra seleccionada: {letra_seleccionada}"
                page.update()
                
                # Si hay un timer activo, cancelarlo
                if timer_activo:
                    timer_activo = False
                    time.sleep(0.1)  # Dar tiempo para que el timer anterior se detenga
                
                # Iniciar nuevo timer
                timer_activo = True
                timer_thread = threading.Thread(target=temporizador_regresivo, daemon=True)
                timer_thread.start()
        finally:
            seleccion_en_curso = False

    def actualizar_tiempo():
        segundos = 0
        while True:
            time.sleep(1)
            segundos += 1
            tiempo_text.value = f"Tiempo: {segundos}s"
            page.update()

    def girar_ruleta():
        duracion_total = random.uniform(4, 9)
        tiempo_inicial = time.time()
        tiempo_transcurrido = 0
        
        # Configuración para que gire muy rápido al principio y luego desacelere
        velocidad_inicial = 0.001  # Mucho más rápido al inicio
        velocidad_final = 0.2
        
        angulo_por_paso_inicial = math.radians(30)  # Mayor ángulo por paso
        angulo_por_paso_final = math.radians(5)

        while tiempo_transcurrido < duracion_total:
            progreso = tiempo_transcurrido / duracion_total
            # Curva de desaceleración no lineal para efecto más realista
            factor_desaceleracion = math.pow(progreso, 1.5)
            
            tiempo_pausa = velocidad_inicial + factor_desaceleracion * (velocidad_final - velocidad_inicial)
            angulo_por_paso = angulo_por_paso_inicial + factor_desaceleracion * (angulo_por_paso_final - angulo_por_paso_inicial)
            
            # Aplicar giro con varios pasos pequeños
            pasos = 5
            for _ in range(pasos):
                ruleta.rotate.angle += angulo_por_paso / pasos
                current_angle = math.degrees(ruleta.rotate.angle) % 360
                effective_angle = (current_angle + 90) % 360
                current_category = get_category(effective_angle)
                categoria_ganadora_text.value = f"{current_category}"
                page.update()
                time.sleep(tiempo_pausa / pasos)
                
            tiempo_transcurrido = time.time() - tiempo_inicial

    # Función para borrar la letra seleccionada
    def borrar_letra_seleccionada():
        nonlocal letra_seleccionada, timer_activo
        
        if letra_seleccionada and letra_seleccionada in contenedores_letras:
            contenedor = contenedores_letras[letra_seleccionada]
            contenedor.content.value = ""
            contenedor.bgcolor = "transparent"
            letra_seleccionada = None
            
            # Detener el temporizador si está activo
            if timer_activo:
                timer_activo = False
                tiempo_text.value = "Tiempo: 40s"  # Resetear el tiempo mostrado
                overlay_container.visible = False
                cuenta_regresiva_grande.visible = False
            
            page.update()

    # Función para manejar los eventos de teclado
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == " ":
            # Ejecutamos el giro en un hilo para evitar bloquear la interfaz
            threading.Thread(target=girar_ruleta, daemon=True).start()
        elif e.key == "Enter":
            # Inicia la selección de letra aleatoria
            threading.Thread(target=seleccionar_letra_aleatoria, daemon=True).start()
        elif e.key == "Backspace":
            # Borra la letra seleccionada
            borrar_letra_seleccionada()

    # Asignamos el callback de teclado a la página
    page.on_keyboard_event = on_keyboard

    ruleta_boton = ft.Column(
        controls=[flecha_container, ruleta],
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

    # Modificar el contenido principal para que sea responsive
    contenido_principal = ft.Stack(
        controls=[
            ft.Column(
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
            ),
            overlay_container
        ],
        expand=True,
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
    ft.app(target=main)
