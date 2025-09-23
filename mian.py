# Instalar pygame si no lo tienes: pip install pygame
import pygame
import random
import math
from pygame import mixer
import io


# Inicializar Pygame
pygame.init()


# Configurar la pantalla
pantalla = pygame.display.set_mode((800, 600))


# Título de la ventana e icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load('img/icono.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('img/Fondo.jpg')


# Música de fondo
mixer.music.load('music/MusicaFondo.mp3')
mixer.music.set_volume(0.8)
mixer.music.play(-1)


# Variables del Jugador
img_jugador = pygame.image.load('img/cohete.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0


# Variables del Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8


# Crear múltiples enemigos
for i in range(cantidad_enemigos):

    img_enemigo.append(pygame.image.load('img/enemigo.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(.5)
    enemigo_y_cambio.append(40)


# Variables de la BALA
img_bala = pygame.image.load('img/bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False


# Puntuación
puntuacion = 0


# Función para convertir la fuente a bytes
def fuente_a_bytes(fuente_path):
    with open(fuente_path, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


# Configuración de la fuente
fuente_como_bytes = fuente_a_bytes('font/fastest/Fastest.ttf')
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10


# Texto de fin del juego
fuente_final = pygame.font.Font(fuente_como_bytes, 40)


# Función para mostrar el texto de fin del juego
def texto_final():
    texto_final_render = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(texto_final_render, (120, 200))


# Función para mostrar la puntuación
def mostrar_puntuacion(x, y):
    puntuacion_render = fuente.render("Puntuación: " + str(puntuacion), True, (255, 255, 255))
    pantalla.blit(puntuacion_render, (x, y))


# Función para dibujar al jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Función para dibujar al enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Función para disparar la bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# Función para detectar colisiones
def hay_colision(enemi_x, enemi_y, bal_x, bal_y):
    distancia = math.sqrt((math.pow(enemi_x - bal_x, 2)) + (math.pow(enemi_y - bal_y, 2)))
    if distancia < 27:
        return True
    return False


# Loop principal
ejecutar = True
while ejecutar:


    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))


    # Manejo de eventos
    for event in pygame.event.get():


        # Cerrar la ventana
        if event.type == pygame.QUIT:
            ejecutar = False


        # Movimiento del jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio -= 1
            if event.key == pygame.K_RIGHT:
                jugador_x_cambio += 1
            if event.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('music/disparo.mp3')
                sonido_bala.set_volume(0.5)
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)


        # Detener el movimiento cuando se suelta la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0


    # Actualizar la posición del jugador
    jugador_x += jugador_x_cambio


    # Mantener al jugador dentro de los límites de la pantalla
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736


    # Actualizar la posición del enemigo
    for i in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[i] > 500:
            for j in range(cantidad_enemigos):
                enemigo_y[j] = 2000
            texto_final()
            break

        enemigo_x[i] += enemigo_x_cambio[i]

        # Cambiar dirección al llegar a los bordes
        if enemigo_x[i] <= 0:
            enemigo_x_cambio[i] = .5
            enemigo_y[i] += enemigo_y_cambio[i]
        elif enemigo_x[i] >= 736:
            enemigo_x_cambio[i] = -.5
            enemigo_y[i] += enemigo_y_cambio[i]

        # Detectar colisión
        colision = hay_colision(enemigo_x[i], enemigo_y[i], bala_x, bala_y)
        if colision:
            sonido_explosion = mixer.Sound('music/Golpe.mp3')
            sonido_explosion.set_volume(0.5)
            sonido_explosion.play()
            bala_y = 500
            bala_visible = False
            puntuacion += 1
            enemigo_x[i] = random.randint(0, 736)
            enemigo_y[i] = random.randint(50, 200)

        # Dibujar al enemigo en su posición
        enemigo(enemigo_x[i], enemigo_y[i], i)


    # Actualizar la posición de la bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    # Disparar la bala
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio


    # Dibujar al jugador en la nueva posición
    jugador(jugador_x, jugador_y)


    # Mostrar la puntuación
    mostrar_puntuacion(texto_x, texto_y)


    # Actualizar la pantalla
    pygame.display.update()
