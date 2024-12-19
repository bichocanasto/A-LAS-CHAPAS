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
screen = pygame.display.set_mode((RESOLUTION),  pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("A LAS CHAPAS")
#my_font = pygame.font.SysFont('Comic Sans MS', 24)
imgSpace = pygame.image.load("images/pista12diaALC.png").convert()
imgSpace2 = pygame.image.load("images/pista12tardeALC.png").convert()
imgSpace3 = pygame.image.load("images/pista12nocheALC.png").convert()
ancho_pista = imgSpace.get_width()

# Variables para el fondo y animación
offset_x_pista = 0
nivel_actual = 1


# Coches de pj y rocas (coches a esquivar)

coche_rosa = Coche.Coche("rosa", "images/cocherosaALC.png")
coche_eva = Coche.Coche("eva", "images/cochevioletaALC.png")
coche_verde = Coche.Coche("verde", "images/cocheverdeALC.png")
car = coche_rosa # Inicializar el coche predeterminado
roca = Roca.Roca()
rocas = pygame.sprite.Group()
paused = False


#Música de fondo y sonidos

sonidos = {
    "sonido_choque": pygame.mixer.Sound("sonido/choque.mp3"),
    "sonido_eleccion": pygame.mixer.Sound("sonido/eleccion.mp3"),
    "sonido_car": pygame.mixer.Sound("sonido/car-straring-sound-126708.mp3"),
    "sonido_over": pygame.mixer.Sound("sonido/gameover.mp3")
}

musica = {
    "menu": "sonido/menu.mp3",
    "nivel1": "sonido/nivelbien.mp3",
    "nivel2": "sonido/nivel2.mp3",
    "nivel3": "sonido/musica_de_brusi.mp3"
}

musica_actual = None
# Cambiar música
def cambiar_musica(nombre, loop=-1):
    global musica_actual, nivel_actual
    if musica_actual != (musica[nombre]):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(musica[nombre])
        pygame.mixer.music.play(loop)
        musica_actual = (musica[nombre])
        print(f"Cambia a: {musica[nombre]}")
        print(f"Nivel Actual: {nivel_actual}, Música Actual: {musica_actual}")


pygame.display.set_caption("A LAS CHAPAS")

BG = pygame.image.load("images/BG.png")

def get_font(size):
    return pygame.font.Font("images/font.ttf", size)


def pantalla_seleccion_personaje():
    global areas_coches, screen, seleccion, ejecutando, car
    
    # Crear los rectángulos con las dimensiones máximas
    areas_coches = [
            (coche_rosa, pygame.Rect(30, 180, 240, 140)),
            (coche_eva, pygame.Rect(280, 245, 240, 140)),
            (coche_verde, pygame.Rect(530, 310, 240, 140))]

    seleccion = None
    ejecutando = True

#Bucle infinito fondo

def dibujar_fondo(screen, imgSpace, offset_x_pista, ancho_pista):
    x_relativa = offset_x_pista % ancho_pista
    screen.blit(imgSpace, (x_relativa, 0))
    screen.blit(imgSpace, (x_relativa - ancho_pista, 0))


def options():
    while True:
        global car, coche_rosa, coche_eva, coche_verde, areas_coches, screen, seleccion, ejecutando
        pantalla_seleccion_personaje()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("yellow2")


        for coche, area in areas_coches:
            # Dibuja el rectangulo en el area del coche
            pygame.draw.rect(screen, (30, 136, 229), area, 5)  # Rectangulo con grosor 5
            # Dibuja la imagen del coche en el centro del rectangulo
            #screen.blit(coche.current_image, (area.x, area.y))
            screen.blit(coche.current_image, (area.x + (area.width - coche.image.get_width()) // 2,
                                      area.y + (area.height - coche.image.get_height()) // 2))
            
            if area.collidepoint(OPTIONS_MOUSE_POS):  # Si mouse sobre el coche
                    coche.set_hovered_state(True)  # Cambia a la imagen hover
            else:
                    coche.set_hovered_state(False)  # Vuelve a la imagen normal
        
        OPTIONS_TEXT = get_font(55).render("ELEGI AUTO", True, "purple")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 75))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        linea = get_font(16).render("Velocidad +25   Velocidad +10   Velocidad +50", True, "firebrick1")
        linea_rect = linea.get_rect(center=(SCREEN_WIDTH // 2 - 1, SCREEN_HEIGHT // 2 + 169))
        screen.blit(linea, linea_rect)
        linea1 = get_font(16).render("Impactos +3     Impactos +5     Impactos +2", True, "firebrick1")
        linea1_rect = linea1.get_rect(center=(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 + 189))
        screen.blit(linea1, linea1_rect)

        OPTIONS_BACK = Boton(image=None, pos=(400, 560), 
                            text_input="VOLVER AL MENU PRINCIPAL", font=get_font(15), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for coche, area in areas_coches:
                    if area.collidepoint(event.pos):
                        sonidos["sonido_car"].play()
                        car = coche  # Asignar coche seleccionado a 'car'
                        ejecutando = False  # Salir de la seleccion
                        game()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
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

def reiniciar_estado():
    global nivel_actual, offset_x_pista, roca_timer, roca_col_cont, rocas, imgSpace, imgSpace2, imgSpace3, nivel_actual, adjusted_score, roca_interval
    offset_x_pista = 0 
    roca_timer = pygame.time.get_ticks()
    roca_col_cont = 0
    roca_interval = 1000
    rocas.empty() 
    nivel_actual = 1
    adjusted_score = 0
    imgSpace = pygame.image.load("images/pista12diaALC.png").convert()
    imgSpace2 = pygame.image.load("images/pista12tardeALC.png").convert()
    imgSpace3 = pygame.image.load("images/pista12nocheALC.png").convert()



def game():
    global musica_actual,nivel_actual, imgSpace, imgSpace2, imgSpace3, screen, clock, game_on, isFullscreen, offset_x_pista, roca_timer, roca_collision, roca_col_cont, elapsed_time, adjusted_score, roca_interval
    reiniciar_estado()
    pygame.mixer.music.stop()
    sonidos["sonido_car"].play()

    # Registrar el tiempo de inicio
    start_time = pygame.time.get_ticks()
    
    # Pausa inicial
    start_time_pausa = pygame.time.get_ticks()
    pausa_duracion = 4000  # milisegundoS
    preparando = True

    #Pausa
    paused = False
    
    while preparando:
        current_time = pygame.time.get_ticks()
        if current_time - start_time_pausa >= pausa_duracion:
            preparando = False
        else:
            # Mostrar mensaje durante la pausa
            screen.blit(imgSpace,(0,0))
            texto = get_font(30).render("¡PREPARATE QUE ARRANCAMOS!", True, ("purple"))
            screen.blit(texto, (screen.get_width() // 2 - texto.get_width() // 2,
                                screen.get_height() // 2 - texto.get_height() // 2 + 100))
            pygame.display.flip()
            clock.tick(FPS)
            

    # Reiniciar el tiempo para el juego principal
    start_time = pygame.time.get_ticks()
    paused_time = 0  # Tiempo al pausar
    cambiar_musica("nivel1")
    
    
    
    roca_timer = pygame.time.get_ticks()
    roca_interval = 1000
    roca_collision = False
    roca_col_cont = 0
    rocas.empty()  # Limpiar grupo de rocas

    game_on = True
    while game_on:
        offset_x_pista -= car.background_speed
        dibujar_fondo(screen, imgSpace, offset_x_pista, ancho_pista)
        puntos_para_nivel_2 = 4#30
        puntos_para_nivel_3 = 8#70
        nivel_actual = 1

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
                elif event.key == pygame.K_p:  # Si se presiona la tecla "p"
                        paused = not paused  # Cambia el estado de pausa
                        if paused:
                            paused_time = pygame.time.get_ticks()  # Guarda el momento de pausa
                        else:
                            # Ajusta el tiempo inicial para compensar el tiempo pausado
                            start_time += pygame.time.get_ticks() - paused_time
                elif event.key == pygame.K_f:
                    isFullscreen = not isFullscreen
                    screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN) if isFullscreen else pygame.display.set_mode(RESOLUTION)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_DOWN, pygame.K_UP]:
                    car.move_y = 0


        #Configurando pausa
        if not paused:
            # Calcular el tiempo transcurrido con ajuste por velocidad de cada coche
            elapsed_time = (pygame.time.get_ticks() - start_time) * car.speed_boost // 1000
            adjusted_score = round(elapsed_time / car.speed_boost)
        else:
            # Al pausar recalcula start_time para detener el contador bien
            start_time += pygame.time.get_ticks() - paused_time
            paused_time = pygame.time.get_ticks()

        if paused:
            screen.blit(imgSpace, (0, 0))
            textopausa = get_font(60).render("EN PAUSA", True, ("purple"))
            screen.blit(textopausa, (screen.get_width() // 2 - textopausa.get_width() // 2,
                                screen.get_height() // 2 - textopausa.get_height() // 2 + 100))
            pygame.display.flip()
            clock.tick(FPS)  # Mantén el bucle pausado con los FPS activos
            continue  # Salta el resto de la lógica del juego


        collided_rocas = pygame.sprite.spritecollide(car, rocas, False)
        for roca in collided_rocas:
            if pygame.sprite.collide_mask(car, roca):
                if not roca.collided:  # Solo cuenta si la roca no ha colisionado antes
                    roca.change_image_on_collision()
                    roca_col_cont += 1  # Incrementa el contador una sola vez por roca
                    sonidos["sonido_choque"].play()
    
                if roca_col_cont >= car.max_collisions:  # Comparar con el limite del coche
                    game_over_screen()
                    return
            
        if adjusted_score >= 20:
            roca_interval = 860
        if adjusted_score >= 40:
            roca_interval = 820
        if adjusted_score >= 65:
            roca_interval = 780 
        if adjusted_score >= 85:
            roca_interval = 750
        if adjusted_score >= 99:
            roca_interval = 720 
        if adjusted_score >= 120:
            roca_interval = 700 
        if adjusted_score >= 145:
            roca_interval = 670 
            
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

        font = pygame.font.SysFont('Comic Sans MS', 36)
        time_text = font.render(f"{round(adjusted_score)} Km", True, (230, 51, 255))
        screen.blit(time_text, (10, 10))

        # Cambiar el fondo basado en los puntos
        if adjusted_score >= puntos_para_nivel_2 and adjusted_score <= puntos_para_nivel_3 and nivel_actual == 1:
            imgSpace = imgSpace2
            nivel_actual = 2
            if nivel_actual == 2:  # Solo cambiar si no es la música actual
                cambiar_musica("nivel2")

        if adjusted_score >= puntos_para_nivel_3 and nivel_actual == 2:
            imgSpace2 = imgSpace3
            nivel_actual = 3
            texto = get_font(45).render("¡ULTIMO NIVEL!", True, ("purple"))
            screen.blit(texto, (screen.get_width() // 2 - texto.get_width() // 2,
                                screen.get_height() // 2 - texto.get_height() // 2 + 100))
            if nivel_actual == 3:  # Solo cambiar si no es la música actual
                cambiar_musica("nivel3")


            


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def play():
    game()  # Llama a la función del juego directamente para iniciar la partida
    

def game_over_screen():
    global elapsed_time, adjusted_score
    pygame.mixer.music.stop()
    #Fondo negro de Game Over
    screen.fill((0, 0, 0)) 
    sonidos["sonido_over"].play()

    font = pygame.font.SysFont('Comic Sans MS', 56)
    color = (51, 178, 255)

    # Primera
    line1 = font.render("ALPISTE PERDISTE", True, color)
    line1_rect = line1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
    screen.blit(line1, line1_rect)

    # Segunda
    line2 = font.render((f"¡¡Lograste recorrer {round(adjusted_score)} Km!!"), True, color)
    line2_rect = line2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(line2, line2_rect)
    
    # Tercera
    if adjusted_score <= 10:
        line3 = font.render("Tranki, vamos de vuelta", True, color)
        line3_rect = line3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
        screen.blit(line3, line3_rect)
    
    
    if adjusted_score >= 11 and adjusted_score <= 49:
        line3 = font.render("Falta practica che...", True, color)
        line3_rect = line3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
        screen.blit(line3, line3_rect)
    
    if adjusted_score >= 50:
        line3 = font.render("Estas para el torneo compi", True, color)
        line3_rect = line3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
        screen.blit(line3, line3_rect)


    pygame.display.flip()
    time.sleep(5)  # Pausa antes de volver al menu
    main_menu()

main_menu()
