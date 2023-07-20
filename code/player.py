# IMPORTS
import pygame
from settings import *
from helper import *
from timekeeper import Timer

# CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop):
        super().__init__(groups)

        # Graphics import / set-up
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # General setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z_index = LAYERS['main']
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]] 

        # Movement setup / attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Collisions
        self.hitbox = self.rect.copy().inflate((-126,-70))      
        self.collision_sprites = collision_sprites

        # Interactions
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop

        # Timers
        self.timers = {
            'tool_use': Timer(350, self.use_tool),
            'tool_switch': Timer(200),
            'seed_use': Timer(350, self.use_seed),
            'seed_switch': Timer(200)
        }

        # Inventories
        self.inventory = {
            'wood':   0,
            'apple':  0,
            'corn':   0,
            'tomato': 0
        }
        self.seed_inventory = {
            'corn':   5,
            'tomato': 5
        }
        self.money = 200

        # Tools
        self.tools = ['axe', 'hoe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

    def import_assets(self):
        self.animations = {'right': [],'left': [],'up': [],'down': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}
        
        for animation in self.animations.keys():
            import_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(import_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        # Movement and tool use only allowed if tool is not already in use and awake
        if not self.timers['tool_use'].active and not self.sleep:
            
            # Movement
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # Use a tool (& stop the player from moving, reset frame index to start new animation)
            if keys[pygame.K_SPACE]:
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
            
            # Change tool
            if keys[pygame.K_TAB] and not self.timers['tool_switch'].active:
                self.timers['tool_switch'].activate()
                self.tool_index += 1
                if self.tool_index >= len(self.tools):
                    self.tool_index = 0
                self.selected_tool = self.tools[self.tool_index]

            # Plant a seed  (& stop the player from moving, reset frame index to start new animation)
            if keys[pygame.K_f]:
                self.timers['seed_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # Change seeds
            if keys[pygame.K_LSHIFT] and not self.timers['seed_switch'].active:
                self.timers['seed_switch'].activate()
                self.seed_index += 1
                if self.seed_index >= len(self.seeds):
                    self.seed_index = 0
                self.selected_seed = self.seeds[self.seed_index]

            # Interations with Trader or bed
            if keys[pygame.K_RETURN]:
                collided_interation_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interation_sprite:
                    if collided_interation_sprite[0].name == 'Trader':
                        self.toggle_shop()
                    else:
                        # Interacting with bed, so sleep
                        self.status = 'left_idle'
                        self.sleep = True

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
        
    def get_status(self):
        # Manages idle animations
        if self.direction.magnitude() == 0:
            # Avoids *_idle_idle by splitting the string if one already exists.
            self.status = self.status.split('_')[0] + '_idle'
        
        # Tool use
        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: # i.e. if the player is moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # i.e. if the player is moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == 'vertical':
                        if self.direction.y > 0: # i.e. if the player is moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: # i.e. if the player is moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        # Normalise the vector (in case of two simultaneous key presses for direction)
        if self.direction.magnitude():
            self.direction = self.direction.normalize()
        
        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        # Vertical Movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')
    
    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
        # Checks what direction the player is facing by using self.status, and applies the tool offset 
        # which have the same names so this works!
    
    def use_tool(self):
        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
                   
        if self.selected_tool == 'hoe':
            self.soil_layer.get_dig_hit(self.target_pos)
    
        if self.selected_tool == 'water':
            self.soil_layer.water_single_tile(self.target_pos)

    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:
            self.soil_layer.plant_crop(self.target_pos, self.selected_seed)
            self.seed_inventory[self.selected_seed] -= 1

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)
