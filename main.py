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

# Diccionario de subcategorías
subcategorias = {
    "Historia": [
        "Fechas y eventos importantes (independencias, guerras, tratados)",
        "Personajes históricos influyentes",
        "Civilizaciones antiguas (Egipto, Roma, Maya, etc.)"
    ],
    "Geografía": [
        "Países y capitales",
        "Ríos, montañas y océanos",
        "Banderas y mapas"
    ],
    "Ciencia y Tecnología": [
        "Descubrimientos científicos importantes",
        "Inventores y sus creaciones",
        "Principios físicos y químicos básicos"
    ],
    "Arte y Literatura": [
        "Autores y sus obras más famosas",
        "Movimientos artísticos y culturales",
        "Premios Nobel de literatura y cine"
    ],
    "Deportes": [
        "Reglas y datos de deportes populares",
        "Juegos Olímpicos y récords mundiales",
        "Equipos y jugadores legendarios"
    ],
    "Entretenimiento y Cultura musical": [
        "Películas, series y personajes icónicos",
        "Música y cantantes famosos",
        "Videojuegos y cómics"
    ],
    "Filosofía y Pensamiento": [
        "Principales filósofos y sus ideas",
        "Conceptos básicos de ética y lógica",
        "Religiones y sistemas de creencias"
    ],
    "Cultura Popular y Curiosidades": [
        "Tradiciones y costumbres de distintos países",
        "Récords Guinness sorprendentes",
        "Datos curiosos sobre la vida cotidiana"
    ],
    "Cálculo rápido y matemáticas mentales": [
        "Operaciones básicas"
    ],
    "Pensamiento lateral y creatividad": [
        "Inventa un objeto o personaje",
        "Desafío: Inventa un objeto útil que empiece con la letra que te tocó",
        "¿Cómo cruzarías un río sin puente con algo que empiece con la letra que te tocó?"
    ]
}

def get_random_subcategory(category):
    if category in subcategorias:
        return random.choice(subcategorias[category])
    return ""

# Función para crear la ruleta visual como respaldo
def crear_ruleta_visual():
    categorias = [
        ("Historia", "#FF9AA2"),
        ("Geografía", "#FFB347"),
        ("Ciencia y Tecnología", "#FDFD96"),
        ("Arte y Literatura", "#CFCFC4"),
        ("Deportes", "#B5EAD7"),
        ("Entretenimiento", "#C7CEEA"),
        ("Filosofía", "#FFDAC1"),
        ("Cultura Popular", "#E2F0CB"),
        ("Matemáticas", "#B5D8EB"),
        ("Creatividad", "#FCD1D1")
    ]
    
    segmentos = []
    angulo_inicial = 0
    angulo_segmento = 36  # 360 / 10 categorías
    
    for i, (categoria, color) in enumerate(categorias):
        segmento = ft.Container(
            width=400,
            height=400,
            bgcolor=color,
            border_radius=0,
            rotate=ft.Rotate(angle=math.radians(angulo_inicial), alignment=ft.alignment.center),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            padding=10,
        )
        segmentos.append(segmento)
        angulo_inicial += angulo_segmento
    
    return ft.Stack(
        width=400,
        height=400,
        controls=segmentos
    )

# Diálogo de bienvenida
dialogo_bienvenida = ft.AlertDialog(
    modal=True,
    title=ft.Container(
        content=ft.Text("¡Bienvenido al Juego!", size=32, weight=ft.FontWeight.BOLD),
        alignment=ft.alignment.center,
        width=400
    ),
    content=ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Instrucciones:", size=24, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center,
                    width=400
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("1. Gira la ruleta para obtener una categoría y subcategoría", size=18),
                            ft.Text("2. Selecciona una letra aleatoria", size=18),
                            ft.Text("3. Di una palabra que:", size=18),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("• Empiece con la letra seleccionada", size=16),
                                        ft.Text("• Corresponda a la categoría y subcategoría", size=16)
                                    ],
                                    spacing=5
                                ),
                                padding=ft.padding.only(left=20)
                            ),
                            ft.Text("4. Si aciertas, presiona el botón 'Correcto'", size=18),
                            ft.Text("5. Si no aciertas, presiona 'Enter' para nueva letra", size=18),
                            ft.Text("6. Tienes 40 segundos para jugar", size=18)
                        ],
                        spacing=10
                    ),
                    width=400,
                    padding=10
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("¡Que te diviertas!", size=24, weight=ft.FontWeight.BOLD, color="#FF6B6B"),
                            ft.Text("Presiona cualquier botón para comenzar", size=18, italic=True, color="#666666")
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    width=400,
                    padding=ft.padding.only(top=10)
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            scroll=ft.ScrollMode.AUTO
        ),
        width=400,
        height=500,
        alignment=ft.alignment.center
    ),
    shape=ft.RoundedRectangleBorder(radius=15),
    content_padding=30
)

def main(page: ft.Page):
    page.title = "Ruleta"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FFF8E1"

    # Mostrar diálogo de bienvenida al inicio
    page.dialog = dialogo_bienvenida
    dialogo_bienvenida.open = True
    page.update()

    # Imprimir información del entorno para depuración
    print(f"Directorio actual: {os.getcwd()}")
    try:
        print(f"Contenido del directorio: {os.listdir('.')}")
        if os.path.exists("assets"):
            print(f"Contenido de assets: {os.listdir('assets')}")
    except Exception as e:
        print(f"No se pudo listar el directorio: {e}")
    
    # Determinar el entorno (local o Render)
    es_render = os.environ.get("RENDER") == "true"
    print(f"¿Ejecutando en Render? {es_render}")
    
    # Establecer rutas de imágenes según el entorno
    if es_render:
        # En Render, asumimos que los assets están en la raíz
        ruleta_path = "Rulete.png"
        flecha_path = "Flecha.png"
    else:
        # Localmente, usamos la carpeta assets
        ruleta_path = "assets/Rulete.png"
        flecha_path = "assets/Flecha.png"
        
    print(f"Ruta de la ruleta: {ruleta_path}")
    print(f"Ruta de la flecha: {flecha_path}")
    
    # Hacemos focus para que la página reciba los eventos de teclado
    page.focus = True

    # Letras válidas (excluyendo Ñ, X, Y, Z, Q)
    opciones = [letra for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if letra not in "ÑXYZQ"]

    notification_text = ft.Text("Presiona espacio para girar la ruleta", color="#000000", weight=ft.FontWeight.BOLD, size=22)
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
            color="#FFFFFF",
            text_align=ft.TextAlign.CENTER
        ),
        alignment=ft.alignment.center,
        visible=False,
        bgcolor=ft.colors.with_opacity(0.8, "#000000"),
        expand=True,
        animate_opacity=300,
    )

    # Contenedor overlay para la cuenta regresiva
    overlay_container = ft.Container(
        content=cuenta_regresiva_grande,
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.with_opacity(0.3, ft.colors.BLACK),
        visible=False,
        animate_opacity=300,
        margin=0,
        padding=0,
    )

    # Contenedor para la ruleta - simplificado sin verificaciones complejas
    ruleta = ft.Container(
        content=ft.Image(src=ruleta_path, width=400, height=400),
        rotate=ft.Rotate(angle=0),
        width=400, 
        height=400,
        margin=0,
        padding=0,
    )

    # Crear flecha sencilla
    flecha_container = ft.Container(
        content=ft.Image(src=flecha_path, width=70, height=70, fit="contain"),
        width=70,
        height=70,
        alignment=ft.alignment.center,
    )

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

    puntaje_text = ft.Text(value="Puntaje: 0", color="#000000", weight=ft.FontWeight.BOLD, size=20)
    tiempo_text = ft.Text(value="Tiempo: 40s", color="#000000", weight=ft.FontWeight.BOLD, size=20)

    categoria_ganadora_text = ft.Text(value="Ciencia y Tecnología", color="#000000", font_family="Bold", size=20)
    categoria_container = ft.Container(
        content=categoria_ganadora_text,
        bgcolor="#B5EAD7",
        width=630,
        height=50,
        alignment=ft.alignment.center,
        border_radius=20
    )

    # Contenedor para la subcategoría
    subcategoria_text = ft.Text(value="", color="#000000", font_family="Bold", size=18)
    subcategoria_container = ft.Container(
        content=subcategoria_text,
        bgcolor="#FFDAC1",
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
        title=ft.Container(
            content=ft.Text("¡Tiempo agotado!", size=32, weight=ft.FontWeight.BOLD),
            alignment=ft.alignment.center,
            width=300
        ),
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("Tu puntaje final es:", size=24, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        width=300
                    ),
                    ft.Container(
                        content=ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color="#FF6B6B"),
                        alignment=ft.alignment.center,
                        width=300
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("¡Buen trabajo!", size=24, weight=ft.FontWeight.BOLD, color="#4CAF50"),
                                ft.Text("Presiona cualquier botón para reiniciar", size=18, italic=True, color="#666666")
                            ],
                            spacing=10,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        width=300,
                        padding=ft.padding.only(top=10)
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            width=300,
            height=250,
            alignment=ft.alignment.center
        ),
        shape=ft.RoundedRectangleBorder(radius=15),
        content_padding=30
    )

    def mostrar_texto_grande(texto, duracion=2):
        cuenta_regresiva_grande.content.value = texto
        cuenta_regresiva_grande.content.size = 100
        overlay_container.visible = True
        cuenta_regresiva_grande.visible = True
        overlay_container.opacity = 1
        cuenta_regresiva_grande.opacity = 1
        page.update()
        time.sleep(duracion)
        overlay_container.opacity = 0
        cuenta_regresiva_grande.opacity = 0
        page.update()
        time.sleep(0.3)
        overlay_container.visible = False
        cuenta_regresiva_grande.visible = False
        page.update()

    def restablecer_letras():
        nonlocal timer_activo, letra_seleccionada, seleccion_en_curso
        timer_activo = False  # Asegurarse de que el timer se detenga
        letra_seleccionada = None  # Reiniciar letra seleccionada
        seleccion_en_curso = False  # Reiniciar estado de selección
        
        # Reiniciar letras
        for letra in opciones:
            contenedor = contenedores_letras[letra]
            contenedor.content.value = letra
            contenedor.bgcolor = colores[letra]
        
        # Reiniciar tiempo y puntaje
        tiempo_text.value = "Tiempo: 40s"
        puntaje_text.value = "Puntaje: 0"
        
        # Reiniciar ruleta
        ruleta.rotate.angle = 0
        
        # Reiniciar categoría y subcategoría
        categoria_ganadora_text.value = "Ciencia y Tecnología"
        subcategoria_text.value = ""
        
        # Reiniciar notificación
        notification_text.value = "Presiona espacio para girar la ruleta"
        
        # Mostrar diálogo de bienvenida al reiniciar
        page.dialog = dialogo_bienvenida
        dialogo_bienvenida.open = True
        page.update()

    def temporizador_regresivo():
        nonlocal timer_activo
        
        try:
            # Cuenta regresiva desde 40 segundos
            for segundos_restantes in range(40, -1, -1):
                if not timer_activo:  # Si el timer fue cancelado, salir
                    return
                    
                tiempo_text.value = f"Tiempo: {segundos_restantes}s"
                page.update()
                
                # Si llegamos a cero, mostrar diálogo
                if segundos_restantes == 0:
                    # Actualizar el puntaje en el diálogo
                    try:
                        puntaje_final = int(puntaje_text.value.split(": ")[1])
                        dialogo_tiempo_agotado.content.content.controls[1].content.value = str(puntaje_final)
                        page.dialog = dialogo_tiempo_agotado
                        dialogo_tiempo_agotado.open = True
                        page.update()
                    except Exception as e:
                        print(f"Error al actualizar el puntaje: {e}")
                    break
                    
                time.sleep(1)
        finally:
            timer_activo = False

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

        # Mostrar la categoría seleccionada en grande
        mostrar_texto_grande(f"Categoría: {categoria_ganadora_text.value}")
        
        # Esperar un momento antes de mostrar la subcategoría
        time.sleep(0.5)
        
        # Seleccionar y mostrar la subcategoría
        subcategoria = get_random_subcategory(categoria_ganadora_text.value)
        subcategoria_text.value = subcategoria
        mostrar_texto_grande(f"Subcategoría: {subcategoria}")
        page.update()

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
        
        # Color de resaltado (ya es hexadecimal)
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
                
                # Verificar que aún haya letras disponibles
                letras_disponibles = [letra for letra in opciones if contenedores_letras[letra].content.value]
                if not letras_disponibles:
                    break
                
                # Calcular el índice actual (circular)
                indice_actual = indice_actual % len(letras_disponibles)
                letra_actual = letras_disponibles[indice_actual]
                
                # Verificar que la letra actual aún existe y está visible
                if letra_actual not in contenedores_letras or not contenedores_letras[letra_actual].content.value:
                    continue
                
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
            if ultima_letra_resaltada and ultima_letra_resaltada in contenedores_letras:
                contenedor = contenedores_letras[ultima_letra_resaltada]
                if contenedor.content.value:  # Verificar que la letra aún está visible
                    letra_seleccionada = ultima_letra_resaltada
                    notification_text.value = f"Letra seleccionada: {letra_seleccionada}"
                    notification_text.color = "#000000"
                    page.update()
                    
                    # Iniciar timer solo si no está activo
                    if not timer_activo:
                        timer_activo = True
                        timer_thread = threading.Thread(target=temporizador_regresivo, daemon=True)
                        timer_thread.start()
                else:
                    # Si la letra ya no está visible, seleccionar otra
                    seleccion_en_curso = False
                    threading.Thread(target=seleccionar_letra_aleatoria, daemon=True).start()
        finally:
            seleccion_en_curso = False

    def borrar_letra_seleccionada():
        nonlocal letra_seleccionada, timer_activo
        
        if letra_seleccionada and letra_seleccionada in contenedores_letras:
            contenedor = contenedores_letras[letra_seleccionada]
            if contenedor.content.value:  # Verificar que la letra aún está visible
                contenedor.content.value = ""
                contenedor.bgcolor = "transparent"
                
                # Sumar un punto
                try:
                    puntaje_actual = int(puntaje_text.value.split(": ")[1])
                    puntaje_text.value = f"Puntaje: {puntaje_actual + 1}"
                except Exception as e:
                    print(f"Error al actualizar el puntaje: {e}")
                    puntaje_text.value = "Puntaje: 1"
                
                letra_seleccionada = None
                page.update()
                
                # Seleccionar nueva letra
                threading.Thread(target=seleccionar_letra_aleatoria, daemon=True).start()

    # Función para manejar los eventos de teclado
    def on_keyboard(e: ft.KeyboardEvent):
        nonlocal letra_seleccionada, timer_activo
        
        # Si el diálogo de bienvenida está abierto, cerrarlo con cualquier tecla
        if dialogo_bienvenida.open:
            dialogo_bienvenida.open = False
            page.update()
            return
            
        # Si el diálogo de tiempo agotado está abierto, cerrarlo con cualquier tecla
        if dialogo_tiempo_agotado.open:
            dialogo_tiempo_agotado.open = False
            restablecer_letras()
            page.update()
            return
            
        if e.key == " ":
            if dialogo_tiempo_agotado.open:  # Si el diálogo está abierto, restablecer letras
                dialogo_tiempo_agotado.open = False
                restablecer_letras()
                page.update()
            else:  # Si no, girar la ruleta
                threading.Thread(target=girar_ruleta, daemon=True).start()
        elif e.key == "Enter":
            # Borrar letra actual sin sumar punto y seleccionar nueva
            if letra_seleccionada and letra_seleccionada in contenedores_letras:
                contenedor = contenedores_letras[letra_seleccionada]
                contenedor.content.value = ""
                contenedor.bgcolor = "transparent"
                letra_seleccionada = None
                page.update()
                # Seleccionar nueva letra
                threading.Thread(target=seleccionar_letra_aleatoria, daemon=True).start()
            else:
                # Si no hay letra seleccionada, seleccionar una nueva
                threading.Thread(target=seleccionar_letra_aleatoria, daemon=True).start()
        elif e.key == "Backspace":
            # Borra la letra seleccionada, suma punto y selecciona nueva
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
        controls=[
            ft.Column(
                controls=[
                    categoria_container,
                    subcategoria_container
                ],
                spacing=10
            )
        ],
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

    page.add(contenido_principal)
    page.update()

# La instancia de la aplicación flet si es necesaria para servidores ASGI como Gunicorn
# app = ft.app(target=main, view=ft.AppView.WEB)

if __name__ == "__main__":
    # Configurar la aplicación Flet para ejecutarse en modo escritorio por defecto
    # Para modo web, se debería usar un servidor ASGI como Gunicorn
    ft.app(target=main)
