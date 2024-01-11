from ship import Ship
from events import *



class Board:
    def __init__(self, size, signs_dict):
        self.size = size
        self.empty = signs_dict['empty']
        self.hit = signs_dict['hit']
        self.ship = signs_dict['ship']
        self.miss = signs_dict['miss']
        self.map = [[self.empty for i in range(self.size + 2)] for j in range(self.size + 2)]

    def __str__(self):
        print(*[x for x in range(self.size + 1)])
        for y in range(1, self.size + 1):
            print(y, end=' ')
            print(*self.map[y][1: -1])


    def add_ship(self, x, y, dir, size):
        if not self.check_new_ship(x, y, dir, size):
            return
        if dir == 'h':
            for i in range(size):
                self.map[y][x + i] = self.ship
        else:
            for i in range(size):
                self.map[y + i][x] = self.ship


    def check_new_ship(self, x, y, dir, size):
        if x < 1 or y < 1 or x > self.size or y > self.size:
            raise StartOutOfBound()
        if dir == 'h' and (x + size) > self.size:
            raise LengthOutOfBound
        if dir == 'v' and (y + size) > self.size:
            raise LengthOutOfBound
        if dir == 'h':
            for i in range(size):
                if self.map[y][x + i] != self.empty:
                    raise ShipCollision
        else:
            for i in range(size):
                if self.map[y + i][x] != self.empty:
                    raise ShipCollision
        return True



#####need to refactor###############
    def shoot(self, x, y):
        if x < 1 or y < 1 or x >= self.size or y >= self.size:
            return
        if self.map[y][x] == 'X':
            return
        if self.map[y][x] != '0':
            self.map[y][x] = '.'
            return
        self.map[y][x] = 'X'
        this_ship = None
        for ship in self.ships:
            if [y, x] in ship.coords:
                this_ship = ship
                break
        i = this_ship.coords.index([y, x])
        this_ship.coords[i] = 0
        if sum(this_ship.coords) == 0:
            self.draw_aura(this_ship)
            self.ships.remove(this_ship)

    def draw_aura(self, ship: Ship):
        if ship.dir == 'v':
            y, x = ship.coords[0]
            self.map[y - 1][x - 1] = '.'
            self.map[y - 1][x] = '.'
            self.map[y - 1][x + 1] = '.'
            for y, x in ship.coords:
                self.map[y][x - 1] = '.'
                self.map[y][x + 1] = '.'
            self.map[y + 1][x - 1] = '.'
            self.map[y + 1][x] = '.'
            self.map[y + 1][x + 1] = '.'
        else:
            y, x = ship.coords[0]
            self.map[y - 1][x - 1] = '.'
            self.map[y][x - 1] = '.'
            self.map[y + 1][x - 1] = '.'
            for y, x in ship.coords:
                self.map[y - 1][x] = '.'
                self.map[y + 1][x] = '.'
            self.map[y - 1][x + 1] = '.'
            self.map[y][x + 1] = '.'
            self.map[y + 1][x + 1] = '.'

    def check_lose(self):
        if not self.ships:
            return False
        return True

    def get_ships_number(self):
        return len(self.ships)

    def get_cell(self, x, y):
        return self.map[y][x]

    def set_from_matrix(self, matrix):
        self.map = matrix

    def get_map(self):
        return self.map
