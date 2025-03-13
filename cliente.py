import flet as ft
import socket
import threading

# Clase para manejar el cliente de chat
class ClienteChat:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Chat en Línea"
        self.chat = ft.Column()
        self.nuevo_mensaje = ft.TextField(hint_text="Escribe tu mensaje aquí...", expand=True)
        self.boton_enviar = ft.ElevatedButton("Enviar", on_click=self.enviar_mensaje)
        self.page.add(self.chat, ft.Row([self.nuevo_mensaje, self.boton_enviar]))

        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_cliente.connect(('127.0.0.1', 12345))

        self.recibir_hilo = threading.Thread(target=self.recibir_mensajes)
        self.recibir_hilo.start()

    def enviar_mensaje(self, e):
        mensaje = self.nuevo_mensaje.value
        self.socket_cliente.send(mensaje.encode('utf-8'))
        self.nuevo_mensaje.value = ""
        self.page.update()

    def recibir_mensajes(self):
        while True:
            try:
                mensaje = self.socket_cliente.recv(1024).decode('utf-8')
                if mensaje:
                    self.chat.controls.append(ft.Text(mensaje))
                    self.page.update()
            except:
                break

def main(page: ft.Page):
    ClienteChat(page)

ft.app(target=main)
