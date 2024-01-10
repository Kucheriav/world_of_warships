class Ship:
    def __init__(self, x, y, dir, size):
        self.coords = list()
        self.dir = dir
        if dir == 'h':
            for i in range(size):
                self.coords.append([y, x + i])
        else:
            for i in range(size):
                self.coords.append([y + i, x])
        self.hitbox = [1 for i in range(size)]