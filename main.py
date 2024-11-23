import pygame
import random
from player import Player
from enemy import Enemy
from bullet import Bullet
from interfaz import Interfaz
pygame.init()
pygame.mixer.init()


sonido_inicio = pygame.mixer.Sound("Recursos/inicio.mp3")
onido_disparo = pygame.mixer.Sound("Recursos/disparo.mp3")

sonido_inicio.play()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo
        if tipo == "vida_extra":
            self.image = pygame.image.load("Recursos/vida_extra.png").convert_alpha()
        elif tipo == "puntos_dobles":
            self.image = pygame.image.load("Recursos/puntos_dobles.png").convert_alpha()
        elif tipo == "inmunidad":
            self.image = pygame.image.load("Recursos/inmunidad.png").convert_alpha()
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 0))  
        self.image = pygame.transform.scale(self.image, (20, 20)) 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 2  

    def update(self):
        self.rect.y += self.velocidad  
        if self.rect.top > 600:  
            self.kill() 

pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

todos_los_sprites = pygame.sprite.Group()
balas_jugador = pygame.sprite.Group()
balas_enemigos = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
powerups = pygame.sprite.Group()
inmunidad_activa = False
tiempo_inmunidad = 0 

interfaz = Interfaz()
vidas_iniciales = 3
nivel_inicial = 1
puntaje = 0

jugador = Player(400, 500, balas_jugador, todos_los_sprites)
todos_los_sprites.add(jugador)

def generar_power_up(x, y):
    tipos = ["vida_extra", "puntos_dobles", "inmunidad"]
    tipo = random.choice(tipos + ["nada"]) 
    if tipo != "nada":
        power_up = PowerUp(tipo, x, y)
        todos_los_sprites.add(power_up)
        powerups.add(power_up)
        return power_up
    return None 

def crear_enemigos(nivel):
    enemigos.empty()
    balas_enemigos.empty()  

    filas = 3
    columnas = 5 + nivel
    velocidad_bajada = 10 + nivel * 5
    disparo_frecuencia = max(20, 80 - nivel * 15)

    for fila in range(filas):
        for columna in range(columnas):
            x = 100 + columna * 100
            y = 50 + fila * 60
            if fila % 2 == 0:
                x += 20 * (columna % 2)
            enemigo = Enemy(x, y, balas_enemigos, todos_los_sprites, velocidad_bajada, disparo_frecuencia)
            enemigos.add(enemigo)
            todos_los_sprites.add(enemigo)

def seleccionar_nivel():
    font = pygame.font.Font(None, 50)
    niveles = ["NIVEL 1", "NIVEL 2", "NIVEL 3"]
    seleccion = 0
    while True:
        ventana.fill((0, 0, 0))
        texto = font.render("Selecciona el Nivel", True, (255, 255, 255))
        ventana.blit(texto, (250, 150))

        for i, nivel_texto in enumerate(niveles):
            color = (255, 255, 255) if i == seleccion else (100, 100, 100)
            texto_nivel = font.render(nivel_texto, True, color)
            ventana.blit(texto_nivel, (300, 250 + i * 60))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(niveles)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(niveles)
                elif evento.key == pygame.K_RETURN:
                    return seleccion + 1

def menu_principal():
    font = pygame.font.Font(None, 50)
    logo = pygame.image.load("Recursos/logo.png").convert_alpha()
    logo = pygame.transform.scale(logo, (200, 100))
    opciones = ["INICIO", "NIVELES", "SALIR"]
    seleccion = 0
    while True:
        ventana.fill((0, 0, 0))
        ventana.blit(logo, (300, 50))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (100, 100, 100)
            texto = font.render(opcion, True, color)
            ventana.blit(texto, (350, 200 + i * 60))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "INICIO":
                        return 1
                    elif opciones[seleccion] == "NIVELES":
                        return seleccionar_nivel()
                    elif opciones[seleccion] == "SALIR":
                        pygame.quit()
                        exit()

def menu_derrota():
    font = pygame.font.Font(None, 50)
    opciones = ["REINICIAR", "SALIR"]
    seleccion = 0
    while True:
        ventana.fill((0, 0, 0))
        texto = font.render("YOU LOSE", True, (255, 0, 0))
        ventana.blit(texto, (300, 200))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (100, 100, 100)
            texto_opcion = font.render(opcion, True, color)
            ventana.blit(texto_opcion, (350, 300 + i * 60))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "REINICIAR":
                        return "reiniciar"
                    elif opciones[seleccion] == "SALIR":
                        pygame.quit()
                        exit()

def menu_victoria(puntaje):
    font = pygame.font.Font(None, 50)
    opciones = ["REINICIAR", "SALIR"]
    seleccion = 0
    while True:
        ventana.fill((0, 0, 0))
        texto = font.render("¡FELICIDADES, GANASTE!", True, (0, 255, 0))
        puntaje_texto = font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        ventana.blit(texto, (150, 150))
        ventana.blit(puntaje_texto, (300, 250))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (100, 100, 100)
            texto_opcion = font.render(opcion, True, color)
            ventana.blit(texto_opcion, (350, 350 + i * 60))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "REINICIAR":
                        return "reiniciar"
                    elif opciones[seleccion] == "SALIR":
                        pygame.quit()
                        exit()

def temporizador_inicial():
    font = pygame.font.Font(None, 100)
    for cuenta_regresiva in range(3, 0, -1):
        ventana.fill((0, 0, 0))
        texto = font.render(str(cuenta_regresiva), True, (255, 255, 255))
        ventana.blit(texto, (400, 300))
        pygame.display.flip()
        pygame.time.delay(1000)

def generar_power_up(x, y):
    tipos = ["vida_extra", "puntos_dobles", "inmunidad"]
    tipo = random.choice(tipos + ["nada"]) 
    if tipo != "nada":
        power_up = PowerUp(tipo, x, y)
        todos_los_sprites.add(power_up)
        powerups.add(power_up)
        return power_up
    return None 
        
def mostrar_nivel(nivel):
    font = pygame.font.Font(None, 80)
    texto = font.render(f"NIVEL {nivel}", True, (255, 255, 255))
    ventana.fill((0, 0, 0))
    ventana.blit(texto, (350, 150))
    pygame.display.flip()
    pygame.time.delay(2000) 
    
def iniciar_juego(nivel):
    global vidas, puntaje,vidas_iniciales,inmunidad_activa,tiempo_inmunidad
    vidas = vidas_iniciales
    puntaje = 0
    crear_enemigos(nivel)

    temporizador_inicial() 

    juego_activo = True
    while juego_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jugador.disparar()

        todos_los_sprites.update()
        if inmunidad_activa:
            tiempo_inmunidad -= 1 
            if tiempo_inmunidad <= 0:
                inmunidad_activa = False 

        colision_balas = pygame.sprite.groupcollide(balas_jugador, enemigos, True, True)
        for colision in colision_balas:
            puntaje += 100
            if random.random() < 0.2:
                generar_power_up(colision.rect.x, colision.rect.y)

        colision_jugador_enemigos = pygame.sprite.spritecollide(jugador, enemigos, True)
        if colision_jugador_enemigos:
            vidas -= 1
            if vidas <= 0:
                return menu_derrota()

        colision_balas_enemigos = pygame.sprite.spritecollide(jugador, balas_enemigos, True)
        if colision_balas_enemigos:
            vidas -= 1
            if vidas <= 0:
                return menu_derrota()
       

        if len(enemigos) == 0:
            if nivel == 3:
                return menu_victoria(puntaje)
            else:
                nivel += 1
                mostrar_nivel(nivel)  
                crear_enemigos(nivel)
                pygame.time.delay(1000)  

        power_ups_colisionados = pygame.sprite.spritecollide(jugador, powerups, True)
        for power_up in power_ups_colisionados:
            if isinstance(power_up, PowerUp):
                if power_up.tipo == "vida_extra":
                        vidas += 1
                elif power_up.tipo == "puntos_dobles":
                        puntaje += 200
                elif power_up.tipo == "inmunidad":
                    inmunidad_activa = True  
                    tiempo_inmunidad = 300 
                       

            if vidas_iniciales <= 0:
                if menu_derrota() == "reiniciar":
                    vidas_iniciales = 3
                    nivel_actual = 1
                    puntaje = 0
                    crear_enemigos(nivel_actual)
                    temporizador_inicial(ventana, 3)
                break
        ventana.fill((0, 0, 0))
        todos_los_sprites.draw(ventana)
        interfaz.mostrar(ventana, puntaje, vidas, nivel)
        pygame.display.flip()
        clock.tick(60)

while True:
    nivel = menu_principal()
    iniciar_juego(nivel)
