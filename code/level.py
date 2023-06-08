# IMPORTS
import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import GenericSprite, WaterSprite, WildflowerSprite, TreeSprite
from pytmx.util_pygame import load_pygame
from helper import *

class Level:
    def __init__(self):
        
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprites
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        # TILE IMPORTS
        tmx_data = load_pygame('../data/map.tmx')

        # House (refactor me?)
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                GenericSprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house_bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                GenericSprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['main'])

        # Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            GenericSprite((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['main'])

        # Water
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            WaterSprite((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            TreeSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], obj.name)

        # Wildflowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildflowerSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # Map collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            GenericSprite((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
            # by only including it in the collision_sprites group, it means the tiles are not rendered / updated
            # which is fine because they're static on the map!
        
        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x, obj.y), 
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites,
                    tree_sprites = self.tree_sprites)  
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
            # sorted makes the player appear behind objects by using their y coordinates to as a render order
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z_index == layer:
                    offset_rect = sprite.rect.copy() 
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # Some visualisation for trouble-shooting - hide me when done!
                    # if sprite == player:
                    #     # Player rect
                    #     pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                    #     # Collision hitbox
                    #     hitbox_rect = player.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
                    #     # Tool target position
                    #     target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                    #     pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)