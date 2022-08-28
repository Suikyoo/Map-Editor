import pygame

class Tab:
    def __init__(self):
        pass

    def draw(self, surf):
        pass

    def update(self, surf):
        pass

class TileSetTab(Tab):
    def __init__(self, tileset_surf, tile_size):
        self.tile_index = 0
        self.tile_size = tile_size

        self.tileset_surf = tileset_surf.copy()
        self.surf = tileset_surf.copy()

    def get_matrix_loc(self, num):
        return [num%(self.tileset_surf[0]//self.tile_size[0]), num//(self.tileset_surf[1]//self.tile_size[1])]

    def update(self, surf):
        self.surf.fill((0, 0, 0))
        self.surf.blit(self.tileset_surf)

        #highlight
        normalized_loc = get_matrix_loc(self.tile_index)
        pygame.draw.rect(self.surf, *[normalized_loc[i] * self.tile_size[i] for i in range(2)], *self.tile_size)

        return self.surf.copy()
