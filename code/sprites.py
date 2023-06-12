# IMPORTS
import pygame
from settings import *
from timekeeper import Timer
from random import randint, choice

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

        # Tree Attributes
        self.health = 5
        self.alive = True
        tree_stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.tree_stump_surf = pygame.image.load(tree_stump_path).convert_alpha()
        self.invul_timer = Timer(200)

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
   
    def damage(self):
        # Damaging the tree
        self.health -= 1

        # Removing an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()
    
    def is_dead(self):
        if self.health <= 0:
            self.image = self.tree_stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False

    def update(self, dt):
        if self.alive:
            self.is_dead()


class WildflowerSprite(GenericSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)