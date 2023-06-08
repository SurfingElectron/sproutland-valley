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

# APPLE POSITION DICTIONARIES
APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}