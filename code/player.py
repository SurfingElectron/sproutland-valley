# IMPORTS
import pygame
from settings import *
from helper import *
from timekeeper import Timer

# CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Graphics import / set-up
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # General setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # Movement setup / attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Timers
        self.timers = {
            'tool_use': Timer(350, self.use_tool)
        }

        # Tools
        self.selected_tool = 'axe'

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

        # Movement and tool use only allowed if tool is not already in use
        if not self.timers['tool_use'].active:
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

            # Tool use (& stop the player from moving, reset frame index to start new animation)
            if keys[pygame.K_SPACE]:
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

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

    def move(self, dt):
        # Normalise the vector (in case of two key presses for direction)
        if self.direction.magnitude():
            self.direction = self.direction.normalize()
        
        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        # Vertical Movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
    
    def use_tool(self):
        print(self.selected_tool)

    def update(self, dt):
        self.input()
        self.update_timers()
        self.get_status()
        self.move(dt)
        self.animate(dt)
