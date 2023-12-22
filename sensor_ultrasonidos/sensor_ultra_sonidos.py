#Instalar libreria si no funciona
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM);

#Asignacion de pines
trigger = 3
echo  = 2

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def ultra():
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
   print("The distance from object is ",distance,"cm")
try:
    while True:
       ultra()
       time.sleep(1)
except KeyboardInterrupt:       
    GPIO.cleanup()
