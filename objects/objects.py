from .drawable import DrawableObject
from .movable import MovableObject
from .descriptionobject import DescriptionObject
from .aiable import AIObject
from random import shuffle, randint



class Entity(DrawableObject, MovableObject, DescriptionObject, AIObject):
    def __init__(self, sprite, x, y, name, description, ai):
        MovableObject.__init__(self, x, y)
        DrawableObject.__init__(self, sprite, x, y)
        DescriptionObject.__init__(self, name, description)
        AIObject.__init__(self, ai)
    
    def __str__(self):
        return self.name


class Player(Entity):
    def __init__(self, sprite, x, y):
        self.inventory = list()
        Entity.__init__(self, sprite, x, y, "Player", "A player", AIObject.get_input_act)


class Monster(Entity):
    def __init__(self, sprite, x, y, name, description, ai):
        Entity.__init__(self, sprite, x, y, name, description, ai)


class Item(Entity): 
    @staticmethod
    def factory(x, y):
        random_seed = randint(0, 1)
        if random_seed == 0:
           return Sword(x,y)
        elif random_seed == 1:
           return Potion(x,y)

class Sword(Item): 
    def __init__(self,x, y):
        Entity.__init__(self, "+", x, y, "Sword of Silver Sword", "Pointy!", AIObject.empty_ai)

class Potion(Item): 
    def __init__(self, x, y):
        Entity.__init__(self, "8", x, y, "Limoncello", "Hm...", AIObject.empty_ai)    