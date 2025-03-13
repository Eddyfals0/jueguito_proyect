import socket
import threading

# Lista para almacenar los clientes conectados
clientes = []

# Función para manejar cada cliente
def manejar_cliente(socket_cliente):
    while True:
        try:
            mensaje = socket_cliente.recv(1024).decode('utf-8')
            if mensaje:
                difundir_mensaje(mensaje, socket_cliente)
            else:
                eliminar_cliente(socket_cliente)
                break
        except:
            eliminar_cliente(socket_cliente)
            break

# Función para difundir mensajes a todos los clientes
def difundir_mensaje(mensaje, cliente_emisor):
    for cliente in clientes:
        if cliente != cliente_emisor:
            try:
                cliente.send(mensaje.encode('utf-8'))
            except:
                eliminar_cliente(cliente)

# Función para eliminar clientes desconectados
def eliminar_cliente(cliente):
    if cliente in clientes:
        clientes.remove(cliente)

# Configuración del servidor
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 12345))
    servidor.listen(5)
    print("Servidor iniciado en el puerto 12345")

    while True:
        socket_cliente, direccion = servidor.accept()
        print(f"Conexión establecida desde {direccion}")
        clientes.append(socket_cliente)
        hilo = threading.Thread(target=manejar_cliente, args=(socket_cliente,))
        hilo.start()

iniciar_servidor()
