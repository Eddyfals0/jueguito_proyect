import flet as ft
import random
import string
import requests
import os

def generar_codigo(longitud=6):
    """Genera un código aleatorio de la longitud especificada."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=longitud))

def main(page: ft.Page):
    page.title = "Control Ruleta"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.SURFACE_VARIANT
    page.padding = 0
    page.window_width = 400
    page.window_height = 700
    
    # Variables de estado
    conectado = False
    codigo_sesion = ""
    panel_config_visible = False
    
    # Función para enviar comandos al juego
    def enviar_comando(comando, params=None):
        if not conectado:
            mostrar_snackbar("No conectado")
            return
        
        try:
            # Aquí enviarías el comando al servidor
            mostrar_snackbar(f"Enviado: {comando}")
        except Exception as e:
            mostrar_snackbar(f"Error: {str(e)}")
    
    # Mostrar mensaje en la barra inferior
    def mostrar_snackbar(mensaje):
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje),
            duration=2000
        )
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()
    
    # Cambiar estado de conexión
    def cambiar_estado_conexion(estado, mensaje=None):
        if estado:
            indicador_conexion.color = ft.colors.GREEN
            estado_texto.value = mensaje or "Conectado"
            estado_texto.color = ft.colors.GREEN
        else:
            indicador_conexion.color = ft.colors.RED
            estado_texto.value = mensaje or "Desconectado"
            estado_texto.color = ft.colors.RED
        page.update()
    
    # Función para conectar al juego
    def conectar(e=None):
        nonlocal conectado, codigo_sesion
        codigo = campo_codigo.value.strip().upper()
        
        if len(codigo) != 6:
            mostrar_snackbar("Código inválido")
            return
        
        try:
            # Simulación de conexión exitosa
            conectado = True
            codigo_sesion = codigo
            cambiar_estado_conexion(True, f"Conectado: {codigo}")
            
            # Cambiar apariencia del botón
            btn_conectar.icon = ft.icons.LOGOUT
            btn_conectar.tooltip = "Desconectar"
            btn_conectar.bgcolor = ft.colors.RED_400
            
            # Mostrar los controles
            controles_principales.visible = True
            page.update()
        except Exception as e:
            mostrar_snackbar(f"Error: {str(e)}")
    
    def desconectar(e=None):
        nonlocal conectado, codigo_sesion
        
        if not conectado:
            return
        
        try:
            conectado = False
            codigo_sesion = ""
            cambiar_estado_conexion(False)
            
            # Cambiar apariencia del botón
            btn_conectar.icon = ft.icons.LOGIN
            btn_conectar.tooltip = "Conectar"
            btn_conectar.bgcolor = ft.colors.BLUE_400
            
            # Ocultar configuración si está visible
            if panel_config_visible:
                toggle_panel_config(None)
                
            page.update()
        except Exception as e:
            mostrar_snackbar(f"Error: {str(e)}")
    
    # Alternar la conexión
    def toggle_conexion(e):
        if conectado:
            desconectar()
        else:
            conectar()
    
    # Campo para código
    campo_codigo = ft.TextField(
        hint_text="Código de 6 dígitos",
        width=130,
        height=40,
        text_align=ft.TextAlign.CENTER,
        max_length=6,
        text_size=14,
        border_radius=20,
        filled=True,
        dense=True,
        on_submit=conectar
    )
    
    # Botón para conectar/desconectar
    btn_conectar = ft.IconButton(
        icon=ft.icons.LOGIN,
        tooltip="Conectar",
        bgcolor=ft.colors.BLUE_400,
        icon_color=ft.colors.WHITE,
        on_click=toggle_conexion
    )
    
    # Indicador de estado
    indicador_conexion = ft.Container(
        width=12,
        height=12,
        border_radius=6,
        bgcolor=ft.colors.RED
    )
    
    estado_texto = ft.Text(
        "Desconectado",
        size=12,
        color=ft.colors.RED
    )
    
    # Botones de control principales
    btn_girar = ft.ElevatedButton(
        text="GIRAR",
        icon=ft.icons.REFRESH,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.colors.GREEN_400,
            color=ft.colors.WHITE
        ),
        height=80,
        width=80,
        on_click=lambda e: enviar_comando("girar")
    )
    
    btn_seleccionar = ft.ElevatedButton(
        text="SELEC",
        icon=ft.icons.CHECK_CIRCLE,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.colors.AMBER_400,
            color=ft.colors.WHITE
        ),
        height=80,
        width=80,
        on_click=lambda e: enviar_comando("seleccionar")
    )
    
    btn_borrar = ft.ElevatedButton(
        text="BORRAR",
        icon=ft.icons.DELETE,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.colors.RED_400,
            color=ft.colors.WHITE
        ),
        height=80,
        width=80,
        on_click=lambda e: enviar_comando("borrar")
    )
    
    # Contenedor para los controles principales
    controles_principales = ft.Container(
        content=ft.Row(
            controls=[btn_girar, btn_seleccionar, btn_borrar],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=ft.padding.only(top=20, bottom=20),
        margin=ft.margin.only(top=10),
        width=page.window_width,
        visible=False
    )
    
    # Panel de configuración
    def toggle_panel_config(e):
        nonlocal panel_config_visible
        panel_config_visible = not panel_config_visible
        panel_configuracion.visible = panel_config_visible
        btn_config.icon = ft.icons.CLOSE if panel_config_visible else ft.icons.SETTINGS
        page.update()
    
    # Controles de navegación para configuración
    pad_navegacion = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.ARROW_LEFT,
                icon_color=ft.colors.WHITE,
                bgcolor=ft.colors.with_opacity(0.3, ft.colors.WHITE),
                on_click=lambda e: enviar_comando("izquierda")
            ),
            ft.IconButton(
                icon=ft.icons.ARROW_UPWARD,
                icon_color=ft.colors.WHITE,
                bgcolor=ft.colors.with_opacity(0.3, ft.colors.WHITE),
                on_click=lambda e: enviar_comando("arriba")
            ),
            ft.IconButton(
                icon=ft.icons.ARROW_DOWNWARD,
                icon_color=ft.colors.WHITE,
                bgcolor=ft.colors.with_opacity(0.3, ft.colors.WHITE),
                on_click=lambda e: enviar_comando("abajo")
            ),
            ft.IconButton(
                icon=ft.icons.ARROW_RIGHT,
                icon_color=ft.colors.WHITE,
                bgcolor=ft.colors.with_opacity(0.3, ft.colors.WHITE),
                on_click=lambda e: enviar_comando("derecha")
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )
    
    # Control de volumen
    slider_volumen = ft.Slider(
        min=0,
        max=100,
        value=50,
        width=200,
        on_change=lambda e: enviar_comando("volumen", {"nivel": e.control.value})
    )
    
    # Panel de configuración expandible
    panel_configuracion = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Controles adicionales", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                
                ft.Container(
                    content=ft.Text("Navegación", size=14),
                    margin=ft.margin.only(top=10, bottom=5)
                ),
                pad_navegacion,
                
                ft.Container(
                    content=ft.Text("Volumen", size=14),
                    margin=ft.margin.only(top=15, bottom=5)
                ),
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.VOLUME_DOWN, size=16),
                        slider_volumen,
                        ft.Icon(ft.icons.VOLUME_UP, size=16)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                
                ft.Container(height=15),
                ft.TextButton(
                    text="Cerrar",
                    icon=ft.icons.CLOSE,
                    on_click=toggle_panel_config
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        ),
        padding=20,
        bgcolor=ft.colors.with_opacity(0.95, ft.colors.SURFACE_VARIANT),
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
        width=page.window_width,
        height=300,
        visible=False,
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
    )
    
    # Botón de configuración (flotante)
    btn_config = ft.FloatingActionButton(
        icon=ft.icons.SETTINGS,
        bgcolor=ft.colors.BLUE_GREY_700,
        mini=True,
        on_click=toggle_panel_config
    )
    
    # Barra superior
    barra_superior = ft.AppBar(
        leading=ft.Icon(ft.icons.VIDEOGAME_ASSET),
        title=ft.Text("Control Ruleta"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Row(
                controls=[
                    indicador_conexion,
                    ft.Container(width=5)
                ],
                spacing=0
            )
        ]
    )
    
    # Diseño principal
    page.add(
        barra_superior,
        ft.Container(
            content=ft.Column(
                controls=[
                    # Área de conexión
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                campo_codigo,
                                btn_conectar,
                                estado_texto
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        padding=10,
                        margin=ft.margin.only(top=10),
                        alignment=ft.alignment.center
                    ),
                    
                    # Controles principales
                    controles_principales,
                    
                    # Panel de configuración (aparece desde abajo)
                    ft.Container(
                        content=panel_configuracion,
                        alignment=ft.alignment.bottom_center
                    )
                ]
            ),
            expand=True
        ),
        
        # Botón flotante
        ft.Container(
            content=btn_config,
            alignment=ft.alignment.bottom_right,
            padding=20
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER) 