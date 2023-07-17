import pygame
from random import choice, randint
from settings import *
from helper import import_folder
from sprites import GenericSprite

class Raindrop(GenericSprite):
    def __init__(self, surf, pos, is_moving, groups, z_index):

        # Setup
        super().__init__(pos, surf, groups, z_index)
        self.lifespan =  randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # Movement
        self.is_moving = is_moving
        if self.is_moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)

    def update(self, dt):
        # Update movement
        if self.is_moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        # Destroy if lifespan is over
        if pygame.time.get_ticks() - self.start_time >= self.lifespan:
            self.kill()

class Rain:
    def __init__(self, all_sprites):
        
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('../graphics/rain/drops')
        self.rain_splats = import_folder('../graphics/rain/floor')
        self.map_width, self.map_height = pygame.image.load('../graphics/world/ground.png').get_size()
    
    def create_drops(self):
        Raindrop(
            surf = choice(self.rain_drops), 
            pos = (randint(0, self.map_width), randint(0, self.map_height)),
            is_moving = True, 
            groups = self.all_sprites, 
            z_index = LAYERS['rain_drops']
            )

    def create_splats(self):
        Raindrop(
            surf = choice(self.rain_splats), 
            pos = (randint(0, self.map_width), randint(0, self.map_height)), 
            is_moving = False, 
            groups = self.all_sprites, 
            z_index = LAYERS['rain_ground']
            )

    def update(self):
        self.create_drops()
        self.create_splats()

