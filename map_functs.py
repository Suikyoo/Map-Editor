import pygame, core_functs
#splits an image and returns a list of surf
#Use slash(/) when specifying file path
def cut_tile(file_path, dimension, colorkey=(0, 0, 0)):
    surf = pygame.image.load(file_path).convert()
    surf_size = surf.get_size()
    tileset = []
    for y in range(surf_size[1]//dimension[1]):
        for x in range(surf_size[0]//dimension[0]):
            tile_surf = core_functs.cut(surf, dimension[0] * x, dimension[1] * y, dimension[0], dimension[1])   
            tile_surf.set_colorkey(colorkey)
            tileset.append(tile_surf.copy())

    return tileset
