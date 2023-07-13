import pygame
from pytmx.util_pygame import load_pygame
from random import choice
from helper import *
from settings import *

# SOIL GRID KEYS
# F: farmable
# T: tilled (has been dug by hoe)
# W: watered

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z_index = LAYERS['soil'] 

class WateredTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z_index = LAYERS['soil_water']

class SoilLayer:
    def __init__(self, all_sprites):
        
        # Sprite Groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.watered_sprites = pygame.sprite.Group()

        # Graphics
        self.soil_surfs = import_folder_dict('../graphics/soil/')
        self.watered_surfs = import_folder('../graphics/soil_water/')

        self.create_soil_grid()
        self.create_dig_rects()
    
    def create_soil_grid(self):
        ground = pygame.image.load('../graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        
        # Load the Tiled data, mark farmable tiles with an F
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_dig_rects(self):
        self.dig_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.dig_rects.append(rect)

    def get_dig_hit(self, target_pos):
        for rect in self.dig_rects:
            if rect.collidepoint(target_pos):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('T')
                    self.create_soil_tiles()

    def water_soil(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                # Update the soil grid to mark tile as watered
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')

                # Show the tile as watered
                WateredTile(
                    pos = soil_sprite.rect.topleft,
                    surf = choice(self.watered_surfs),
                    groups = [self.all_sprites, self.watered_sprites]
                )

    def dry_soil(self):
        # Destroy all the watered sprites
        for sprite in self.watered_sprites.sprites():
            sprite.kill()
        
        # Update the soil grid so nothing is marked as watered
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def create_soil_tiles(self):
        # Gets rid of all soil tiles and redraws them
        # So that the tilled soil looks like a continuous patch and not individual tiles
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'T' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    tile_type = 'o'

                    # Establish the status of the tile's neighbours (top, bottom, left, right)
                    t_nb = 'T' in self.grid[index_row - 1][index_col]
                    b_nb = 'T' in self.grid[index_row + 1][index_col]
                    r_nb = 'T' in row[index_col + 1]
                    l_nb = 'T' in row[index_col - 1]

                    # Logic for determining which tile graphic to use
                    # All neighbours are tilled soil
                    if all((t_nb, r_nb, b_nb, l_nb)): tile_type = 'x'

                    # Only horizontal neighbours are tilled soil
                    if r_nb and not any((t_nb, b_nb, l_nb)): tile_type = 'l'
                    if l_nb and not any((t_nb, r_nb, b_nb)): tile_type = 'r'
                    if r_nb and l_nb and not any((t_nb, b_nb)): tile_type = 'lr'

                    # Only vertical neighbours are tilled soil
                    if t_nb and not any((r_nb, b_nb, l_nb)): tile_type = 'b'
                    if b_nb and not any((t_nb, r_nb, l_nb)): tile_type = 't'
                    if t_nb and b_nb and not any((r_nb, l_nb)): tile_type = 'tb'

                    # Neighbours form a corner of tilled soil
                    if t_nb and r_nb and not any((b_nb, l_nb)): tile_type = 'bl'
                    if t_nb and l_nb and not any((r_nb, b_nb)): tile_type = 'br'
                    if b_nb and r_nb and not any((t_nb, l_nb)): tile_type = 'tl'
                    if b_nb and l_nb and not any((t_nb, r_nb)): tile_type = 'tr'

                    # Neighbours create t-shapes of tilled soil
                    if all((t_nb, r_nb, b_nb)) and not l_nb: tile_type = 'tbr'                  
                    if all((t_nb, b_nb, l_nb)) and not r_nb: tile_type = 'tbl'
                    if all((t_nb, r_nb, l_nb)) and not b_nb: tile_type = 'lrb'
                    if all((r_nb, b_nb, l_nb)) and not t_nb: tile_type = 'lrt'

                    SoilTile(
                        pos = (x, y), 
                        surf = self.soil_surfs[tile_type], 
                        groups = [self.all_sprites, self.soil_sprites])
