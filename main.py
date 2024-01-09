class Game:
    def __init__(self):
        self.round = 0
        self.board_size = 10
        self.signs = {'empty': '_', 'miss': '.', 'hit': 'x'}
        self.player1 = None
        self.player2 = None


    def greeting(self):
        print('Welcome to warships battle!')
        print('Choose an option:\n1.new game\n2.load game\n3.exit')
        answ = input()
        while True:
            if answ == '1':
                return self.new_game()
            elif answ == '2':
                return self.load_game()
            elif answ == '3':
                print('Goodbye!')
                break
            else:
                print('Incorrect input!')
                answ = input()


    def new_game(self):
        print('Choose an option:\n1.player vs player\n2.player vs bot\n3.return')
        answ = input()
        while True:
            if answ == '1':
                return self.p_v_p()
            elif answ == '2':
                return self.p_v_b()
            elif answ == '3':
                return self.greeting()
            else:
                print('Incorrect input!')
                answ = input()

    def p_v_p(self):
        name1 = self.get_player_name(1)


    def get_player_name(self, n):
        print(f'Hello, player{n}! Name yourself')
        answ = input()
        while True:
            print('Is this correct?')
            print(answ)
            print('If ok - just hit Enter. Else - input again')
            answ_copy = answ
            answ = input()
            if not answ:
                return answ_copy

    def ship_position_mode(self):
        print('Choose an option:\n1.input ships coordinates\n2.upload file\n3.return')
        answ = input()
        while True:
            if answ == '1':
                return self.input_loop()
            elif answ == '2':
                return self.upload_file()
            elif answ == '3':
                return self.greeting()
            else:
                print('Incorrect input!')
                answ = input()


    def upload_file(self):
        print('Input file name')
        filename = input()
        while filename not in os.listdir():
            print('No such filename!')
            filename = input()
        file = open(filename)
        sells = [x.split() for x in file.readlines()]
        self.player_board = Board(size=len(sells))
        self.player_board.map = sells
        return 'result'


    def load_game(self):
        pass




    def input_loop(self):
        while True:
            try:
                x, y = map(int, input().split())
                break
            except Exception:
                print('Wrong coordinates')
        return x, y

    def print_board(self):
        space = ' ' * len(str(self.size))
        hor_header = ' ' + space.join([str(x) for x in range(self.size + 1)])[1:]
        margin = ' ' * 4
        print(hor_header, end=' ' * (4 - len(str(self.size)) + 1))
        print(hor_header)
        for y in range(1, self.size + 1):
            print(y, end=' ' * (len(str(self.size)) - len(str(y)) + 1))
            print(space.join(self.player_board.map[y][1: -1]), end=margin)
            print(y, end=' ' * (len(str(self.size)) - len(str(y)) + 1))
            print(space.join(self.bot_visble_board.map[y][1: -1]))


    # def save_to_file(self, filename):
    #     file = open(filename, 'w')
    #     for line in self.map:
    #         file.write(line)
    #         file.write('\n')
    #     file.close()



    def main_loop(self):
        while True:
            self.print_board()
            print('Shoot!')
            print('input x y')
            x, y = self.input_loop()


if __name__ == '__main__':
    game = Game()
    game.greeting()