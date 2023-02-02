import os, pygame
from scripts import tile_menu, cursor, core_functs, map_functs, font

class Editor:
    def __init__(self, window_size):
        #save config
        self.map_registries = ["tile", "object", "entity", "info"]
        self.save_file = os.path.join("map", os.listdir("map")[0])
        self.save_status = False

        #data hehe
        self.map_data = self.load_map() 

        for i in self.map_registries:
            self.map_data[i] = self.map_data.get(i, {})

        self.tile_map = self.map_data["tile"]
        self.object_map = self.map_data["object"]
        self.entity_map = self.map_data["entity"] 
        self.map_info = self.map_data["info"]

        #tile config
        self.map_info["chunk_size"] = self.map_info.get("chunk_size", (5, 5))
        self.map_info["tile_size"] = self.map_info.get("tile_size", (13, 13))
        self.map_info["collide_layers"] = self.map_info.get("collide_layers", [0]) 

        self.chunk_size = self.map_info["chunk_size"]
        self.tile_size = self.map_info["tile_size"]

        #gui elements

        #texts
        self.font = font.Font("assets/font/font.png")
        self.map_texts = ["chunk: ", "coords: ", "tile_slot: ", ""]

        #tile menu  
        self.tile_menu = tile_menu.TileMenu((3, 3))
        self.tile_menu.set_render((80, 294))
        self.tile_menu.load_tiles(self.tile_size)

        self.cursor = cursor.Cursor()
        self.cursor.set_tile_info("", 0, tile_size=list(self.tile_size))

        #render
        self.scale = 0.5
        self.surf = pygame.Surface([window_size[i] * self.scale for i in range(2)])
        self.map_render = self.surf.copy()
        self.background_color = (7, 11, 20)

        self.scroll = [0, 0]
        self.scroll_vel = [0, 0]

        self.zoom = 1
        self.zoom_offset = [0, 0]
        self.zoom_limit = [1, 3]


        if self.tile_map == {}:
            self.layer = [0, 0]

        else: self.layer = [0, max([int(i) for i in self.tile_map])]

        #1 for front and 0 for behind
        self.tile_slot = 1

        #editor controls
        self.tool_scheme = [pygame.K_LSHIFT, pygame.K_LALT, pygame.K_CAPSLOCK, pygame.K_SPACE, pygame.K_t, pygame.K_LCTRL, pygame.K_RETURN]         
        self.tool_keys = [False] * len(self.tool_scheme)
        #detects key_taps
        self.tool_tap = self.tool_keys.copy()
        #not used for detection. Change boools of this list
        #to lock certain keys
        self.tool_lock = self.tool_keys.copy()
        
        #used by tool_tap
        self.tool_delay = self.tool_keys.copy()

        self.movement_scheme = "wsad"
        self.movement_keys = [False] * len(self.movement_scheme)
        self.movement_tap = self.movement_keys.copy()
        self.movement_delay = self.movement_keys.copy()

        self.tile_bond = {
                (False, False, False, True) : 2, 
                (False, True, False, True) : 6, 
                (True, True, False, True) : 7, 
                (True, False, False, True) : 8, 
                (False, True, False, False) : 10, 
                (False, True, True, True) : 11, 
                (True, True, True, True) : 12, 
                (True, False, True, True) : 13, 
                (True, False, False, False) : 14,
                (False, True, True, False) : 16, 
                (True, True, True, False) : 17, 
                (True, False, True, False) : 18, 
                (False, False, True, False) : 22 
                } 

        self.map_geography = ["Layer", "Chunk", "Coord", "Tile Slot"]

    
    def add_layer(self):
        self.layer[1] += 1

    def get_chunk(self, coords):
        return [int(coords[i] // (self.chunk_size[i] * self.tile_size[i])) for i in range(2)]

    def switch_layer(self, layer_num):
        self.layer[0] = core_functs.clamp(layer_num, (0, self.layer[1]))

    def layer_handler(self, keys):
        #...where am I supposed to put this then?!?!?
        if self.tool_keys[2]: 
            self.tile_slot = 0
            self.cursor.color = (200, 130, 130)
        else: 
            self.tile_slot = 1
            self.cursor.color = (255, 255, 255)

        if self.tool_tap[4]: 
            self.layer[1] += 1
            self.switch_layer(self.layer[1])

        for i in range(1, 10):
            if keys[pygame.key.key_code(str(i))]:
                self.switch_layer(i - 1)

        if self.tool_keys[5]:
            count = 0
            for value in [-1, 1]:
                if self.movement_tap[2 + count]:
                    self.switch_layer(self.layer[0] + value)
                count += 1

    def show_layers(self, surf, coords):
        for layer in range(self.layer[1] + 1):
            radius = 3
            spacing = 10
            if layer == self.layer[0]: thickness = 0
            else: thickness = 1
            pygame.draw.circle(surf, (255, 255, 255), [coords[0] + layer * (radius + spacing) - (self.layer[1] * (radius + spacing) / 2), coords[1]], radius, thickness)

    #done before calling event_handler() 
    #for every event that's active
    def pre_event_handler(self):
        #negate signals
        self.cursor.negate_click()
        
    def event_handler(self, event):
        self.tile_menu.event_handler(event)
        self.cursor.event_handler(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_CAPSLOCK:
                self.tool_lock[2] = not self.tool_lock[2]

    def update_tool_keys(self, keys):
        self.tool_tap = [False] * len(self.tool_scheme)
        for i in range(len(self.tool_scheme)):
            self.tool_keys[i] = keys[self.tool_scheme[i]]
            #lock override
            if self.tool_lock[i]: self.tool_keys[i] = True
            
            #updates tool_tap
            if self.tool_keys[i] != self.tool_delay[i]:
                self.tool_delay[i] = self.tool_keys[i]
                if self.tool_delay[i]: 
                    self.tool_tap[i] = True

    def tool_key_handler(self, keys):
        self.update_tool_keys(keys)

    def movement_key_handler(self, keys):
        self.movement_tap = [False] * len(self.movement_scheme)

        for i in range(len(self.movement_scheme)):
            self.movement_keys[i] = keys[pygame.key.key_code(self.movement_scheme[i])]

            #... I know I copied it, you judgemental son of a gun
            if self.movement_keys[i] != self.movement_delay[i]:
                self.movement_delay[i] = self.movement_keys[i]
                if self.movement_delay[i]: 
                    self.movement_tap[i] = True

    def check_tile(self, target_loc):
        #I know I copied it ok?
        chunk_key = tuple(self.get_chunk(target_loc))
        loc_key = tuple(target_loc)
        keys = [self.layer[0], chunk_key, loc_key]
        data = core_functs.data_scout(self.tile_map, keys)
        if not data: return False
        elif not data[self.tile_slot]: return False
        else: return True

    #return a tuple of the bond status
    def check_tile_bond(self, target_loc):
        bond = [False] * 4
        index = 0
        for i in range(2):
            for j in [-1, 1]:
                check_coords = target_loc.copy()
                check_coords[i] += j * self.tile_size[i]
                bond[index] = self.check_tile(check_coords)
                index += 1
        
        return tuple(bond)

    def place_tile(self, coords, tile_key):
        self.save_status = False

        chunk_key = tuple(self.get_chunk(coords))
        #low key hahahaha
        loc_key = tuple(coords)

        if tile_key:
            tileset, tile_id = tile_key.rsplit("_", 1)

            tab = self.tile_menu.get_tab_from_name(tileset)
            keys = [self.layer[0], chunk_key, loc_key]
            keys = [keys[i] for i in range(len(keys)) if i in tab.pierce_level]
            core_functs.data_pierce(self.map_data, [tab.get_map_registry()])
            map_registry = self.map_data[tab.get_map_registry()]
            if not self.tile_menu.tile_data.get(tile_key): 
                key = None
            else: key = tile_id

            tab.set_tile_id(map_registry, keys + [self.tile_slot, tileset, key])
            
        else:
            keys = [self.layer[0], chunk_key, loc_key]
            core_functs.data_pierce(self.tile_map, keys, value=[None, None])
            core_functs.data_scout(self.tile_map, keys)[self.tile_slot] = None

            keys = [chunk_key, loc_key]
            core_functs.data_pierce(self.entity_map, keys, value=None)
            core_functs.data_pierce(self.object_map, keys, value=None)
            self.entity_map[chunk_key].pop(loc_key)
            self.object_map[chunk_key].pop(loc_key)

    def scroll_handler(self, dt, keys):
        #movement for camera panning
        self.scroll_vel = [False] * 4

        if self.tool_keys[0]:
            count = 0
            for axis in [1, 0]:
                for val in [-1, 1]:
                    if self.movement_keys[count]:
                        self.scroll_vel[axis] = val * 90 
                    count += 1

        self.scroll = [self.scroll[i] + self.scroll_vel[i] * dt for i in range(2)]

    def selection_fill(self, target_loc, max_iteration=30):
        if max_iteration > 0: 
            if target_loc not in self.cursor.selection:
                self.cursor.selection.append(target_loc)

                for i in range(2):
                    for j in [-1, 1]:
                        coords = target_loc.copy()
                        coords[i] += j * self.tile_size[i]
                        self.selection_fill(coords, max_iteration=max_iteration - 1)

    def selection_handler(self):
        if not self.tool_keys[3]:
            valid_tileset = True
            for i in range(2):
                if self.tile_menu.get_current_tab().surf.get_size()[i] < 4 * self.tile_size[i]:
                    valid_tileset = False

            if len(self.cursor.selection):
                self.selection_fill(self.cursor.cubify(self.cursor.translate_coords()))

                #places tiles for every selection
                for i in self.cursor.selection:
                    self.place_tile(i.copy(), self.tile_menu.tileset + "_" + "12")

                #modifies those tiles based on the tile bond
                for i in self.cursor.selection:
                    bond = self.check_tile_bond(i)

                    if self.cursor.mode:
                        if valid_tileset:
                            tile_info = self.tile_menu.tileset + "_" + str(self.tile_bond.get(bond, 12)) 
                    else:
                        tile_info = None
                        
                    if valid_tileset:
                        self.place_tile(i.copy(), tile_info)

                self.cursor.selection = []

    def text_handler(self, surf):
        spacing = 5

        save_msg = ""
        if self.save_status: save_msg = "progress saved!"
        coords = self.cursor.cubify(self.cursor.translate_coords())
        map_texts = [str(self.get_chunk(coords)), str(coords), str(self.tile_slot), save_msg]


        text = [self.map_texts[i] + map_texts[i] for i in range(len(self.map_texts))]

        for i in range(len(text)):
            self.font.render(surf, text[i], [surf.get_width() - self.font.get_string_size(text[i])[0] - spacing, spacing + 10 * i])
        
    def menu_to_cursor(self):
        self.cursor.set_tile_info(self.tile_menu.tileset, self.tile_menu.tile_id)

    def cursor_to_editor(self, dt):

        cursor_click = self.cursor.click()
        cursor_hold = self.cursor.hold()

        
        if cursor_hold: 
            #translate and cubify coords
            #gosh you don't know how much time I spent getting the translation right
            
            #notes:
            #scroll is the gateway to translation. Tiles, in order to be displayed from 
            #map data to the window, need their coords to be decremented by scroll.
            #Cursor positions, which are in the already in the window, need their coords
            #to be incremented by scroll to convert to map data level.

            #zoom offset which is a variable derived from both map data and window should
            #be understood as belonging in the higher translation level which is , in this case,
            #the window. I don't know if this applies to translations generally 
            #but it works for this game
            coords = self.cursor.cubify(self.cursor.translate_coords())

            if cursor_hold == 1:
                tile_key = self.cursor.tileset + "_" + str(self.cursor.tile_id)
                self.cursor.mode = 1

            elif cursor_hold == 3:
                tile_key = None
                self.cursor.mode = 0


            self.place_tile(coords, tile_key)

            #handles selection tiles
            if self.tool_keys[3]:
                if coords not in self.cursor.selection:
                    self.cursor.selection.append(coords)

                #selection_tile_slot is dictated by the
                #tile slot of the first selected tile
                if not len(self.cursor.selection):
                    self.cursor.selection_tile_slot = self.tile_slot
            #I was originally going to add selection tiles 
            #in a different way but this works too
            
        #the name is kinda useless
        #right now, it just detects
        #mousewheel events
        if cursor_click:
            if cursor_click == 4:
                self.zoom = core_functs.clamp(self.zoom + 30 * dt, self.zoom_limit)
            if cursor_click == 5:
                self.zoom = core_functs.clamp(self.zoom - 30 * dt, self.zoom_limit)

    def render_map(self):
        #fill
        self.map_render.fill(self.background_color)

        #visible chunks
        chunk_loc = [int(self.scroll[i] // (self.chunk_size[i] * self.tile_size[i])) for i in range(2)]
        chunk_amt = [int(self.surf.get_size()[i] // (self.chunk_size[i] * self.tile_size[i])) + 2 for i in range(2)]

        #drawing elements for map_render
        
        #map
        for layer in sorted(range(self.layer[1] + 1), reverse=True):
            if layer in self.tile_map:
                for y in range(chunk_amt[1]):
                    for x in range(chunk_amt[0]):
                        chunk_key = (chunk_loc[0] + x, chunk_loc[1] + y)
                        if chunk_key in self.tile_map[layer]:
                            for coord in self.tile_map[layer][chunk_key]:
                                tile_keys = self.tile_map[layer][chunk_key][coord]
                                for key in tile_keys:
                                    if key != None:
                                        tile_surf = self.tile_menu.tile_data.get(key)
                                        if tile_surf != None:
                                            self.map_render.blit(tile_surf, [coord[i] - self.scroll[i] for i in range(2)])

        for y in range(chunk_amt[1]):
            for x in range(chunk_amt[0]):
                chunk_key = (chunk_loc[0] + x, chunk_loc[1] + y)
                for registry in ["object", "entity"]:
                    if chunk_key in self.map_data[registry]:
                        for coords in self.map_data[registry][chunk_key]:
                            # string after ":" is omitted as it contains info for a particular object
                            data = self.map_data[registry][chunk_key][coords].split(":")[0]
                            if data:
                                self.map_render.blit(self.tile_menu.tile_data[data], [coords[j] - self.scroll[j] for j in range(2)])


        #tile_preview
        preview_tile = self.cursor.get_preview_tile(self.tile_menu.tile_data)
        if preview_tile != None and self.tile_slot == 1:
            preview_coords = self.cursor.translate_coords()
            preview_coords = self.cursor.cubify(preview_coords)
            self.map_render.blit(preview_tile, [preview_coords[i] - self.scroll[i] for i in range(2)])

        #selection render
        self.cursor.render_selection(self.map_render, self.scroll)

        #scaling map's render according to zoom then cutting it to fit the window
        scaled_surf = pygame.transform.scale(self.map_render, [self.map_render.get_size()[i] * self.zoom for i in range(2)])
        cut_dimension = [*[(scaled_surf.get_size()[i] - self.surf.get_size()[i])/2 for i in range(2)], *self.surf.get_size()]
        self.zoom_offset = [(self.surf.get_size()[i] - scaled_surf.get_size()[i])/2 for i in range(2)]
        self.surf.blit(core_functs.cut(scaled_surf, *cut_dimension), (0, 0))

            
    def load_map(self):
        try: data = core_functs.read_json(self.save_file)
        except FileNotFoundError: data = {}
        data = map_functs.mapify_json(data)
        return data
            
    def save_map(self):
        data = core_functs.copy_dict(self.map_data)
        data = map_functs.jsonify_map(data)
        for i in [None, [None, None], {}]:
            core_functs.prune_dict(data, i)

        core_functs.write_json(self.save_file, data)
        self.save_status = True

    def update(self, surf, dt):
        #mouse coords based on window
        mouse_loc = pygame.mouse.get_pos()
        #translate mouse coords to surf coords of editor
        self.cursor.set_loc([mouse_loc[i] * self.scale for i in range(2)])

        keys = pygame.key.get_pressed()

        #update tool key events 
        self.tool_key_handler(keys)
        self.movement_key_handler(keys)
        self.surf.fill((0, 0, 0))

        self.layer_handler(keys)
        self.scroll_handler(dt, keys)
        self.selection_handler()
        self.render_map()

        self.tile_menu.update(self.surf)
        self.cursor.update(self.surf, self.scroll, self.zoom, self.zoom_offset)
        self.menu_to_cursor()
        self.cursor_to_editor(dt)

        #save
        if self.tool_tap[-1]:
            self.save_map()

        self.text_handler(self.surf)
        self.show_layers(self.surf, [self.surf.get_width()/2, 20])
        surf.blit(pygame.transform.scale(self.surf, surf.get_size()), (0, 0))
            
        

