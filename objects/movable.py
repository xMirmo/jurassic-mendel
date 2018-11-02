class MovableObject:

    def __init__(self, x, y):
        self.x = x;
        self.y = y;
    
    def move_object(self, dx, dy):
        self.x += dx
        self.y += dy