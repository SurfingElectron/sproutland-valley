# IMPORTS
import pygame
from settings import *
from random import randint

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
        # TreeSprite currently inherits the GenericSprite hitbox
        # - pretty big, do I want to change that?

        # Apples!
        self.apple_surf = pygame.image.load('../graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_apple()

    def create_apple(self):
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                GenericSprite(
                    pos = (x,y), 
                    surf = self.apple_surf, 
                    groups = [self.apple_sprites, self.groups()[0]],
                    z_index = LAYERS['fruit'])
                # using self.groups[0] places it in the all_sprites group which isn't otherwise
                # available here 

class WildflowerSprite(GenericSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)