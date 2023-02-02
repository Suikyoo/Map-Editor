import pygame 
from scripts import core_functs

class Cursor:
    def __init__(self):
        self.coords = [0, 0]
        self.scroll = [0, 0]
        self.zoom_offset = [0, 0]
        self.zoom = 1

        self.img = pygame.image.load('assets/cursor/cursor.png').convert()
        self.img.set_colorkey((0, 0, 0))
        self.color = (255, 255, 255)

        #tile info
        self.tile_size = [0, 0]
        self.tileset = ""
        self.tile_id = 0

        #[click, hold]
        self.control_state = [False, False]
        self.button_type = 1
        #1 : draw, 0 : erase
        self.mode = 1

        #list of coords
        self.selection = []

    def set_loc(self, coords):
        self.coords = coords

    def set_tile_info(self, tileset, id, tile_size=None):
        self.tileset = tileset
        self.tile_id = id

        if tile_size: self.tile_size = tile_size

    def event_handler(self, event):
        #clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.control_state = [True, True]
            self.button_type = event.button

        #holds
        if event.type == pygame.MOUSEBUTTONUP:
            self.control_state[1] = False

    #these functions are getters
    #I just want to name them 
    #without the "get_" for once
 
    #tracks mousewheel inputs in 
    #button_types 4 and 5
    def click(self):
        if self.control_state[0]:
            return self.button_type

    def hold(self):
        if self.control_state[1]:
            return self.button_type

    def cubify(self, coords=None):
        if not coords:
            coords = self.coords.copy()

        return [int((coords[i]//self.tile_size[i]) * self.tile_size[i]) for i in range(2)]

    def translate_coords(self):
        return [(self.coords[i] - self.zoom_offset[i]) / self.zoom + self.scroll[i] for i in range(2)]

    def negate_click(self):
        #negate click at the end of update
        self.control_state[0] = False

    #returns a surface based on the cursor's tile data
    #with the help of the dictionary as an argument
    def get_preview_tile(self, dictionary):
        return dictionary.get(self.tileset + "_" + str(self.tile_id))

    def draw(self, surf, scroll):
        surf.blit(core_functs.swap_color(self.img, [(255, 255, 255), self.color]), self.coords)

    def render_selection(self, surf, scroll):
        for i in self.selection:
            pygame.draw.rect(surf, (255, 255, 255), (*[i[j] - scroll[j] for j in range(2)], *self.tile_size), 1)
    
    def update(self, surf, scroll, zoom, zoom_offset):
        self.scroll = scroll
        self.zoom = zoom
        self.zoom_offset = zoom_offset

        self.draw(surf, scroll)

