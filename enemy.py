
import pygame
import random
from powerups import PowerUp
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, balas_enemigos, todos_los_sprites, velocidad_bajada=20, disparo_frecuencia=60):
        super().__init__()
        self.image = pygame.image.load("Recursos/enemy.png").convert_alpha() 
        self.image = pygame.transform.scale(self.image, (40, 40))  
        self.rect = self.image.get_rect(topleft=(x, y))
        self.balas_enemigos = balas_enemigos
        self.todos_los_sprites = todos_los_sprites
        self.velocidad_x = 3
        self.velocidad_bajada = velocidad_bajada
        self.disparo_frecuencia = disparo_frecuencia
        self.tiempo_disparo = 0

    def update(self):
       
        self.rect.x += self.velocidad_x
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.velocidad_x = -self.velocidad_x
            self.rect.y += self.velocidad_bajada

        
        self.tiempo_disparo += 1
        if self.tiempo_disparo >= self.disparo_frecuencia:
            self.disparar()
            self.tiempo_disparo = 0

    def disparar(self):
        bala = Bullet(self.rect.centerx, self.rect.bottom, "enemigo")
        self.balas_enemigos.add(bala)
        self.todos_los_sprites.add(bala)

    def eliminar(self):
        
        if random.random() < 0.3:  
            tipo_power_up = random.choice(["vida_extra", "puntos_dobles", "inmunidad"])
            power_up = PowerUp(self.rect.centerx, self.rect.bottom, tipo_power_up)
            self.todos_los_sprites.add(power_up)
