import pygame
import random

class Coche(pygame.sprite.Sprite):

    def __init__(self, tipo ="rosa",image = None):
        super().__init__()
        self.tipo = tipo
        self.image = self.cargar_imagen(tipo)
        self.hover_image = self.cargar_imagen_hover(tipo) #Imagen para el estado hover
        self.current_image = self.image
        self.rect = pygame.Rect(random.randint(75,95),random.randint(250,480),190,70)
        self.mask = pygame.mask.from_surface(self.image) #para la colision basada en la forma del coche y no el rectangulo
        self.move_x = 0
        self.move_y = 0
        self.speed_boost = 1
        self.max_collisions = 3
        self.background_speed = 12
    
         # Límites de movimiento vertical
        self.min_y = 250  
        self.max_y = 520  

        if tipo == "rosa":
            self.speed_boost = 1
            self.max_collisions = 3
            self.background_speed = 12
        elif tipo == "eva":
            self.speed_boost = float(1.3)
            self.max_collisions = 4
            self.background_speed = 15
        elif tipo == "verde":
            self.speed_boost = float(1.6)
            self.max_collisions = 5
            self.background_speed = 17


    def cargar_imagen(self, tipo):
        # Cargar la imagen correspondiente segun el tipo de coche
        if tipo == "rosa":
            #coche normi sin habilidades agregadas
            return pygame.image.load("images/cocherosaALC.png").convert_alpha()
        elif tipo == "eva":
            return pygame.image.load("images/cochevioletaALC.png").convert_alpha()
        elif tipo == "verde":
            return pygame.image.load("images/cocheverdeALC.png").convert_alpha()  
        
        
    def cargar_imagen_hover(self, tipo):
        # Cargar la imagen para el estado hover segun el tipo
        if tipo == "rosa":
            return pygame.image.load("images/cocherosabrillaALC.png").convert_alpha()
        elif tipo == "eva":
            return pygame.image.load("images/cochevioletabrillaALC.png").convert_alpha()
        elif tipo == "verde":
            return pygame.image.load("images/cocheverdebrillaALC.png").convert_alpha()      

    def set_hovered_state(self, hovered):
        # Cambia entre imagen original y hover
        if hovered:
            self.current_image = self.hover_image
        else:
            self.current_image = self.image
        
        self.rect = self.current_image.get_rect(center=self.rect.center)
        
        self.mask = pygame.mask.from_surface(self.current_image)

    def update(self):
        # Actualiza la posición del coche en base a su velocidad
        self.rect.x += self.move_x 
        self.rect.y += self.move_y * self.speed_boost
        
        # Restringe el coche dentro del rango deseado en el eje Y
        if self.rect.y < self.min_y:
            self.rect.y = self.min_y
        elif self.rect.y > self.max_y:
            self.rect.y = self.max_y
