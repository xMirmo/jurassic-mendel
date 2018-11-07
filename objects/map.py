from .objects import DrawableObject
import libtcodpy as libtcod


class Tiles(DrawableObject):
    def __init__(self, x, y, glyph = "", block = False, trasparent = True):
        DrawableObject.__init__(self, glyph, x, y)
        self.block = block
        self.trasparent = trasparent
        self.explored = False
    
    def draw(self):
        if self.explored:
            DrawableObject.draw(self)

class Map():
    def __init__(self, mapX, mapY):
        self.lenght = mapX
        self.height = mapY

        self.mapBuffer = [[Tiles(x, y, " ", True) for y in range(mapY)] for x in range(mapX)]
    
    def get_tile(self, x, y):
        return self.mapBuffer[x][y]
    
    def get_map_list(self):
        return [x for sublist in self.mapBuffer for x in sublist]

    def is_free_at(self, x, y):
        return (self.mapBuffer[x][y].block is False)

    # we should check if the values are inside the map
    def make_room(self, x, y, w, h):
        for j in range(x, x+w):
            for k in range(y, y+h):
                self.mapBuffer[j][k] = Tiles(j, k, ".")

    # we should check if the values are inside the map
    def make_corridor(self, x1, y1, x2, y2):
        step1 = 1 if x1 < x2 else -1
        step2 = 1 if y1 < y2 else -1

        for j in range(x1, x2, step1):
            self.mapBuffer[j][y1] = Tiles(j, y1, ".")
        for k in range(y1, y2,step2):
            self.mapBuffer[j][k] = Tiles(j, k, ".")

    def make_walls(self):
        for x in range(self.lenght):
            for y in range(self.height):
                if self.is_free_at(x, y):
                    for j in range(x-1, x+2, 2):
                        for k in range(y-1, y+2, 2):
                            if not self.is_free_at(j, k):
                                self.mapBuffer[j][k] = Tiles(j, k, "#", True, False)
        

class DrawableMap():
    def __init__(self, currentMap, player):
        self.currentMap = currentMap
        self.player = player
        self.fov_map = libtcod.map_new(currentMap.lenght, currentMap.height)

        list(map(lambda tile:libtcod.map_set_properties(self.fov_map, tile.x, tile.y, tile.trasparent, not tile.block) , currentMap.get_map_list()))

        for tile in self.get_tiles_in_fov(): tile.explored = True
        
    def get_tiles_in_fov(self):
        libtcod.map_compute_fov(self.fov_map, self.player.x, self.player.y, 5, True, 0)
        return list(filter(lambda tile: libtcod.map_is_in_fov(self.fov_map, tile.x, tile.y), self.currentMap.get_map_list()))

    def get_map(self):
        return self.currentMap

    def draw(self):
        for tile in self.currentMap.get_map_list():
            tile.draw()
            libtcod.console_set_char_foreground(0, tile.x, tile.y,  libtcod.Color(255, 0, 0))
        
        for tile in self.get_tiles_in_fov():
            self.currentMap.get_tile(tile.x,tile.y).explored = True
            libtcod.console_set_char_foreground(0, tile.x, tile.y, libtcod.Color(255, 255, 255))
