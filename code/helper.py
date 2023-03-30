# IMPORTS
import pygame
from os import listdir

# General helper functions
def import_folder(import_path):
    surface_list = []

    for image in listdir(import_path):
        full_path = import_path + '/' + image
        image_surf = pygame.image.load(full_path).convert_alpha()
        surface_list.append(image_surf)

    return surface_list