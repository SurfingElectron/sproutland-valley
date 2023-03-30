# IMPORTS
import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import GenericSprite


class Level:
    def __init__(self):
        
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprites
        self.all_sprites = CameraGroup()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        self.player = Player((640,360), self.all_sprites)
        GenericSprite(
            pos = (0,0), 
            surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(), 
            groups = self.all_sprites,
            z_index = LAYERS['ground'])


    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player): 
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values(): 
            for sprite in self.sprites():
                if sprite.z_index == layer:
                    offset_rect = sprite.rect.copy() 
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)