from .drawable import DrawableObject
from .movable import MovableObject

class Player(DrawableObject, MovableObject):

    def __init__(self, sprite, x, y):
        MovableObject.__init__(self, x, y)
        DrawableObject.__init__(self, sprite, x, y)