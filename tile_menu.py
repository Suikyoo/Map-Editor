import pygame, os, map_functs, core_functs, tab

class TileMenu:
    def __init__(self, coords=[0, 0], surf_size=(100, 100)):
        self.tile_dimension = [13, 13]

        #tile data is a dictionary that contains a list of tiles 
        #with their corresponding tileset name as key
        self.tile_data = {}
        self.tabs = []
        self.tab_index = 0

        directory = "assets/tilesets"
        for file in os.listdir(directory):
            tileset_name = os.path.splitext(file)[0]

            #tabs
            self.tabs.append(tab.TileSetTab(pygame.image.load(os.path.join(directory, file)).convert(), self.tile_dimension))
            self.tabs[-1].set_name(tileset_name)

            self.tile_data[tileset_name] = map_functs.cut_tile(os.path.join(directory, file), (12, 12))

        #render
        self.surf = pygame.Surface(surf_size)
        self.surf_mesh = tab.SurfMesh(surf_size)
        self.tileset_render = pygame.Surface((50, 50))
        self.coords = coords

    def event_handler(self, event):
        self.tabs[self.tab_index].event_handler(event) 
        
    def draw(self, surf):
        #setting current_tab as it takes way too long to write self.tabs[self.tab_index]
        current_tab = self.tabs[self.tab_index]

        #scroll for tile palette
        current_tab.update()
        #clamping scroll
        #idea: change start value of clamp for a sloppy scroll(scrolls only when selection is out of screen)
        current_tab.scroll = [core_functs.clamp(current_tab.scroll[i], (0, current_tab.get_size()[i] - self.tileset_render.get_size()[i])) for i in range(2)]

        self.surf.fill((46, 66, 102))

        self.tileset_render.blit(core_functs.cut(current_tab.render(), *current_tab.scroll, *current_tab.get_size()), (0, 0))

        self.surf.blit(self.tileset_render, [self.surf_mesh.abs((0.5, 0.5))[i] - self.tileset_render.get_size()[i]/2 for i in range(2)])
        surf.blit(self.surf, self.coords)

    def update(self, surf):
        self.draw(surf)
