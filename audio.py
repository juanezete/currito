import speech_recognition as sr
import socket

# Configuración del cliente para la Raspberry Pi
host_raspberry = '192.168.142.60'
port_raspberry = 12345  # Mismo puerto que en el lado del servidor

# Función para enviar comandos a la Raspberry Pi
def enviar_comando(comando):
    try:
        # Crea un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conéctate al servidor (Raspberry Pi)
        client_socket.connect((host_raspberry, port_raspberry))

        # Envia el comando a la Raspberry Pi
        client_socket.sendall(comando.encode())

        # Cierra la conexión
        client_socket.close()
    except Exception as e:
        print(f"Error al enviar el comando a la Raspberry Pi: {e}")


recognizer = sr.Recognizer()
mic = sr.Microphone()
tiempo_escucha = 5

while True:
    with mic as source:
        try:
            print("Escuchando...")
            audio = recognizer.listen(source, timeout=tiempo_escucha)
            print("Fin de escucha \n")
            text = recognizer.recognize_google(audio, language='es')

            if ("currito" in text.lower() or "burrito" in text.lower() or "rito" in text.lower()):
                print(f'Has dicho: {text}')
                if ("avanza" in text.lower() or "adelante" in text.lower() or "camina" in text.lower() or "continua" in text.lower()):
                    #Manda un 8 a la raspberry
                    enviar_comando("8")
                    print(f'Manda un 8')
                elif("atras" in text.lower() or "retrocede" in text.lower()):
                    #Manda un 2 a la raspberry
                    enviar_comando("2")
                    print(f'Manda un 2')
                elif("derecha" in text.lower()):
                    #Manda un 3 a la raspberry
                    enviar_comando("4")
                    print(f'Manda un 4')
                elif("izquierda" in text.lower()): 
                    #Manda un 4 a la raspberry
                    enviar_comando("3")
                    print(f'Manda un 3')
                elif("para" in text.lower() or "parate" in text.lower()):
                    #manda un 5 a la raspberry
                    enviar_comando("5")
                    print(f'Manda un 5')
                break  # Sale del bucle si se detecta "oye" y "currito"
            else:
                print(f'Palabra clave no detectada. Vuelve a intentar.')
                print(f'Has dicho: {text}')

        except sr.WaitTimeoutError:
            print("Tiempo de espera agotado. No se detectó ninguna palabra clave. Volviendo a escuchar...")
            continue  # Continúa el bucle si no se detecta ninguna palabra clave

        except sr.UnknownValueError:
            print("No se pudo reconocer ninguna palabra en el audio. Volviendo a escuchar...")
            continue  # Continúa el bucle si no se detecta ninguna palabra clave

    # Si llega a este punto, significa que se detectó una palabra clave
    break
