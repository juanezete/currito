import RPi.GPIO as GPIO
import serial
import time
import threading
import sys
import select

# Desactivar las advertencias de GPIO
GPIO.setwarnings(False)

# Configuración de GPIO para el sensor ultrasónico
GPIO.setmode(GPIO.BCM)
trigger = 3
echo = 2
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

# Configuración del puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Variable para almacenar la distancia medida por el sensor ultrasónico
distance = 0

# Función para medir la distancia con el sensor ultrasónico
def ultra():
    global distance  # Utiliza la variable global para almacenar la distancia medida
    while True:
        GPIO.output(trigger, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trigger, GPIO.LOW)

        while GPIO.input(echo) == 0:
            signaloff = time.time()

        while GPIO.input(echo) == 1:
            signalon = time.time()

        timepassed = signalon - signaloff
        distance = (timepassed * 34300) / 2
        
        if distance < 15:
            print("La distancia del objeto es:", distance, "cm")
            ser.write("5".encode())  # Si la distancia es menor a 15, envía 'e'
            
        time.sleep(1)   

# Función para enviar un carácter al Arduino desde el teclado
def enviar_caracter():
    try:
        while True:
            # Chequear si hay entrada en la consola (lectura no bloqueante)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                comando = input("Comando enviado")
                ser.write(comando.encode())

    except KeyboardInterrupt:
        # Maneja la interrupción del teclado (Ctrl+C)
        print("Programa de envío interrumpido")
        ser.close()

# Crea dos hilos para ejecutar ambas funciones simultáneamente
thread_ultra = threading.Thread(target=ultra)
thread_enviar_caracter = threading.Thread(target=enviar_caracter)

try:
    # Inicia ambos hilos
    thread_ultra.start()
    thread_enviar_caracter.start()

    # Espera a que ambos hilos terminen (esto no bloquea la medición)
    thread_ultra.join()
    thread_enviar_caracter.join()

except KeyboardInterrupt:
    # Maneja la interrupción del teclado (Ctrl+C)
    print("Programa principal interrumpido")
    GPIO.cleanup()
    ser.close()
