import pygame, math
import core_functs
#splits an image and returns a list of surf
#Use slash(/) when specifying file path
def cut_set(surf, dimension, colorkey=(0, 0, 0)):
    surf = surf.copy()
    surf_size = surf.get_size()
    tileset = []
    for y in range(math.ceil(surf_size[1]/dimension[1])):
        for x in range(math.ceil(surf_size[0]/dimension[0])):
            tile_surf = core_functs.cut(surf, dimension[0] * x, dimension[1] * y, dimension[0], dimension[1])   
            
            real_tile = False
            for py in range(tile_surf.get_height()):
                for px in range(tile_surf.get_width()):
                    if tile_surf.get_at((px, py)) != colorkey:
                        real_tile = True

            if real_tile:
                tile_surf.set_colorkey(colorkey)
                tile = tile_surf

            else: tile = None

            tileset.append(tile)

    return tileset

#returns a dict that stringifies sequence keys 
#(x, y) --> "x:y"
def jsonify_map(item):
    def stringify_item(item):
        if isinstance(item, (list, tuple)):
            return ":".join(map(str, item))

        if isinstance(item, (int, float)):
            return str(item)

        return item
        
    if isinstance(item, dict):
        return {stringify_item(k) : jsonify_map(v) for k, v in item.items()}

    if isinstance(item, (list, tuple)):
        return [jsonify_map(i) for i in item]

    return item

#opposite of jsonify_map
#"x:y" --> (x, y)
def mapify_json(item):
    def numerify_item(item):
        if isinstance(item, str):
            #if sequence
            if ":" in item:
                return tuple([float(n) if "." in n else int(n) for n in item.split(":")])

            #if number
            if core_functs.is_digit(item):
                if "." in item: return float(item)
                else: return int(item)

        return item
            
    if isinstance(item, dict):
        return {numerify_item(k) : mapify_json(v) for k, v in item.items()}

    if isinstance(item, (list, tuple)):
        return [mapify_json(i) for i in item]

    return item


def tilify(data, chunk_pxl_size):
    new_data = {}
    for spawn_type in data:
        new_data[spawn_type] = {}

        for index in range(len(data[spawn_type])):
            spawn = data[spawn_type][index]

            chunk = tuple([int(spawn["coords"][i] // chunk_pxl_size[i]) for i in range(2)]) 
            coords = tuple(spawn["coords"])

            if chunk not in new_data[spawn_type]:
                new_data[spawn_type][chunk] = {}

            new_data[spawn_type][chunk][coords] = "_".join([spawn_type, spawn["type"]])

    return new_data

def spawnify(data):
    new_data = {}
    for spawn_type in data:
        new_data[spawn_type] = []
        for chunk in data[spawn_type]:
            for loc in data[spawn_type][chunk]:
                obj_type = data[spawn_type][chunk][loc].split("_")[1]
                
                new_data[spawn_type].append({"type" : obj_type, "coords" : loc})

    return new_data

#takes a list of locs and returns 4 points
def get_peak_points(locs):
    min_point = [None, None]
    max_point = [None, None]
    functs = [min, max]

    for loc in locs:
        for n in range(2):
            functs = [min, max]
            index = 0
            for i in [min_point, max_point]:
                if i[n] == None:
                    i[n] = loc[n]

                i[n] = functs[index](loc[n], i[n])  
                index += 1

    return [min_point, max_point]

