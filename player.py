import pygame
from bullet import Bullet  
pygame.mixer.init()

# Cargar sonidos

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, balas_jugador, todos_los_sprites):
        super().__init__()
        self.image = pygame.image.load("Recursos/player.png").convert_alpha()  
        self.image = pygame.transform.scale(self.image, (30, 30))  
        self.rect = self.image.get_rect(center=(x, y))
        self.balas_jugador = balas_jugador
        self.todos_los_sprites = todos_los_sprites
        self.velocidad = 5 

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

    def disparar(self):
        bala = Bullet(self.rect.centerx, self.rect.top, "jugador")
        self.balas_jugador.add(bala)
        self.todos_los_sprites.add(bala)
