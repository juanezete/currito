import telebot
import RPi.GPIO as GPIO
import time
import threading
import time
import serial
import sys
import select
import socket


# Configuración del servidor
host = '0.0.0.0'  # Escucha en todas las interfaces
port = 12345  # Puerto para la conexión

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asocia el socket con la dirección y el puerto
server_socket.bind((host, port))

# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
timeout=1


GPIO.setmode(GPIO.BCM);

#Asignacion de pines
trigger = 3
echo  = 2
global comando
comando = "None"

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

def tel():
    bot.polling(none_stop=True)
#Crear dos hilos
hilo_ultra = threading.Thread(target=ultra)
hilo_telegram = threading.Thread(target=tel)


#Configuracion bot telegram
TOKEN = ('6625376467:AAG8f85d1Hg1PLqC132f1buDFkHxHTlP2xg')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Buenas, soy Currito Bot \U0001F426 para interactuar conmigo utiliza un bot de la lista!:\n /teclado \n /mando \n /aleatorio \n /voz \n /camara")
    
@bot.message_handler(commands=['teclado'])
def send_welcome(message):
    bot.reply_to(message,"Modo TECLADO activado!")
    global comando
    comando="teclado"
    
    
@bot.message_handler(commands=['aleatorio'])
def send_welcome(message):
    bot.reply_to(message,"Modo ALEATORIO activado!")
    global comando
    comando="aleatorio"
    
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

@bot.message_handler(commands=['mando'])
def send_welcome(message):
    bot.reply_to(message,"Modo MANDO activado!")
    global comando
    comando="mando"
    
#Iniciar los hilos  
hilo_ultra.start()
hilo_telegram.start()

while True:
    
    if comando=="teclado":
       
        print("Estoy en el modo teclado")
        entrada = leer_dato()
        
        if entrada is not None and cerca == 0:
            ser.write(entrada.encode())
            entrada = None
        if entrada is not None and cerca == 8:
            ser.write(str(cerca).encode())
            cerca = 0
            entrada = None
            time.sleep(1.5)
            print("Entro al if")
            
    elif comando=="mando":
        print("Modo mando")
        
    elif comando=="voz":
        while (comando == "voz"):
            print("Modo voz")
            
            # Escucha conexiones entrantes (máximo de 1 conexión en cola)
            server_socket.listen(1)

            print(f"Esperando conexión en {host}:{port}")

            # Acepta la conexión entrante
            client_socket, client_address = server_socket.accept()
            print(f"Conexión establecida desde {client_address}")

            # Recibe datos del cliente
            data = client_socket.recv(1024)
            print(f"Dato recibido: {data.decode()}")
            
    elif comando=="camara":
        print("Modo camara")
        
    elif comando=="aleatorio":
        print("Modo aleatorio")
    else:
        print("No hay modo aun")
        time.sleep(1)
        print(comando)

