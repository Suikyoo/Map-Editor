import os, pygame, map_functs, core_functs
pygame.init()
pygame.display.set_mode((50, 50))

def make_dir(string):
    try: os.mkdir(string)
    except FileExistsError: pass

def get_files(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            yield file_path
        else:
            for i in get_files(file_path):
                yield i

cut_dimensions = [13, 13]
load_dir = "../assets/tiles/tilesets"
save_dir = "../cut_tiles"
make_dir(save_dir)

files = [i for i in get_files(load_dir) if os.path.basename(i) != "custom_tileset"]
for file_path in get_files(load_dir):
    folder_name = os.path.splitext(os.path.basename(file_path))[0]
    make_dir(os.path.join(save_dir, folder_name))
    tiles = map_functs.cut_set(pygame.image.load(file_path).convert(), cut_dimensions)
    for i in range(len(tiles)):
        if tiles[i] != None:
            pygame.image.save(tiles[i], os.path.join(save_dir, folder_name, str(i) + ".png"))

