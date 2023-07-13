# IMPORTS
import pygame
from os import listdir

# Import the graphics from a folder 
def import_folder(import_path):
    surface_list = []

    for graphic in listdir(import_path):
        full_path = import_path + '/' + graphic
        graphic_surf = pygame.image.load(full_path).convert_alpha()
        surface_list.append(graphic_surf)

    return surface_list

# Import the graphics from a folder, when we need to know the name of each graphic
def import_folder_dict(import_path):
    surface_dict = {}

    for graphic in listdir(import_path):
        full_path = import_path + '/' + graphic
        graphic_name = graphic.split('.')[0]
        graphic_surf = pygame.image.load(full_path).convert_alpha()
        surface_dict[graphic_name] = graphic_surf
    
    return surface_dict