import os, pygame, math
import core_functs, map_functs
#tabs contain data and returns a surf based on said data

class Tab:
    def __init__(self):
        pass

    def render(self, surf):
        pass

    def update(self, surf):
        pass

class TileSetTab(Tab):
    def __init__(self, source, tile_size, chunk_size):
        if isinstance(source, pygame.Surface):
            self.tileset = source
            self.tileset_name = ""
        else: 
            self.tileset = pygame.image.load(source).convert()
            self.tileset_name = os.path.splitext(os.path.split(source)[1])[0]

        self.tile_size = tile_size
        self.chunk_size = chunk_size
        self.tile_ids = [str(i) for i in range(math.prod([self.tileset.get_size()[i]//self.tile_size[i] for i in range(2)]))]
        self.tile_data = self.set_tile_data()

        self.tile_movement = "wsad"
        self.tile_index = 0

        self.matrix_coords = [0, 0]
        self.scroll = [0, 0]

        self.tileset_surf = self.tileset.copy()
        self.tile_render_spacing = 2
        
        max_render_size = 90
        self.render_size = [core_functs.clamp(self.tileset_surf.get_size()[i] + (self.tileset_surf.get_size()[i]//self.tile_size[i] + 1) * self.tile_render_spacing, (0, max_render_size)) for i in range(2)]
        self.surf = pygame.Surface(self.render_size)

        #oh! Big ballsey move innit lad? Putting a variable that no one would understand.
        #registries = ["tile", "object", "entity"]
        #there are different data structures saved in different files
        self.pierce_level = list(range(3))
        self.map_registry = "tile"

    
    def get_map_registry(self):
        return self.map_registry

    #info = [layer, chunk, coords, tile_slot, tileset, tile_id]
    def set_tile_id(self, dictionary, info):
        core_functs.data_pierce(dictionary, info[:3], value=[None, None])
        if info[-1] != None:
            core_functs.data_scout(dictionary, info[:3])[info[-3]] = "_".join(info[-2:])

    #I don't know why I put so many parameters in a foking method
    def set_tile_data(self):
        data = {}
        surf_list = map_functs.cut_set(self.tileset, self.tile_size)
        for i in range(len(self.tile_ids)):
            data["_".join([j for j in [self.tileset_name, str(self.tile_ids[i])] if len(j)])] = surf_list[i]

        return data

    def get_tile_data(self):
        return self.tile_data

    def to_matrix(self, num):
        return [num%(self.tileset_surf.get_size()[0]//self.tile_size[0]), num//(self.tileset_surf.get_size()[0]//self.tile_size[0])]

    def to_id(self, loc):
        return loc[1] * self.tileset_surf.get_size()[0]//self.tile_size[0] + loc[0]

    def event_handler(self, event):
        count = 0
        if event.type == pygame.KEYDOWN:
            for axis in (1, 0):
                for movement in (-1, 1):
                    if event.key == pygame.key.key_code(self.tile_movement[count]):
                        
                        dimension = [self.tileset_surf.get_size()[i]//self.tile_size[i] for i in range(2)]
                        matrix = self.to_matrix(self.tile_index)
                        matrix[axis] += movement
                        matrix = [core_functs.clamp(matrix[i], (0, dimension[i] - 1)) for i in range(len(matrix))]
                        self.tile_index = self.to_id(matrix)

                    count += 1

    def get_current_tile(self):
        return [self.tileset_name, self.tile_ids[self.tile_index]]

    def get_data(self):
        return self.tile_data

    def update(self):
        self.scroll = [self.to_matrix(self.tile_index)[i] * self.tile_size[i] for i in range(2)]
        self.scroll = [core_functs.clamp(self.scroll[i], (0, self.tileset_surf.get_size()[i] - self.render_size[i])) for i in range(2)]

    def render(self):
        self.surf.fill((0, 0, 0))
        dimensions = [(self.tileset_surf.get_size()[i]//self.tile_size[i]) for i in range(2)]
        count = 0
        for y in range(dimensions[1]):
            for x in range(dimensions[0]):
                loc = [x, y]
                tile_img = self.tile_data["_".join([i for i in [self.tileset_name, str(self.tile_ids[count])] if len(i)])]
                if tile_img:
                    self.surf.blit(tile_img, [self.tile_render_spacing + loc[i] * (self.tile_size[i] + self.tile_render_spacing) for i in range(2)])
                count += 1

        

        #highlight
        pygame.draw.rect(self.surf, (255, 255, 255), (*[self.tile_render_spacing + self.to_matrix(self.tile_index)[i] * (self.tile_size[i] + self.tile_render_spacing) for i in range(2)], *self.tile_size), 1)
        return core_functs.cut(self.surf, *self.scroll, *self.render_size)

        
#entity tab supplies the data to the tile menu 
#which is the opposite to the normal tileset tab

#entities here are loaded like tiles
#the only way to tell them apart is that entities are of "#" tileset i.e.(#_Player, #_Knight)

class UniqueTab(TileSetTab):
    def __init__(self, tileset, tile_ids, tile_size, chunk_size):
        super().__init__(tileset, tile_size, chunk_size)
        self.tile_ids = tile_ids
        self.pierce_level = [1, 2]

    def create_tileset(self, amt, tile_size):
        dimensions = self.get_dimensions(amt)
        surf = pygame.Surface([dimensions[i] * tile_size[i] for i in range(2)])
        surf.fill((0, 0 ,0))
        color_except = [(0, 0, 0)]

        iter_list = [0, 0]
        for iter_list[1] in range(dimensions[1]):
            for iter_list[0] in range(dimensions[0]):
                color = core_functs.randomize_color(color_except=color_except)
                color_except.append(color)
                pygame.draw.rect(surf, color, (*[iter_list[i] * tile_size[i] for i in range(2)], *tile_size))

        return surf
    
    def get_dimensions(self, value):
        for i in sorted(range(1, 6), reverse=True):
            if value != i:
                if not value % i:
                    return [value // i, i]
    
    def create_tile(self, color):
        surf = pygame.Surface(self.tile_size)
        surf.fill(color)
        return surf

    #info = [chunk, coords, tile_slot, tileset, tile_id]
    def set_tile_id(self, dictionary, info):
        if info[-1] != None:
            core_functs.data_pierce(dictionary, info[:2], value="_".join(info[-2:]))

    def set_data(self, surface, name, tile_size):
        data = {}
        surf_list = map_functs.cut_set(surface, tile_size)
        for i in range(len(surf_list)):
            data["_".join([j for j in [name, str(self.objects[i])] if len(j)])] = surf_list[i]

        return data

class EntityTab(UniqueTab):
    def __init__(self, tile_size, chunk_size):
        try: tile_ids = core_functs.read_json('../entities.json') 
        except FileNotFoundError: tile_ids = []
        tileset = self.create_tileset(len(tile_ids), tile_size)

        super().__init__(tileset, tile_ids, tile_size, chunk_size)
        self.tileset_name = "entity"
        self.map_registry = "entity"
        self.tile_data = self.set_tile_data()

    

class ObjectTab(UniqueTab):
    def __init__(self, path, tile_size, chunk_size):
        tile_ids = [os.path.splitext(i)[0] for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]
        self.object_surfs = [pygame.image.load(os.path.join(path, i)) for i in os.listdir(path) if os.path.isfile(os.path.join(path, i))]
        for i in self.object_surfs:
            i.set_colorkey((0, 0, 0))
        tileset = self.create_tileset(len(tile_ids), tile_size) 

        super().__init__(tileset, tile_ids, tile_size, chunk_size)
        self.map_registry = "object"
        self.tileset_name = "object"
        self.tile_data = self.set_tile_data()

    def set_tile_data(self):
        data = {}
        for i in range(len(self.tile_ids)):
            data[self.tileset_name + "_" + str(self.tile_ids[i])] = self.object_surfs[i]
            data["_".join([j for j in [self.tileset_name, self.tile_ids[i]] if len(j)])] = self.object_surfs[i]

        return data

class CustomTileTab(ObjectTab):
    def __init__(self, path, tile_size, chunk_size):
        self.path = path
        super().__init__(path, tile_size, chunk_size)
        self.map_registry = "tile"
        self.pierce_level = list(range(3))

#info = [layer, chunk, coords, tile_slot, tileset, tile_id]
    def set_tile_id(self, dictionary, info):
        core_functs.data_pierce(dictionary, info[:3], value=[None, None])
        if info[-1] != None:
            img_size = self.tile_data[info[-2] + "_" + info[-1]].get_size()
            dimension = [math.ceil(img_size[i]/self.tile_size[i]) for i in range(len(img_size))]

            index = 0
            for y in range(dimension[1]):
                for x in range(dimension[0]):

                    coord = tuple([info[2][0] + self.tile_size[0] * x, info[2][1] + self.tile_size[1] * y])
                    chunk = tuple([coord[i]//(self.tile_size[i] * self.chunk_size[i]) for i in range(2)])

                    core_functs.data_pierce(dictionary, [info[0], chunk, coord], value=[None, None])

                    core_functs.data_scout(dictionary, [info[0], chunk, coord])[info[3]] = "_".join(info[-1:] + [str(index)])
                    index += 1

    def set_tile_data(self):
        self.tileset_name = ""

        data = super().set_tile_data();

        #add tile-ish tile_data too
        for i in self.tile_ids:
            surf_list = map_functs.cut_set(data[i], self.tile_size)
            for j in range(len(surf_list)):
                data[i + "_" + str(j)] = surf_list[j]

        return data


class SurfMesh:
    def __init__(self, surf_size):
        self.surf_size = surf_size

    def abs(self, normalized_loc):
        return [core_functs.lerp(0, self.surf_size[i], normalized_loc[i]) for i in range(2)]

    def rel(self, loc):
        return [loc[i]/self.surf_size[i] for i in range(2)]

