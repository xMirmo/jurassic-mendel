from .objects import DrawableObject
import libtcodpy as libtcod


class Tiles(DrawableObject):
    def __init__(self, x, y, glyph = "", block = False, trasparent = True):
        DrawableObject.__init__(self, glyph, x, y)
        self.block = block
        self.trasparent = trasparent

class Map():
    def __init__(self, mapX, mapY):
        self.lenght = mapX
        self.height = mapY

        self.mapBuffer = [[Tiles(x, y, " ", True) for y in range(mapY)] for x in range(mapX)]
    
    def get_tile(self, x, y):
        return self.mapBuffer[x][y]

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
                                self.mapBuffer[j][k] = Tiles(j, k, "#", True)
        

class DrawableMap():
    def __init__(self, map, player):
        self.currentMap = map
        self.player = player
        self.fov_map = libtcod.map_new(map.mapX, map.mapY)

        for y in range(map.mapY):
            for x in range(map.mapX):
                libtcod.map_set_properties(self.fov_map, x, y, self.currentMap.get_tile(x,y).trasparent, not self.currentMap.get_tile(x,y).block)
    
    def get_map(self):
        return self.currentMap

    def draw(self):
        for y in range(self.currentMap.height):
           for x in range(self.currentMap.lenght):
               self.currentMap.get_tile(x,y).draw()

