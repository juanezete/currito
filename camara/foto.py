from picamera import PiCamera
from time import sleep

# Inicializar la cámara
camera = PiCamera()

# Ajustes opcionales (puedes personalizar según tus necesidades)
camera.resolution = (1024, 768)  # Resolución de la imagen
camera.rotation = 180  # Rotar la imagen (si es necesario)

# Capturar una imagen
camera.start_preview()  # Iniciar la vista previa
sleep(2)  # Esperar un momento para que la cámara se estabilice
camera.capture('/home/pi/Desktop/codigo/camara/fotos/imagen.jpg')  # Capturar la imagen
camera.stop_preview()  # Detener la vista previa

print("Imagen capturada exitosamente!")
