import pygame
from pytmx.util_pygame import load_pygame
from settings import *

class SoilLayer:
    def __init__(self, all_sprites):
        
        # Sprite Groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # Graphics
        self.soil_surf = pygame.image.load('../graphics/soil/o.png')

        self.create_soil_grid()
        self.create_dig_rects()
    
    def create_soil_grid(self):
        ground = pygame.image.load('../graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        # Loading the Tiled data, marking farmable tiles with an F
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('farmable').tiles():
            self.grid[y][x].append('F')

    def create_dig_rects(self):
        self.dig_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x_pos = index_col * TILE_SIZE
                    y_pos = index_row * TILE_SIZE
                    rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)
                    self.dig_rects.append(rect)

    def get_dig_hit(self, point):
        for rect in self.dig_rects:
            if rect.collidepoint(point):
                x_pos = rect.x // TILE_SIZE
                y_pos = rect.y // TILE_SIZE