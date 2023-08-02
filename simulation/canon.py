import pygame
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from PIL import Image

# Inicializar pygame
pygame.init()

# Variables de la ventana
window_width = 800
window_height = 600
window_caption = "Simulación de Pistola"

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
blue = (0, 0, 255)
golden = (212, 175, 55)

# Configuración de la ventana
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_caption)

# Variables de la pistola
gun_x = 50
gun_y = window_height // 2
gun_width = 50
gun_height = 30

sensor_x = 500
sensor_y = 580
sensor_width = 100
sensor_height = 30

# Variables de la bala
bullet_width = 10
bullet_height = 5
bullets = []  # Lista para almacenar las balas disparadas

# Variables del juego
bullet_speed = 117
bullet_count = 1
shots = 0

M = True
bullets_detected = 0


def draw_button():
    button_rect = pygame.Rect(10, window_height - 50, 100, 40)
    pygame.draw.rect(screen, gray, button_rect)
    font = pygame.font.Font(None, 30)
    text = font.render("Graficar", True, white)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)


def draw_gun():
    pygame.draw.rect(screen, white, (gun_x, gun_y, gun_width, gun_height))
    pygame.draw.rect(screen, blue, (sensor_x, sensor_y, sensor_height, sensor_height))


def draw_bullet():
    for bullet in bullets:
        pygame.draw.rect(screen, golden, (bullet[0], bullet[1], bullet_width, bullet_height))
        # print(f"Bala - Coordenadas: ({bullet[0]}, {bullet[1]})")  # Imprimir coordenadas en la consola


def main():
    global bullet_speed, bullet_count, gun_y, shots, bullets_detected

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtener posición del mouse al hacer clic
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Verificar si el clic fue dentro del botón
                if 10 <= mouse_x <= 110 and window_height - 50 <= mouse_y <= window_height - 10:
                    index = ["detectado", "no detectado"]
                    values = [bullets_detected, shots - bullets_detected]
                    plt.figure()
                    plt.bar(index, values)
                    plt.ylabel('Número de Balas')
                    plt.title('Balas Detectadas vs No Detectadas')
                    plt.grid()
                    plt.show()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            gun_y -= 5
        if keys[pygame.K_DOWN]:
            gun_y += 5
        if keys[pygame.K_LEFT]:
            bullet_speed -= 1+ np.random.normal(loc=1, scale=1)
        if keys[pygame.K_RIGHT]:
            bullet_speed += 1 + np.random.normal(loc=1, scale=1)
        if keys[pygame.K_SPACE]:
            # Disparar una bala
            shots += 1
            bullet_y = gun_y + gun_height // 2 - (bullet_height * bullet_count) // 2
            bullets.append([gun_x + gun_width, bullet_y])

        screen.fill(black)

        draw_gun()

        # Mover las balas 
        bullets_to_remove = []
        global M
        t = 0
        Tm = t + 18 + np.random.normal(loc=0.1, scale=0.1) + np.random.normal(loc=0.1, scale=0.1)
        Tnm = 0
        for i, bullet in enumerate(bullets):
            bullet[0] += bullet_speed + np.random.normal(loc=1, scale=1)
            if Tnm == 0:
                if t > Tm:
                    M = False
                    Tnm = t + 22 + np.random.normal(loc=0.1, scale=0.1)
                    Tm = 0
            elif Tm == 0:
                if t > Tnm:
                    M = True
                    Tm = t + 18 + np.random.normal(loc=0.1, scale=0.1) + np.random.normal(loc=0.1, scale=0.1)
                    Tnm = 0

            t = t + 1
            
            if bullet[0] >= 300:
                if bullet[0] < 400:
                    if M:
                        bullets_detected += 1

            if bullet[0] > window_width:
                bullets_to_remove.append(i)

        for index in reversed(bullets_to_remove):
            bullets.pop(index)

        draw_bullet()
        draw_button()

        # Mostrar datos en la ventana
        font = pygame.font.Font(None, 30)
        text = font.render(f"Velocidad de la bala: {bullet_speed}", True, white)
        screen.blit(text, (10, 10))

        text = font.render(f"Disparos: {shots}", True, white)
        screen.blit(text, (10, 40))

        text = font.render(f"Balas detectadas: {bullets_detected}", True, white)
        screen.blit(text, (10, 70))

        pygame.display.flip()
        clock.tick(60)


def ultrasonic_simulation():
    global M
    t = 0
    Tm = t + 18 + np.random.normal(loc=0.1, scale=0.1) + np.random.normal(loc=0.1, scale=0.1)
    Tnm = 0
    while True:

        if Tnm == 0:
            if t > Tm:
                M = False
                Tnm = t + 22 + np.random.normal(loc=0.1, scale=0.1)
                Tm = 0
        elif Tm == 0:
            if t > Tnm:
                M = True
                Tm = t + 18 + np.random.normal(loc=0.1, scale=0.1) + np.random.normal(loc=0.1, scale=0.1)
                Tnm = 0

        t = t + 1
        time.sleep(0.001)


if __name__ == "__main__":
    #thread = threading.Thread(target=ultrasonic_simulation)
   # thread.start()
    main()
