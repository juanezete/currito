import serial
import time

# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

try:
    while True:
        # Envía datos al Arduino
        dato = input("Envia comando a : ")
        ser.write(dato.encode())

        time.sleep(1)  # Espera antes de enviar el siguiente dato

except KeyboardInterrupt:
    # Maneja la interrupción del teclado (Ctrl+C)
    print("Programa interrumpido")
    ser.close()
