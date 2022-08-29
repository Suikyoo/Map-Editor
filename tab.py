import pygame, core_functs
#tabs contain data and returns a surf based on said data

class Tab:
    def __init__(self):
        pass

    def render(self, surf):
        pass

    def update(self, surf):
        pass

class TileSetTab(Tab):
    def __init__(self, tileset_surf, tile_size):
        self.name = "tileset"
        self.tile_movement = "wsad"
        self.tile_id = 0
        self.tile_size = tile_size

        self.matrix_coords = [0, 0]
        self.scroll = [0, 0]

        self.surf = tileset_surf.copy()
        self.tileset_surf = tileset_surf.copy()

    def get_size(self):
        return self.surf.get_size()

    def set_name(self, name):
        self.name = name

    def to_matrix(self, num):
        return [num%(self.tileset_surf.get_size()[0]//self.tile_size[0]), num//(self.tileset_surf.get_size()[1]//self.tile_size[1])]

    def to_id(self, loc):
        return loc[1] * self.tileset_surf.get_size()[1]//self.tile_size[1] + loc[0]

    def event_handler(self, event):
        count = 0
        if event.type == pygame.KEYDOWN:
            for index in range(2):
                for movement in range(2):
                    increment = -1
                    if movement == 1: increment = 1 
                    if event.key == pygame.key.key_code(self.tile_movement[count]):
                        self.matrix_coords[(index + 1) % 2] += increment
                        
                    count += 1

    def update(self):
        self.scroll = [self.to_matrix(self.tile_id)[i] * self.tile_size[i] for i in range(2)]
        self.matrix_coords = [core_functs.clamp(self.matrix_coords[i], (0, self.get_size()[i]//self.tile_size[i] - 1)) for i in range(2)]
        print(self.tile_id)

    def render(self):
        self.surf.fill((0, 0, 0))
        self.surf.blit(self.tileset_surf, (0, 0))

        #highlight
        pygame.draw.rect(self.surf, (255, 255, 255), (*[self.matrix_coords[i] * self.tile_size[i] for i in range(2)], *self.tile_size), 1)
        #update tile id
        self.tile_id = self.to_id(self.matrix_coords)

        return self.surf.copy()

class SurfMesh:
    def __init__(self, surf_size):
        self.surf_size = surf_size

    def abs(self, normalized_loc):
        return [core_functs.lerp(0, self.surf_size[i], normalized_loc[i]) for i in range(2)]

    def rel(self, loc):
        return [loc[i]/self.surf_size[i] for i in range(2)]

