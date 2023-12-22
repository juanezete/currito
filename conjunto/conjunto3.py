#Instalar libreria si no funciona
import RPi.GPIO as GPIO
import time
import threading
import time
import serial
import sys
import select

# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
timeout=1


GPIO.setmode(GPIO.BCM);

#Asignacion de pines
trigger = 3
echo  = 2

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def ultra():
   global cerca
   cerca = 0
   while True :
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
       
       if (distance < 70):
           cerca = 8
           
       time.sleep(0.5)   
       
def leer_dato():
    # Envía datos al Arduino
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()
    else:
        return None
    
#Crear dos hilos
hilo_ultra = threading.Thread(target=ultra)

#Iniciar los hilos  
hilo_ultra.start()

try:
    while True:
        entrada = leer_dato()
        
        if entrada is not None and cerca == 0:
            ser.write(entrada.encode())
            entrada = None
        if entrada is not None and cerca == 8:
            ser.write(str(cerca).encode())
            cerca = 0
            entrada = None
            time.sleep(0.55)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Fin del programa")