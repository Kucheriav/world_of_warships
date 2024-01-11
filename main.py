from os import listdir
from active_entities import Player, Bot
from events import NoSuchFileError, CorruptedSettingsFileError
import pickle

class Game:
    def __init__(self):
        self.round = 0
        self.board_size = 10
        self.signs = {'empty': '', 'miss': '', 'hit': '', 'ship': ''}
        self.player1 = None
        self.player2 = None

    def load_settings(self, filename):
        if filename not in listdir():
            raise NoSuchFileError
        else:
            with open(filename) as file:
                data = {}
                for line in file:
                    x = line.strip().split()
                    data[x[0]] = x[1]
                for key in self.signs:
                    if key not in data:
                        raise CorruptedSettingsFileError
                    else:
                        self.signs[key] = data[key]


    def greeting(self):
        print('Welcome to warships battle!')
        print('Choose an option:\n1.new game\n2.load game\n3.exit')
        answ1 = input()
        while True:
            if answ1 == '1':
                break
            elif answ1 == '2':
                break
            elif answ1 == '3':
                print('Goodbye!')
                break
            else:
                print('Incorrect input!')
                answ1 = input()

        print('Choose an option:\n1.player vs player\n2.player vs bot\n3.return')
        answ2 = input()
        while True:
            if answ2 == '1':
                break
            elif answ2 == '2':
                break
            elif answ2 == '3':
                return self.greeting()
            else:
                print('Incorrect input!')
                answ2 = input()

        # new p_v_p
        if answ1 == 1 and answ2 == 1:
            print('Choose an option:\n1.input ships coordinates\n2.upload file\n3.return')
            answ = input()
            while True:
                if answ == '1':
                    print('Player1, input your name')
                    name = self.get_player_name()
                    print(f'{name}, get ready to input your ship coordinates')
                    board, ships = self.input_loop()
                    self.player1 = Player(name, board, ships, self.signs)
                    print("That's all! Now it's player2 turn!")
                    print('Player2, input your name')
                    name = self.get_player_name()
                    print(f'{name}, get ready to input your ship coordinates')
                    board, ships = self.input_loop()
                    self.player2 = Player(name, board, ships, self.signs)
                elif answ == '2':
                    print('This option is temporary unavailable!')
                    continue
                    # something
                elif answ == '3':
                    return self.greeting()
                else:
                    print('Incorrect input!')
                    answ = input()
        # new p_v_b
        elif answ1 == 1 and answ2 == 2:
            print('Choose an option:\n1.input ships coordinates\n2.upload txt file\n3.return')
            answ = input()
            while True:
                if answ == '1':
                    print('Hello, player1! Get ready to input your ship coordinates')
                    board, ships = self.input_loop()
                    print('Input your name')
                    name = self.get_player_name()
                    self.player1 = Player(name, board, ships, self.signs)
                    self.player2 = Bot(self.board_size, self.signs)
                    self.player2.init_board()
        ##############initialize bot board #####################
                elif answ == '2':
                    print('This option is temporary unavailable!')
                    continue
                    # print('Hello, player1! Get ready to input your filename')
                    # print(f'This file should contain matrix {self.board_size}x{self.board_size}')
                    # print('Use this signs:')
                    # saved_game = self.load_file()
                    # self.player1 = Player(*saved_game[0])
                    # self.player2 = Player(*saved_game[1])
                    # self.round = saved_game[2]
                elif answ == '3':
                    return self.greeting()
                else:
                    print('Incorrect input!')
                    answ = input()
        # load p_v_p
        elif answ1 == 2 and answ2 == 1:
            saved_game = self.load_game()
            self.player1 = Player(*saved_game[0])
            self.player2 = Player(*saved_game[1])
            self.round = saved_game[2]

        # load p_v_b
        elif answ1 == 2 and answ2 == 2:
            saved_game = self.load_game()
            self.player1 = Player(*saved_game[0])
            self.player2 = Bot(self.board_size, self.signs)
            self.player2.load_board(*saved_game[1])
            self.round = saved_game[2]


    def get_player_name(self):
        answ = input()
        while True:
            print('Is this correct?')
            print(answ)
            print('If ok - just hit Enter. Else - input again')
            answ_copy = answ
            answ = input()
            if not answ:
                return answ_copy


    # def load_file(self):
    #     print('Input file name')
    #     filename = input()
    #     while filename not in listdir():
    #         print('No such filename!')
    #         filename = input()
    #     file = open(filename)
    #     sells = [x.split() for x in file.readlines()]
    #     self.player_board = Board(size=len(sells))
    #     self.player_board.map = sells
    #     return 'result'


    def load_game(self):
        print('Input file name')
        filename = input()
        while filename not in listdir():
            print('No such filename!')
            filename = input()
        with open(f'{filename}.pickle', 'rb') as f:
            data = pickle.load(f)
        return data

    def save_game(self, filename):
        with open(f'{filename}.pickle', 'wb') as f:
            data = [self.player1, self.player2, self.round]
            pickle.dump(data, f)

    def input_loop(self):
        while True:
            try:
                x, y = map(int, input().split())
                break
            except Exception:
                print('Wrong coordinates')
        return x, y

    # def print_board(self):
    #     space = ' ' * len(str(self.size))
    #     hor_header = ' ' + space.join([str(x) for x in range(self.size + 1)])[1:]
    #     margin = ' ' * 4
    #     print(hor_header, end=' ' * (4 - len(str(self.size)) + 1))
    #     print(hor_header)
    #     for y in range(1, self.size + 1):
    #         print(y, end=' ' * (len(str(self.size)) - len(str(y)) + 1))
    #         print(space.join(self.player_board.map[y][1: -1]), end=margin)
    #         print(y, end=' ' * (len(str(self.size)) - len(str(y)) + 1))
    #         print(space.join(self.bot_visble_board.map[y][1: -1]))


    # def save_to_file(self, filename):
    #     file = open(filename, 'w')
    #     for line in self.map:
    #         file.write(line)
    #         file.write('\n')
    #     file.close()



    # def main_loop(self):
    #     while True:
    #         self.print_board()
    #         print('Shoot!')
    #         print('input x y')
    #         x, y = self.input_loop()


if __name__ == '__main__':
    game = Game()
    try:
        game.load_settings('settings.txt')
    except FileExistsError:
        print('Error while loading settings!')
    except CorruptedSettingsFileError:
        print('Settings file is corrupted!')
    else:
        game.greeting()