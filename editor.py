import pygame, sys, tile_menu, cursor 

class Editor:
    def __init__(self, window_size=[500, 500]):
        #gui elements
        self.tile_menu = tile_menu.TileMenu()
        self.cursor = cursor.Cursor()

        #render
        scale = 0.5
        self.surf = pygame.Surface([window_size[i] * scale for i in range(2)])
        self.scroll = [0, 0]
        self.zoom = 1

        #map data hehe
        self.map_data = {}

    def draw(self, surf):
        pass

    def update(self, surf):
        while True:
            for i in pygame.event.get():
                self.tile_menu.event_handler(i)
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.surf.fill((0, 0, 0))


            self.tile_menu.update(self.surf)

            surf.blit(pygame.transform.scale(self.surf, surf.get_size()), (0, 0))
            pygame.display.update()
            
        

