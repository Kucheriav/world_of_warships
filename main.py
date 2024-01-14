from os import listdir
from ship import Ship
from board import Board
from active_entities import Player, Bot
from events import NoSuchFileError, CorruptedSettingsFileError, FileImportAbortionError
import pickle


class Game:
    def __init__(self):
        self.round = 0
        self.board_size = 10
        self.ships_set_dict = self.calculate_ship_set()
        self.signs = {'empty': '', 'miss': '', 'hit': '', 'ship': ''}
        self.player1 = None
        self.player2 = None

    def calculate_ship_set(self):
        ship_cells = self.board_size * self.board_size * 20 // 100
        sample_ship_cells = 20
        coef = ship_cells // sample_ship_cells
        ship_dict = {
            'четырехпалубный': 1 * coef,
            'трехпалубный': 2 * coef,
            'двухпалубный': 3 * coef,
            'однопалубный': 0 * coef
        }
        ship_dict['однопалубный'] = ship_cells - sum([(len(ship_dict) - i) * x for i, x in enumerate(ship_dict.values())])
        return ship_dict

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
        if answ1 == '1' and answ2 == '1':
            print('Choose an option:\n1.input ships coordinates\n2.upload file\n3.return')
            answ = input()
            while True:
                if answ == '1':
                    print('Player1, input your name')
                    name = self.get_player_name()
                    print(f'{name}, get ready to input your ship coordinates')
                    board, ships = self.prepare_board()
                    self.player1 = Player(name, board, ships, self.signs)
                    print("That's all! Now it's player2 turn!")
                    print('Player2, input your name')
                    name = self.get_player_name()
                    print(f'{name}, get ready to input your ship coordinates')
                    board, ships = self.prepare_board()
                    self.player2 = Player(name, board, ships, self.signs)
                elif answ == '2':
                    print('This option is temporary unavailable!')
                    answ = input()
                    continue
                    # something
                elif answ == '3':
                    return self.greeting()
                else:
                    print('Incorrect input!')
                    answ = input()
        # new p_v_b
        elif answ1 == '1' and answ2 == '2':
            print('Choose an option:\n1.input ships coordinates\n2.upload txt file\n3.return')
            answ = input()
            while True:
                if answ == '1':
                    print('Hello, player1! Get ready to input your ship coordinates')
                    board, ships = self.prepare_board()
                    print('Input your name')
                    name = self.get_player_name()
                    self.player1 = Player(name, board, ships, self.signs)
                    self.player2 = Bot(self.board_size, self.signs)
                    self.player2.init_board()
                    break
                elif answ == '2':
                    try:
                        print('Hello, player1! Get ready to input your filename')
                        board, ships = self._load_coords_from_file()
                    except Exception as ex:
                        print(ex)
                        return self.greeting()
                    else:
                        print('Input your name')
                        name = self.get_player_name()
                        self.player1 = Player(name, board, ships, self.signs)
                        self.player2 = Bot(self.board_size, self.signs)
                        self.player2.init_board()
                        break
                elif answ == '3':
                    return self.greeting()
                else:
                    print('Incorrect input!')
                    answ = input()
        # load p_v_p
        elif answ1 == '2' and answ2 == '1':
            saved_game = self.load_game()
            self.player1 = Player(*saved_game[0])
            self.player2 = Player(*saved_game[1])
            self.round = saved_game[2]

        # load p_v_b
        elif answ1 == '2' and answ2 == '2':
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


    def _load_coords_from_file(self):
        print('WARNING: there will be no content checks. Be extremely accurate.')
        print('File format: plain text, one line - one ship')
        print('Ship description prompt: size x y direction (h/v)')
        print('Input file name')
        filename = input()
        while filename not in listdir():
            print('No such filename!')
            filename = input()
        with open(filename) as file:
            this_board = Board(self.board_size, self.signs)
            this_ships = list()
            for line in file:
                size, x, y, dir = line.split()
                this_board.add_ship(int(x), int(y), dir, int(size))
                this_ships.append(Ship(int(x), int(y), dir, int(size)))
            print('Export complete!')
            self.print_board(this_board)
            print('Is this correct? y/n')
            a = input()
            if a.lower() == 'y':
                return this_board, this_ships
            else:
                raise FileImportAbortionError


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

    def prepare_board(self):
        # нужно создавать доску, впечатывать туда корабли, вместе с аурой
        # аура нужна.т.к. есть проверка запрещающая ставить в непустые клетки
        # таким образом получаем положенный по правилам зазор
        # потом обнулять через replace
        this_board = Board(self.board_size, self.signs)
        this_ships = list()
        for i, ship_type in enumerate(self.ships_set_dict):
            counter = 0
            cur_ship_size = len(self.ships_set_dict) - i
            while counter < self.ships_set_dict[ship_type]:
                print(f'Need to place {self.ships_set_dict[ship_type] - counter} {ship_type}')
                try:
                    self.print_board(this_board)
                    print(f'Choose coordinates for {ship_type} and direction(h/v)')
                    x, y, dir = input().split()
                    this_board.add_ship(int(x), int(y), dir, cur_ship_size)
                except Exception as ex:
                    print(repr(ex))
                else:
                    this_ships.append(Ship(int(x), int(y), dir, cur_ship_size))
                    this_board.draw_aura(this_ships[-1])
                    counter += 1
        ##избавляемся от ауры
        m = this_board.get_map()
        for y in range(len(m)):
            s = ''.join(m[y])
            s = s.replace(self.signs['miss'], self.signs['empty'])
            m[y] = list(s)
        this_board.set_from_matrix(m)
        self.print_board(this_board)
        return this_board, this_ships

    def print_board(self, left: Board, right: Board = None):
        space = ' ' * len(str(self.board_size))
        hor_header = ' ' + space.join([str(x) for x in range(self.board_size + 1)])[1:]
        margin = ' ' * 4
        print(hor_header, end=' ' * (4 - len(str(self.board_size)) + 1))
        if right:
            print(hor_header, end='')
        print()
        for y in range(1, self.board_size + 1):
            print(y, end=' ' * (len(str(self.board_size)) - len(str(y)) + 1))
            print(space.join(left.get_map()[y][1: -1]), end=margin)
            if right:
                print(y, end=' ' * (len(str(self.board_size)) - len(str(y)) + 1))
                print(space.join(right.get_map()[y][1: -1]), end='')
            print()


    def main_loop(self):
        while True:

            self.print_board()
            print('Shoot!')
            print('input x y')
            x, y = self.input_loop()


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
        game.main_loop()
