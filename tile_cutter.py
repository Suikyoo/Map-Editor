import os, pygame, 
from scripts import map_functs
pygame.init()
pygame.display.set_mode((50, 50))

def make_dir(string):
    try: os.mkdir(string)
    except FileExistsError: pass

cut_dimensions = [13, 13]
load_dir = "../assets/tilesets"
save_dir = "../cut_tileset"
make_dir(save_dir)

for file in os.listdir(load_dir):
    if os.path.isfile(os.path.join(load_dir, file)):
        file_name = os.path.splitext(file)[0]
        make_dir(os.path.join(save_dir, file_name))
        tiles = map_functs.cut_set(pygame.image.load(os.path.join(load_dir, file)).convert(), cut_dimensions)
        for i in range(len(tiles)):
            if tiles[i] != None:
                pygame.image.save(tiles[i], os.path.join(save_dir, file_name, str(i) + ".png"))

