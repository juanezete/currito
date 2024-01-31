import socket

# Configuración del servidor en la Raspberry Pi
host_raspberry = '0.0.0.0'  # Escucha en todas las interfaces disponibles
port_raspberry = 12345  # Mismo puerto que en el lado del cliente

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula el socket a una dirección y puerto
server_socket.bind((host_raspberry, port_raspberry))

# Escucha conexiones entrantes
server_socket.listen()

print(f"Esperando conexiones en {host_raspberry}:{port_raspberry}...")

while True:
    # Acepta la conexión cuando se recibe una solicitud
    client_socket, client_address = server_socket.accept()
    print(f"Conexión establecida desde {client_address}")

    # Recibe datos del cliente (comando enviado desde el PC)
    comando_recibido = client_socket.recv(1024).decode()

    # Muestra el comando por pantalla
    print(f"Comando recibido: {comando_recibido}")

    # Aquí puedes agregar lógica adicional según el comando recibido

    # Cierra la conexión con el cliente
    client_socket.close()
