import pygame
import random
import time
import Coche
import Roca
import sys
from Boton import Boton

# width and height of the display
# Configuración de pantalla y variables globales
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 100

clock = pygame.time.Clock()
isFullscreen = False

pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("A LAS CHAPAS")
#my_font = pygame.font.SysFont('Comic Sans MS', 24)
imgSpace = pygame.image.load("images/pista10ALC.png").convert()

# Variables para el fondo y animación
ancho_pista = imgSpace.get_width()
offset_x_pista = 0
#car = Coche.Coche()


coche_rosa = Coche.Coche("rosa", "images/cocherosaALC.png")
coche_eva = Coche.Coche("eva", "images/cochevioletaALC.png")
coche_verde = Coche.Coche("verde", "images/cocheverdeALC.png")
car = coche_rosa # Inicializar el coche predeterminado
roca = Roca.Roca()
rocas = pygame.sprite.Group()
paused = False


#Música de fondo y otros
sonidos = {
    "sonido_choque": pygame.mixer.Sound("sonido/choque.mp3"),
    "sonido_eleccion": pygame.mixer.Sound("sonido/eleccion.mp3"),
    "sonido_car": pygame.mixer.Sound("sonido/car-straring-sound-126708.mp3"),
    "sonido_over": pygame.mixer.Sound("sonido/gameover.mp3")
}

# Diccionario para música
musica = {
    "menu": "sonido/menu.mp3",
    "nivel1": "sonido/nivel1.0.mp3",
}

# Reproducir sonido
#sonidos["sonido_car"].play()

# Cambiar música
def cambiar_musica(nombre, loop=-1):
    pygame.mixer.music.load(musica[nombre])
    pygame.mixer.music.play(loop)


#PRUEBA MAIN MENU ON
pygame.display.set_caption("Menu")

BG = pygame.image.load("images/BG.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("images/font.ttf", size)


def pantalla_seleccion_personaje():
# Definir áreas para cada coche
    global areas_coches, screen, seleccion, ejecutando, car
    areas_coches = [
        (coche_rosa, pygame.Rect(30, 155, 240, 140)),
        (coche_eva, pygame.Rect(280, 265, 240, 140)),
        (coche_verde, pygame.Rect(530, 370, 240, 140))
    ]

    seleccion = None
    ejecutando = True

def options():
    while True:
        global car, coche_rosa, coche_eva, coche_verde, areas_coches, screen, seleccion, ejecutando

        pantalla_seleccion_personaje()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("yellow2")

        for coche, area in areas_coches:
            # Dibuja el rectángulo en el área del coche
            pygame.draw.rect(screen, (30, 136, 229), area, 5)  # Rectángulo con grosor 5

            # Dibuja la imagen del coche en el centro del rectángulo
            screen.blit(coche.image, (area.x + (area.width - coche.image.get_width()) // 2,
                                      area.y + (area.height - coche.image.get_height()) // 2))

        # Mostrar los coches en sus áreas
        #for coche, area in areas_coches:
        #    screen.blit(coche.image, area.topleft)  

        OPTIONS_TEXT = get_font(55).render("ELEGI AUTO", True, "purple")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 75))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Boton(image=None, pos=(400, 560), 
                            text_input="VOLVER AL MENU PRINCIPAL", font=get_font(15), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        #Arrancamo el fruteo

        coche_rosa = Coche.Coche()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for coche, area in areas_coches:
                    if area.collidepoint(event.pos):
                        sonidos["sonido_car"].play()
                        car = coche  # Asignar coche seleccionado a 'car'
                        ejecutando = False  # Salir de la selección
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                ejecutando = False  # Salir sin seleccionar un coche
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    global screen
    cambiar_musica("menu")
    while True:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("A LAS CHAPAS", True, "purple")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 90))

        PLAY_BUTTON = Boton(image=pygame.image.load("images/Play Rect.png"), pos=(400, 230), 
                            text_input="JUGAR", font=get_font(45), base_color="yellow", hovering_color="Green")
        OPTIONS_BUTTON = Boton(image=pygame.image.load("images/Options Rect.png"), pos=(400, 375), 
                            text_input="ELEGI AUTO", font=get_font(45), base_color="yellow", hovering_color="Green")
        QUIT_BUTTON = Boton(image=pygame.image.load("images/Quit Rect.png"), pos=(400, 520), 
                            text_input="SALIR", font=get_font(45), base_color="yellow", hovering_color="Green")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sonidos["sonido_eleccion"].play()
                    game()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sonidos["sonido_eleccion"].play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sonidos["sonido_eleccion"].play()
                    pygame.quit()
                    sys.exit()
           
        
        pygame.display.update()
        


def game():
    global screen, clock, game_on, isFullscreen, offset_x_pista, acceleration, roca_timer, roca_collision, roca_col_cont, elapsed_time, sonido_choque
    #time.sleep(2)
    pygame.mixer.music.stop()
    sonidos["sonido_car"].play()
    
    # Registrar el tiempo de inicio
    start_time = pygame.time.get_ticks()
    
    # Pausa inicial
    start_time_pausa = pygame.time.get_ticks()
    pausa_duracion = 4000  # milisegundoS
    preparando = True
    
    while preparando:
        current_time = pygame.time.get_ticks()
        if current_time - start_time_pausa >= pausa_duracion:
            preparando = False
        else:
            # Mostrar mensaje durante la pausa
            screen.blit(imgSpace,(0,0))
            texto = get_font(30).render("¡PREPARATE QUE ARRANCAMOS!", True, ("purple"))
            #MENU_TEXT = get_font(60).render("A LAS CHAPAS", True, "purple")
            #texto = fuente.render("¡PREPARATE QUE ARRANCA!", True, (255, 255, 255))
            screen.blit(texto, (screen.get_width() // 2 - texto.get_width() // 2,
                                screen.get_height() // 2 - texto.get_height() // 2 + 100))
            pygame.display.flip()
            clock.tick(FPS)

    # Reiniciar el tiempo para el juego principal
    start_time = pygame.time.get_ticks()
    cambiar_musica("nivel1")
    
    
    
    roca_timer = pygame.time.get_ticks()
    roca_interval = 1000
    roca_collision = False
    roca_col_cont = 0
    rocas.empty()  # Limpiar grupo de rocas

    game_on = True
    while game_on:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_on = False
                elif event.key == pygame.K_DOWN:
                    car.move_y = 7
                elif event.key == pygame.K_UP:
                    car.move_y = -7
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_f:
                    isFullscreen = not isFullscreen
                    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN) if isFullscreen else pygame.display.set_mode(RESOLUTION)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_DOWN, pygame.K_UP]:
                    car.move_y = 0


        screen.fill((135, 206, 235))
        x_relativa = offset_x_pista % ancho_pista
        screen.blit(imgSpace, (x_relativa - ancho_pista, 0))
        screen.blit(imgSpace, (x_relativa, 0))
        offset_x_pista -= 12


        collided_rocas = pygame.sprite.spritecollide(car, rocas, False)
        for roca in collided_rocas:
            if not roca.collided:  # Solo cuenta si la roca no ha colisionado antes
                roca.change_image_on_collision()
                roca_col_cont += 1  # Incrementa el contador una sola vez por roca
                sonidos["sonido_choque"].play()

        

    # Cambiar la imagen de la roca colisionada

            if roca_col_cont == 3:
                game_over_screen()
                return 
        if pygame.time.get_ticks() - roca_timer >= roca_interval:
            rocas.add(Roca.Roca())
            roca_timer = pygame.time.get_ticks()
            roca_collision = False


        for roca in rocas:
            screen.blit(roca.image, roca.rect)
            roca.update()
            if roca.rect.x < -roca.rect.width:
                roca.kill()


        
        screen.blit(car.image, car.rect)
        car.update()



       # Mostrar el tiempo en pantalla
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Segundos
        #font = pygame.font.Font(None, 36)
        font = pygame.font.SysFont('Comic Sans MS', 36)
        time_text = font.render(f"{elapsed_time} Km", True, (230, 51, 255))
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def play():
    game()  # Llama a la función del juego directamente para iniciar la partida


def game_over_screen():
    global elapsed_time
    pygame.mixer.music.stop()
        # Fondo de Game Over (opcional)
    screen.fill((0, 0, 0))  # Color de fondo negro, por ejemplo
    sonidos["sonido_over"].play()

    # Fuente y color del texto
    font = pygame.font.SysFont('Comic Sans MS', 56)
    color = (51, 178, 255)

    # Primera
    line1 = font.render("ALPISTE PERDISTE", True, color)
    line1_rect = line1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
    screen.blit(line1, line1_rect)

    # Segunda
    line2 = font.render((f"¡¡Lograste recorrer {elapsed_time} Km!!"), True, color)
    line2_rect = line2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(line2, line2_rect)

    # Tercera
    #line3 = font.render("¡Gracias por jugar!", True, color)
    #line3_rect = line3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
    #screen.blit(line3, line3_rect)

    pygame.display.flip()
    time.sleep(3)  # Pausa de 2 segundos antes de volver al menú
    main_menu()

main_menu()
