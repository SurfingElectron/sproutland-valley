# IMPORTS
import pygame
from pytmx.util_pygame import load_pygame
from random import randint
from settings import *
from helper import *
from sprites import *
from player import Player
from overlay import Overlay
from transition import Transition
from soil import SoilLayer
from sky import Nightfall, Rain
from menu import Menu

class Level:
    def __init__(self):
        
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprites
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group() 

        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.advance_day, self.player)

        # Music
        self.bg_music = pygame.mixer.Sound('../audio/music.mp3')
        self.bg_music.set_volume(0.5)

        # Audio
        self.success = pygame.mixer.Sound('../audio/success.wav')
        self.success.set_volume(0.4)

        # Sky & Rain
        self.nightfall = Nightfall()
        self.rain = Rain(self.all_sprites)
        self.is_raining = False
        self.soil_layer.is_raining = self.is_raining

        # Shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.is_shop_active = False


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

        # Fences
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            GenericSprite((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['main'])

        # Water
        water_frames = import_folder('../graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            WaterSprite((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            TreeSprite(
                pos = (obj.x, obj.y), 
                surf = obj.image, 
                groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
                name = obj.name,
                player_inv_add = self.player_add_item)

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
                    tree_sprites = self.tree_sprites,
                    interaction = self.interaction_sprites,
                    soil_layer = self.soil_layer,
                    toggle_shop = self.toggle_shop
                    )  
            if obj.name == 'Bed':
                Interaction(
                    pos = (obj.x, obj.y), 
                    size = (obj.width, obj.height),
                    groups = self.interaction_sprites, #No all_sprites because we don't want this visible!
                    name = obj.name
                    ) 
            if obj.name == 'Trader':
                Interaction(
                    pos = (obj.x, obj.y), 
                    size = (obj.width, obj.height),
                    groups = self.interaction_sprites, #No all_sprites because we don't want this visible!
                    name = obj.name
                    )    
                
        # Ground
        GenericSprite(
            pos = (0,0), 
            surf = pygame.image.load('../graphics/world/ground.png').convert_alpha(), 
            groups = self.all_sprites,
            z_index = LAYERS['ground']
            )
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    def crop_collision(self):
        if self.soil_layer.crop_sprites:
            for crop in self.soil_layer.crop_sprites.sprites():
                if crop.is_harvestable and crop.rect.colliderect(self.player.hitbox):
                    self.player_add_item(crop.crop_type)
                    crop.kill()
                    ParticleEffect(
                        pos = crop.rect.topleft, 
                        surf = crop.image, 
                        groups = self.all_sprites, 
                        z_index = LAYERS['main'],
                    )
                    self.soil_layer.grid[crop.rect.centery // TILE_SIZE][crop.rect.centerx // TILE_SIZE].remove('C')
    
    def player_add_item(self, item):
        self.player.inventory[item] += 1
        self.success.play()

    def toggle_shop(self):
        self.is_shop_active = not self.is_shop_active

    def advance_day(self):
        # Trees grow new apples
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_apple()

        # Crops grow
        self.soil_layer.update_crops()

        # Tilled soil effects
        # Watered soil dries out
        self.soil_layer.dry_soil()

        # Decide if it's raining now
        self.is_raining = randint(0, 10) > 7
        # Making sure is_raining is available in SoilLayer
        self.soil_layer.is_raining = self.is_raining

        # Water all the tilled soil if it is raining
        if self.is_raining:
            self.soil_layer.water_all_tiles()

        # Reset nightfall to start values (so next morning is "bright" again)
        self.nightfall.start_color = [255, 255, 255]      

    def run(self, dt):
        # Play the background music
        self.bg_music.play(loops = -1)

        # Drawing logic
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)

        # Show the HUD
        self.overlay.display()

        # Updates
        if self.is_shop_active:
            self.menu.update()
        else:
        # Don't update sprites and collisions if shop menu is active    
            self.all_sprites.update(dt)
            self.crop_collision()



        # Rain
        if self.is_raining and not self.is_shop_active:
            self.rain.update()

        # Night approaches
        self.nightfall.display(dt)

        # Plays the day transition animation
        if self.player.sleep:
            self.transition.play()

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