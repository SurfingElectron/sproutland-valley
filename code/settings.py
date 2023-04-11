# IMPORTS
import pygame

# SCREEN
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# OVERLAY
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

# DRAW ORDER
LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil_water': 3,
	'rain_floor': 4,
	'house_bottom': 5,
	'ground_plant': 6,
	'main': 7,
	'house_top': 8,
	'fruit': 9,
	'raindrops': 10
}