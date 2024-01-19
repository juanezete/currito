import socket

# Configuración del servidor
host = '0.0.0.0'  # Escucha en todas las interfaces
port = 12345  # Puerto para la conexión

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asocia el socket con la dirección y el puerto
server_socket.bind((host, port))

# Escucha conexiones entrantes (máximo de 1 conexión en cola)
server_socket.listen(1)

comando = "voz"

while comando == "voz":
    print("Modo voz")

    try:
        # Acepta la conexión entrante
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida desde {client_address}")

        # Recibe datos del cliente
        data = client_socket.recv(1024)
        print(f"Dato recibido: {data.decode()}")

        # Agrega aquí la lógica para manejar el comando recibido

    except Exception as e:
        print(f"Error al recibir datos: {e}")
    finally:
        # Cierra la conexión
        if client_socket:
            client_socket.close()

# Cierra el socket del servidor al salir del bucle
server_socket.close()
