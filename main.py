#Librerías para el desarrollo del proyecto
import telebot
import RPi.GPIO as GPIO
import time
import threading
import time
import serial
import sys
import select
import socket
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import numpy as np
import imutils

#----------- CONFIGURACIÓN CONEXIÓN CON EL PC DE JUAN
#La conexión con el ordenador de Juan sirve para activar el modo voz, ya que la raspberry no tiene micrófono
# Configuración del servidor 
host = '0.0.0.0'  # Escucha en todas las interfaces
port = 12345  # Puerto para la conexión

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asocia el socket con la dirección y el puerto
server_socket.bind((host, port))

# Escucha conexiones entrantes (máximo de 1 conexión en cola)
server_socket.listen(1)

#----------- CONFIGURACIÓN CONEXIÓN CON EL ARDUINO
# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
timeout=1


#----------- CONFIGURACIÓN ULTRASONIDOS
#Asignacion de pines
trigger = 3
echo  = 2
GPIO.setmode(GPIO.BCM);
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

#----------- VARIABLES PARA LOS MODOS
global comando
comando = "None"

#----------- CONFIGURACIÓN CÁMARA
defaultSpeed = 80
windowCenter = 320
centerBuffer = 10
pwmBound = float(50)
cameraBound = float(320)
kp = (pwmBound / cameraBound)*1.4
leftBound = int(windowCenter - centerBuffer)
rightBound = int(windowCenter + centerBuffer)
error = 0
ballPixel = 0

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def pwmStop():
#cambiar print
    enviar_dato(0,0,0)

#Camera setup
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size = (640, 480))

time.sleep(0.1)

lower_yellow = np.array([13, 50, 0])
upper_yellow = np.array([30, 255, 255])

camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)

#----------- FUNCIONES
def enviar_dato(dato1, dato2, dato3):
    #-- Envío de la velocidad para los motores de la ruedas y del servo
    
        dato1 = int(dato1) # motor de la derecha
        dato2 = int(dato2) #motor de la izquierda
        dato3 = int(dato3) #servo
        data = f"{dato2},{dato1}, {dato3} \n"
                
        ser.write(data.encode()) #envía por el puerto serial las velocidades
        print(data.encode())
        

def ultra():
    #-- Medida del ultrasonidos
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
       
       if (distance < 45): 
           cerca = 1
           
       time.sleep(0.5)   
       
def leer_dato():
    # -- Lee los números o letras escritos por el teclado
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()
    else:
        return None




#----------- CONFIGURACIÓN DEL BOT DE TELEGRAM
def tel():
    #-- Inicializa el bot de telegram
    bot.polling(none_stop=True)
TOKEN = ('6625376467:AAG8f85d1Hg1PLqC132f1buDFkHxHTlP2xg')
bot = telebot.TeleBot(TOKEN)
#A continuación, se describe los distintos comandos para el bot de telegram
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Buenas, soy Currito Bot \U0001F426 para interactuar conmigo utiliza un bot de la lista!:\n /teclado \n /mando \n /aleatorio \n /voz \n /camara")
    
@bot.message_handler(commands=['teclado'])
def send_welcome(message):
    bot.reply_to(message,"Modo TECLADO activado!")
    global comando
    comando="teclado"
    
    
@bot.message_handler(commands=['voz'])
def send_welcome(message):
    bot.reply_to(message,"Modo VOZ activado!")
    global comando
    comando="voz"
    
@bot.message_handler(commands=['camara'])
def send_welcome(message):
    bot.reply_to(message,"Modo CÁMARA activado!")
    global comando
    comando="camara"

    
#----------- HILOS    
#Para poder ejecutar el ultrasonidos y el bot de telegram al mismo tiempo, ha sido necesario la implementación de dos hilos
hilo_ultra = threading.Thread(target=ultra)
hilo_telegram = threading.Thread(target=tel)
#Iniciar los hilos  
hilo_ultra.start()
hilo_telegram.start()

#----------- EJECUCIÓN DEL CÓDIGO
while True:
    
    if comando=="teclado":
       
        print("Estoy en el modo teclado")
        entrada = leer_dato()
        
        if entrada is not None and cerca == 0:
            #Para el movimiento del robot se han empleado las siguiente letras:
            if (entrada == "w"): #Hacia delante
                enviar_dato(90,60,0)
            elif (entrada == "s"):  #Hacia atrás
                enviar_dato(-80,-60,0)
            elif (entrada == "a"): #Giro izquierda
                enviar_dato(90,60,0)
            elif (entrada == "d"): #Giro derecha
                enviar_dato(60,70,0)
            elif (entrada == "q"): #Parada
                enviar_dato(0,0,0)
            elif (entrada == "x"): #Giro de la cabeza hacia la derecha
                enviar_dato(0,0,90)
            elif (entrada == "z"): #Giro de  la cabeza hacia la izquierda
                enviar_dato(0,0,0)
            entrada = None
            time.sleep(0.1)
        if cerca == 1: #Si detecta algún objeto
            enviar_dato(40,-40,0) #Gira sobre si mismo hasta que se le manda por teclado otra indicación
            time.sleep(1.5)
            cerca = 0
            entrada = None
            print("Entro al if")
        
    elif comando=="voz":
        while (comando == "voz"):
            print("Modo voz")

            print(f"Esperando conexión en {host}:{port}")

            # Acepta la conexión entrante
            client_socket, client_address = server_socket.accept()
            print(f"Conexión establecida desde {client_address}")

            # Recibe datos del cliente
            data = client_socket.recv(1024)
            data_type = type(data)
            print(f"Tipo de dato recibido: {data_type}")
            print(f"Dato recibido: {data.decode()}")
            data_conv = (data.decode('utf-8'))
            if (data_conv == "8"): #avanza
                print("entro")
                enviar_dato(120,100,0)
            elif (data_conv == "2"): #retrocede
                enviar_dato(-120,-100,0)
            elif (data_conv == "3"): #gira hacia la izquierda
                enviar_dato(130,70,0)
            elif (data_conv == "4"): #gira hacia la derecha
                enviar_dato(80,130,0)
            elif (data_conv == "5"): #se detiene
                enviar_dato(0,0,0)

            
    elif comando=="camara":
        print("Modo camara")
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #Captura una imagen de la cámara
            image = frame.array
            output = image.copy()
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            #Genera una máscara para identificar la bola de color amarillo
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            output = cv2.bitwise_and(output, output, mask=mask)
            gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 3, 500, minRadius = 10, maxRadius = 200, param1 = 100,  param2 = 60)
            ballPixel = 0
        
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, radius) in circles:
        
                    cv2.circle(output, (x, y), radius, (0, 255, 0), 4)
        
                    if radius > 10:
                        ballPixel = x
                    else:
                        ballPixel = 0
        
            cv2.imshow("output", output)
            key = cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)
        
            #Control proporcional para ajustar la velocidad de los motores de las ruedas
            if ballPixel == 0:
                error = 0
                pwmStop()
            elif (ballPixel < leftBound) or (ballPixel > rightBound): 
                error = windowCenter - ballPixel
                pwmOut = abs(error * kp) 
                turnPwm = pwmOut + defaultSpeed
                if  ballPixel < (leftBound): #Gira hacia la derecha
                    if radius > 50 and ballPixel < 110:
                        print (ballPixel)
                        enviar_dato(defaultSpeed*1.5,defaultSpeed - 30, 0)
                    else:
                        enviar_dato(turnPwm*1.5, defaultSpeed, 0)
                elif ballPixel > (rightBound): #Gira hacia la izquierda
                    if radius > 50 and ballPixel > 540:
                        print (ballPixel)
                        enviar_dato(defaultSpeed - 30, defaultSpeed, 0)
                    else:
                        enviar_dato(defaultSpeed, turnPwm, 0)
                else:
                    if (radius < 40): #Continua recto
                        enviar_dato(defaultSpeed, defaultSpeed, 0)
                    else:
                        pwmStop()
        
            if key == ord('q'): #Parada
                break
            
            time.sleep(0.8)
        
        #Cerrar las ventanas para cambiar de modo
        cv2.destroyAllWindows()
        camera.close()
        pwmStop()
        GPIO.cleanup()
    else:
        print("No hay modo aun")
        time.sleep(1)

