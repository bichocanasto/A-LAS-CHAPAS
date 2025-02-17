import pygame
import random

class Roca(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image= random.choice([pygame.image.load("images/cocherosaALC.png").convert_alpha(),
                      pygame.image.load("images/cochevioletaALC.png").convert_alpha(),
                      pygame.image.load("images/cocheverdeALC.png").convert_alpha(),
                      pygame.image.load("images/cocheloco.png").convert_alpha(),
                      pygame.image.load("images/cochecircusALC.png").convert_alpha(),
                      pygame.image.load("images/cocheblack.png").convert_alpha()
                      ])
        self.image_collision = pygame.image.load("images/crash.png").convert_alpha()
        self.rect =  pygame.Rect(random.randint(790,800),random.randint(250,480),190,70)
        self.mask = pygame.mask.from_surface(self.image)

         # Límites de movimiento vertical
        self.min_y = 250  # Limite superior
        self.max_y = 480  # Limite inferior, ajusta segun la altura de la pantalla
        self.spawn_time = pygame.time.get_ticks()  # Tiempo en que la roca aparecio
        self.collided = False  # Atributo para saber si ya colisio

    def change_image_on_collision(self):
        if not self.collided:  # Cambia la imagen solo si no ha colisionado antes
            self.image = self.image_collision
            self.collided = True  # Marca como colisionada para evitar multiples registros

    def update(self):
        self.rect.x +=-8
