import random
from board import Board


class Entity:
    def __init__(self):
        self.name = None
        self.own_board = None
        self.enemy_board = None
        self.ship_list = None


    def make_move(self):
        pass


class Player(Entity):
    def __init__(self, name, own_board: Board, ship_list, signs_dict):
        super().__init__()
        self.name = name
        self.own_board = own_board
        self.enemy_board = Board(self.own_board.size, signs_dict)
        self.ship_list = ship_list


    def make_move(self):
        print('Input coordinates x y')
        try:
            x, y = map(int, input().split())
            self.enemy_board.shoot(x, y)
        except Exception as ex:
            print(ex)
            return self.make_move()
        else:
            pass



class Bot(Entity):
    prefixes = ['ловкий', 'быстрый', 'резкий', 'дерзкий']
    suffixes = ['ловкач', 'быстрила', 'резак', 'дерзила']

    def __init__(self, size, signs_dict):
        super().__init__()
        self.name = (random.choice(Bot.prefixes) + ' ' + random.choice(Bot.suffixes)).capitalize()
        self.own_board = Board(size, signs_dict)
        self.enemy_board = Board(self.own_board.size, signs_dict)


    def init_board(self):
        pass


    def load_board(self, name, board, ships):
        self.name = name
        self.own_board.get_from_file(board)
        self.ship_list = ships


    def make_move(self):
        pass
