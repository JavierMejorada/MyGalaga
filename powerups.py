import random
import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, tipo, x, y):
        super().__init__()
        self.tipo = tipo
        self.image = pygame.Surface((20, 20)) 
        self.image.fill((255, 255, 0)) 
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 1  
    def draw(self, surface):
        surface.blit(self.image, self.rect)
