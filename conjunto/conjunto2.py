#Instalar libreria si no funciona
import RPi.GPIO as GPIO
import time
import serial
import threading

GPIO.setwarnings(False)

#CONFIGURACION PUERTO SERIE
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

#CONFIGURACION ULTRASONIDOS
GPIO.setmode(GPIO.BCM);
distance = 100

#Asignacion de pines
trigger = 3
echo  = 2

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

##########################################################################
def ultra():
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
   
   
###########################################################################  
hilo_ultra = threading.Thread(target=ultra)      
hilo_ultra.start();

try:
    
    while True:
        
        # Envía datos al Arduino
        if (distance < 15):
            print("Menor distancia\n")
            ser.write("5".encode())
        else:    
            dato = input("Envia comando a : ")
            ser.write(dato.encode())

        time.sleep(1)  # Espera antes de enviar el siguiente dato

except KeyboardInterrupt:
    # Maneja la interrupción del teclado (Ctrl+C)
    print("Programa interrumpido")
    ser.close()


