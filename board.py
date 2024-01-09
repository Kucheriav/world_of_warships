class MapEvents(Exception):
    pass


class StartOutOfBound(MapEvents):
    def __init__(self):
        super().__init__('Start of your ship is out of bound!')


class LengthOutOfBound(MapEvents):
    def __init__(self):
        super().__init__('End of your ship is out of bound!')


class ShipCollision(MapEvents):
    def __init__(self, ):
        super().__init__('Your ship collides with existing one!')


class ShootOutOfBound(MapEvents):
    def __init__(self, ):
        super().__init__('You shoot out of bound!')


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


class Board:
    def __init__(self, size, empty='_'):
        self.size = size
        if empty != '_':
            self.empty = empty
        self.map = [[self.empty for i in range(self.size + 2)] for j in range(self.size + 2)]
        # обнулится после постановки кораблей
        self.ships_number_dict = self.calculate_ship_number()
        self.ships = list()

    def __str__(self):
        print(*[x for x in range(self.size + 1)])
        for y in range(1, self.size + 1):
            print(y, end=' ')
            print(*self.map[y][1: -1])

    def calculate_ship_number(self):
        ship_cells = self.size * self.size * 20 // 100
        sample_ship_cells = 20
        coef = ship_cells // sample_ship_cells
        ship_dict = {
            'четырехпалубный': 1 * coef,
            'трехпалубный': 2 * coef,
            'двухпалубный': 3 * coef,
        }
        ship_dict['однопалубный'] = ship_cells - sum(ship_dict.values())
        return ship_dict

    def prepare_board(self):
        decks = list(self.ships_number_dict.keys())
        for ship_type in self.ships_number_dict:
            i = 0
            while i < self.ships_number_dict[ship_type]:
                try:
                    self.__str__()
                    print(f'Choose coordinates for {ship_type}')
                    x, y = map(int, input().split())
                    print('Input direction h / v')
                    dir = input()
                    size = len(decks) - decks.index(ship_type)
                    self.set_ship(x, y, dir, size)
                except Exception as ex:
                    print(repr(ex))
                else:
                    i += 1

    def set_ship(self, x, y, dir, size):
        # без невидимого зазора
        # все проверки вынесены в функцию
        if not self.check_new_ship(x, y, dir, size):
            return
        if dir == 'h':
            for i in range(size):
                self.map[y][x + i] = '0'
        else:
            for i in range(size):
                self.map[y + i][x] = '0'
        self.ships.append(Ship(x, y, dir, size))

    def check_new_ship(self, x, y, dir, size):
        if x < 1 or y < 1 or x > self.size or y > self.size:
            raise StartOutOfBound()
        if dir == 'h' and (x + size) > self.size:
            raise LengthOutOfBound
        if dir == 'v' and (y + size) > self.size:
            raise LengthOutOfBound
        if dir == 'h':
            for i in range(size):
                if self.map[y][x + i] == '0':
                    raise ShipCollision
        else:
            for i in range(size):
                if self.map[y + i][x] == '0':
                    raise ShipCollision
        return True

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

    def get_from_file(self):
        pass
