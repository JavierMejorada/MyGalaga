import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0) if tipo == "jugador" else (255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.tipo = tipo

    def update(self):
        if self.tipo == "jugador":
            self.rect.y -= 10  
        else:
            self.rect.y += 5 
        if self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()
