import os
import random
from board import Board
class Entity:
    def __init__(self):
        self.name = None
        self.own_board = None
        self.enemy_board = None


    def upload_file(self):
        pass


    def make_move(self):
        pass


class Player(Entity):
    def __init__(self, name, own_board: Board):
        super().__init__()
        self.name = name
        self.own_board = own_board
        self.enemy_board = Board(self.own_board.size)

    def ship_input_loop(self):
        pass

    def upload_file(self):
        print('Input file name')
        filename = input()
        while filename not in os.listdir():
            print('No such filename!')
            filename = input()
        file = open(filename)
        sells = [x.split() for x in file.readlines()]
        self.own_board = Board(size=len(sells))
        self.own_board


    def make_move(self):
        pass


class Bot(Entity):
    prefixes = ['ловкий', 'быстрый', 'резкий', 'дерзкий']
    suffixes = ['ловкач', 'быстрила', 'резак', 'дерзила']

    def __init__(self, size):
        super().__init__()
        self.name = (random.choice(Bot.prefixes) + ' ' + random.choice(Bot.suffixes)).capitalize()
        self.own_board = Board(size)

    def make_move(self):
        pass
