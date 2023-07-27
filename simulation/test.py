import pygame
import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt

width, height = 800, 600


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = velocidad

    def update(self):
        self.rect.y += self.speed_y


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Simulación de Balas")

    balas = pygame.sprite.Group()
    clock = pygame.time.Clock()
    balas_generadas = 0
    balas_detectadas = 0

    running = False  # Estado inicial del botón (pausado)

    font = pygame.font.SysFont('Arial', 24)
    start_pause_button = pygame.Rect(10, 10, 100, 40)
    button_text = font.render("Start", True, (0, 0, 0))

    mostrar_grafica_button = pygame.Rect(10, 80, 150, 60)
    mostrar_grafica_text = font.render("Mostrar Gráfica", True, (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_pause_button.collidepoint(event.pos):
                    running = not running
                    button_text = font.render("Pause" if running else "Start", True, (0, 0, 0))
                elif mostrar_grafica_button.collidepoint(event.pos):
                    # Mostrar gráfica de balas detectadas y no detectadas
                    index = ["detectado", "no detectado"]
                    values = [balas_detectadas, balas_generadas - balas_detectadas]
                    plt.figure()
                    plt.bar(index, values)
                    plt.ylabel('Número de Balas')
                    plt.title('Balas Detectadas vs No Detectadas')
                    plt.legend()
                    plt.grid()
                    plt.show()

        screen.fill((255, 255, 255))

        # Generar balas de acuerdo a la distribución de Poisson
        if running:
            num_balas = np.random.poisson(lam=5)  # Tasa promedio de 5 balas por segundo
            for _ in range(num_balas):
                x, y = random.randint(50, 750), 0
                velocidad = np.random.normal(loc=300, scale=50)  # Velocidad promedio de 300 píxeles/segundo
                balas.add(Bala(x, y, velocidad))
                balas_generadas += 1

            balas.update()

            for bala in balas:
                if bala.rect.y < height:
                    screen.blit(bala.image, bala.rect)
                    distancia = height - bala.rect.y

                    # Simulación de sensor de ultrasonido
                    tiempo_de_pulso = distancia / 343  # Velocidad del sonido en el aire a 20°C (343 m/s)
                    if tiempo_de_pulso <= 0.016:  # Tiempo máximo que tardaría el pulso en regresar (16 ms)
                        balas_detectadas += 1
                        balas.remove(bala)  # Eliminamos la bala detectada para evitar que se cuente dos veces

        font = pygame.font.SysFont("Arial", 24)
        texto_renderizado = font.render(f"Balas generadas: {balas_generadas}", True, (0, 0, 0))
        screen.blit(texto_renderizado, (550, 50))

        texto_bd = font.render(f"Balas detectadas: {balas_detectadas}", True, (0, 0, 0))
        screen.blit(texto_bd, (200, 50))

        pygame.draw.rect(screen, (200, 200, 200), start_pause_button)
        screen.blit(button_text, (20, 20))

        pygame.draw.rect(screen, (200, 200, 200), mostrar_grafica_button)
        screen.blit(mostrar_grafica_text, (20, 100))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
