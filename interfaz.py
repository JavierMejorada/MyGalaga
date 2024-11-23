# interfaz.py
import pygame

class Interfaz:
    def __init__(self):
        self.font = pygame.font.Font(None, 30)  

    def mostrar(self, ventana, puntaje, vidas, nivel):
        puntaje_texto = self.font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        vidas_texto = self.font.render(f"Vidas: {vidas}", True, (255, 0, 0))
        nivel_texto = self.font.render(f"Nivel: {nivel}", True, (0, 255, 0))

        ventana.blit(puntaje_texto, (10, 10))
        ventana.blit(vidas_texto, (10, 40))
        ventana.blit(nivel_texto, (10, 70))
