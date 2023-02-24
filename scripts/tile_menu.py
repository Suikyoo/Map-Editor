import pygame, os 
from scripts import map_functs, core_functs, tab, font

class TileMenu:
    def __init__(self, coords):
        #tile data is a dictionary that contains a tile 
        #with their identifier as key
        self.tile_data = {}

        self.tileset = ""
        self.tile_id = 0

        self.tabs = []
        self.tab_index = 0

        self.coords = coords

        self.font = font.Font('assets/font/font.png')
        self.tile_texts = ["", ""]

    def set_loc(self, coords):
        self.coords = coords

    def set_render(self, size):
        #render
        self.color_scheme = ((46, 66, 102), (90, 110, 160))
        self.surf = pygame.Surface(size)
        self.surf_mesh = tab.SurfMesh(size)
        self.tab_vertical_loc = 80

        div = self.tab_vertical_loc - 5
        self.menu_padding = (
                (1, 1, self.surf.get_width() - 2, div - 3), 
                (1, div - 1, self.surf.get_width() - 2, self.surf.get_height() - div)
                )

    def load_tiles(self, tile_size):
        self.tile_size = tile_size

        directory = "assets/tiles"

        tileset_dir = os.path.join(directory, "tilesets")
        for file in os.listdir(tileset_dir):
            tileset_name = os.path.splitext(file)[0]
            if os.path.isfile(os.path.join(tileset_dir, file)):
                #tabs
                tile_tab = tab.TileSetTab(os.path.join(tileset_dir, file), tile_size)

                #get tile data from tab and add it to the general tile data
                self.tabs.append(tile_tab)

        self.tabs.append(tab.ObjectTab(os.path.join(directory, 'objects'), tile_size))
        self.tabs.append(tab.CustomTileTab(os.path.join(directory, 'custom_tilesets'), tile_size))
        self.tabs.append(tab.EntityTab(tile_size))

        #unique_tiles = [self.tabs[-i].get_tile_data() for i in range(3)]
        for i in [i.get_tile_data() for i in self.tabs]:
            for k, v in i.items():
                self.tile_data[k] = v

    def get_current_tab(self):
        return self.tabs[self.tab_index]

    def get_tab_from_name(self, string):
        for i in self.tabs:
            if i.tileset_name == string:
                return i

    def event_handler(self, event):
        self.tabs[self.tab_index].event_handler(event) 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.tab_index  = (self.tab_index + 1) % len(self.tabs)
        
    def draw(self, surf):
        #setting current_tab as it takes way too long to write self.tabs[self.tab_index]
        current_tab = self.get_current_tab()


        current_tab.update()

        #set tile info
        self.tileset, self.tile_id = current_tab.get_current_tile()

        self.surf.fill(self.color_scheme[1])
        
        for i in self.menu_padding:
            pygame.draw.rect(self.surf, self.color_scheme[0], i)

        tile_text = [self.tileset, str(self.tile_id)]
        text = [self.tile_texts[i] + tile_text[i] for i in range(2)]
        self.font.render_lines(self.surf, 20, 5, text)

        self.surf.blit(current_tab.render(), [self.surf_mesh.abs((0.5, 0.5))[0] - current_tab.render_size[0]/2, self.tab_vertical_loc])
        surf.blit(self.surf, self.coords)

    def update(self, surf):
        self.draw(surf)
