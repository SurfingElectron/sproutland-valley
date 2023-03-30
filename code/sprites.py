# IMPORTS
import pygame
from settings import *

class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z_index = LAYERS['main']):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z_index = z_index