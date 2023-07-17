# IMPORTS
from pygame.math import Vector2

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
	'rain_ground': 4,
	'house_bottom': 5,
	'ground_plant': 6,
	'main': 7,
	'house_top': 8,
	'fruit': 9,
	'rain_drops': 10
}

# APPLE POSITION DICTIONARIES
APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

# PLAYER TOOL OFFSET VECTORS
PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}