# IMPORTS
import pygame
from settings import *

class GenericSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z_index = LAYERS['main']):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z_index = z_index
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class WaterSprite(GenericSprite):
    def __init__(self, pos, frames, groups):

        # Animation Setup
        self.frames = frames
        self.frame_index = 0

        super().__init__(
            pos = pos, 
            surf = self.frames[self.frame_index], 
            groups = groups, 
            z_index = LAYERS['water'])
    
    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update (self, dt):
        self.animate(dt)

class TreeSprite(GenericSprite):
    def __init__(self, pos, surf, groups, name):
        super().__init__(pos, surf, groups)
        # TreeSprite inherits the GenericSprite hitbox

class WildflowerSprite(GenericSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)