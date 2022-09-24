import pygame, core_functs
#splits an image and returns a list of surf
#Use slash(/) when specifying file path
def cut_set(surf, dimension, colorkey=(0, 0, 0)):
    surf = surf.copy()
    surf_size = surf.get_size()
    tileset = []
    for y in range(surf_size[1]//dimension[1]):
        for x in range(surf_size[0]//dimension[0]):
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
                return tuple([int(i) for i in item.split(":")])

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

def prune_dict(item, blank_val={}):
    if isinstance(item, dict):
        for k in item.copy():
            v = prune_dict(item[k], blank_val=blank_val)
            if v == blank_val:
                item.pop(k)
            if not len(item):
                item = blank_val

    elif item == blank_val:
        return blank_val

    return item
