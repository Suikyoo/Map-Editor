import pygame, core_functs, math
#tabs contain data and returns a surf based on said data

class Tab:
    def __init__(self):
        pass

    def render(self, surf):
        pass

    def update(self, surf):
        pass

class TileSetTab(Tab):
    def __init__(self, path, tile_size):
        self.tileset = pygame.image.load(path).convert()
        self.tileset_name = os.path.splitext(os.path.split(path)[1])[0]
        self.tile_size = tile_size
        self.tile_data = self.set_data(self.tileset, self.tileset_name, self.tile_size)

        self.tile_movement = "wsad"
        self.tile_id = 0

        self.matrix_coords = [0, 0]
        self.scroll = [0, 0]

        self.surf = tileset_surf.copy()
        self.tileset_surf = tileset_surf.copy()
        
        max_render_size = 70
        self.render_size = [core_functs.clamp(self.get_size()[i], (0, max_render_size)) for i in range(2)]

        #oh! Big ballsey move innit lad? Putting a variable that no one would understand.
        self.pierce_level = 3 

    #too lazy to do self.surf.get_size()
    def get_size(self):
        return self.surf.get_size()

    #I don't know why I put so many parameters in a foking method
    def set_data(self, surface, name, tile_size):
        data = {}
        surf_list = map_functs.cut_set(surface, tile_size)
        for i in range(len(surf_list)):
            data[name + "_" + str(i)] = surf_list[i]

        return data

    def to_matrix(self, num):
        return [num%(self.get_size()[0]//self.tile_size[0]), num//(self.get_size()[0]//self.tile_size[0])]

    def to_id(self, loc):
        return loc[1] * self.get_size()[1]//self.tile_size[1] + loc[0]

    def event_handler(self, event):
        count = 0
        if event.type == pygame.KEYDOWN:
            for axis in (1, 0):
                for movement in (-1, 1):
                    if event.key == pygame.key.key_code(self.tile_movement[count]):
                        
                        dimension = [self.surf.get_size()[i]//self.tile_size[i] for i in range(2)]
                        matrix = self.to_matrix(self.tile_id)
                        matrix[axis] += movement
                        matrix = [core_functs.clamp(matrix[i], (0, dimension[i] - 1)) for i in range(len(matrix))]
                        self.tile_id = self.to_id(matrix)

                    count += 1

    def get_current_tile(self):
        return [self.tileset_name, self.tile_id]

    def get_data(self):
        return self.tile_data

    def update(self):
        self.scroll = [self.to_matrix(self.tile_id)[i] * self.tile_size[i] for i in range(2)]
        self.scroll = [core_functs.clamp(self.scroll[i], (0, self.get_size()[i] - self.render_size[i])) for i in range(2)]

    def render(self):
        self.surf.fill((0, 0, 0))
        self.surf.blit(self.tileset_surf, (0, 0))

        #highlight
        pygame.draw.rect(self.surf, (255, 255, 255), (*[self.to_matrix(self.tile_id)[i] * self.tile_size[i] for i in range(2)], *self.tile_size), 1)
        return core_functs.cut(self.surf, *self.scroll, *self.render_size)

        
#entity tab supplies the data to the tile menu 
#which is the opposite to the normal tileset tab

#entities here are loaded like tiles
#the only way to tell them apart is that entities are of "#" tileset i.e.(#_Player, #_Knight)

class ObjectTab(TileSetTab):
    def __init__(self, path, tile_size):
        self.objects = []
        super().__init__(path, tile_size)

    def set_data(self, surface, name, tile_size):
        data = {}
        surf_list = map_functs.cut_set(surface, tile_size)
        for i in range(len(surf_list)):
            data[name + "_" + self.objects[i]]= surf_list[i]

        return data
class EntityTab(TileSetTab):
    def __init__(self, tile_size):
        self.entities = ["Player", "Knight", "Invoker"]
        tileset_surf = self.create_tileset(len(self.entities), tile_size)
        super().__init__(tileset_surf, tile_size)
        self.tile_data = self.set_tile_data()

    def create_tileset(self, amt, tile_size):
        surf = pygame.Surface((amt * tile_size[0], tile_size[1]))
        surf.fill((0, 0 ,0))
        color_except = [(0, 0, 0)]

        for i in range(amt):
            color = core_functs.randomize_color(color_except=color_except)
            color_except.append(color)
            pygame.draw.rect(surf, color, (i * tile_size[0], 0, *tile_size))

        return surf
    
    def create_tile(self, color):
        surf = pygame.Surface(self.tile_size)
        surf.fill(color)
        return surf

    def set_tile_data(self):
        data = {}
        count = 0
        for x in range(len(self.entities)): 
            data[self.entities[count]] = self.create_tile(self.tileset_surf.get_at((x * self.tile_size[0], 0)))
            count += 1
        return data

    def get_tile_data(self):
        return self.tile_data

    #override get_info to modify the second value returned
    #from: tile_id ie [0, 1, 2, 3] to: entity_id["Player", Entity"]
    def get_info(self):
        return [self.tileset, self.entities[self.tile_id]]
        
class SurfMesh:
    def __init__(self, surf_size):
        self.surf_size = surf_size

    def abs(self, normalized_loc):
        return [core_functs.lerp(0, self.surf_size[i], normalized_loc[i]) for i in range(2)]

    def rel(self, loc):
        return [loc[i]/self.surf_size[i] for i in range(2)]

