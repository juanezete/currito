import picamera
import pygame
from pygame.locals import *
from time import sleep

# Inicializar la cámara
camera = picamera.PiCamera()

# Ajustes opcionales (puedes personalizar según tus necesidades)
camera.resolution = (640, 480)  # Resolución del video
camera.rotation = 180  # Rotar el video (si es necesario)

# Inicializar pygame y la pantalla
pygame.init()
screen = pygame.display.set_mode((640, 480), FULLSCREEN)
pygame.display.set_caption("Video en tiempo real")
pygame.mouse.set_visible(False)

try:
    # Iniciar la vista previa
    camera.start_preview()

    # Esperar un momento para que la cámara se estabilice
    sleep(2)

    # Bucle principal para mostrar el video en tiempo real
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        # Capturar el frame actual y mostrarlo en la pantalla
        camera.capture('/tmp/frame.jpg')
        img = pygame.image.load('/tmp/frame.jpg')
        screen.blit(img, (0, 0))
        pygame.display.flip()

finally:
    # Detener la vista previa y cerrar la ventana pygame
    camera.stop_preview()
    pygame.quit()
