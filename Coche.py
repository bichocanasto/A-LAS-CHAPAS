import pygame
import random

class Coche(pygame.sprite.Sprite):

    def __init__(self, tipo ="rosa",image = None):
        super().__init__()
        self.tipo = tipo
        self.image = self.cargar_imagen(tipo)
        self.rect = pygame.Rect(random.randint(75,95),random.randint(250,480),190,70)
        self.move_x = 0
        self.move_y = 0
    
         # Límites de movimiento vertical
        self.min_y = 250  
        self.max_y = 520  

        if tipo == "rosa":
            self.velocidad = 10
            #self.resistencia = 1 #dejar para dsp cuantas colisiones aguanta
        elif tipo == "eva":
            self.velocidad = 5
            #self.resistencia = 2
        elif tipo == "verde":
            self.velocidad = 3
            #self.resistencia = 1.5


    def cargar_imagen(self, tipo):
        # Cargar la imagen correspondiente según el tipo de coche
        if tipo == "rosa":
            return pygame.image.load("images/cocherosaALC.png").convert_alpha()
        elif tipo == "eva":
            return pygame.image.load("images/cochevioletaALC.png").convert_alpha()
        elif tipo == "verde":
            return pygame.image.load("images/cocheverdeALC.png").convert_alpha()        

    def update(self):
        # Actualiza la posición del coche en base a su velocidad
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        
        # Restringe el coche dentro del rango deseado en el eje Y
        if self.rect.y < self.min_y:
            self.rect.y = self.min_y
        elif self.rect.y > self.max_y:
            self.rect.y = self.max_y
