import pygame
from settings import *

class SoilLayer:
    def __init__(self, all_sprites):
        
        # Sprite Groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # Graphics
        self.soil_surf = pygame.image.load('../graphics/soil/o.png')