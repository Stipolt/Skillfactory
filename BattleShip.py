from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Move outside the board"


class BoardRepeatedDotException(BoardException):
    def __str__(self):
        return "The move is repeated"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, f_dot, length, direct):
        self.length = length
        self.f_dot = f_dot
        self.direct = direct
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            x_cord = self.f_dot.x
            y_cord = self.f_dot.y

            if self.direct == 0:
                x_cord += i

            elif self.direct == 1:
                y_cord += i

            ship_dots.append(Dot(x_cord, y_cord))

        return ship_dots

    def is_shoot(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.ships = []
        self.busy = []
        self.count = 0

        self.field = [["◌"] * size for i in range(size)]

    def __str__(self):
        board_show = ""
        board_show += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, value in enumerate(self.field):
            board_show += f"\n{i + 1} | " + " | ".join(value) + " | "

        if self.hid:
            board_show = board_show.replace("◆", "◌")
        return board_show

    def add_ship(self, ship):
        for cor in ship.dots:
            if self.out(cor) or cor in self.busy:
                raise BoardWrongShipException()
        for cor in ship.dots:
            self.field[cor.x][cor.y] = "◆"
            self.busy.append(cor)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        around = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in ship.dots:
            for ix, iy in around:
                a_dot = Dot(i.x + ix, i.y + iy)
                if not(self.out(a_dot)) and a_dot not in self.busy:
                    if verb:
                        self.field[a_dot.x][a_dot.y] = "◦"
                    self.busy.append(a_dot)

    def out(self, cor):
        return not ((0 <= cor.x < self.size) and (0 <= cor.y < self.size))

    def shot(self, cor):

        if self.out(cor):
            raise BoardOutException()

        if cor in self.busy:
            raise BoardRepeatedDotException()

        self.busy.append(cor)

        for ship in self.ships:
            if ship.is_shoot(cor):
                ship.lives -= 1
                self.field[cor.x][cor.y] = "⊗"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("You destroyed the ship")
                    return False
                else:
                    print("Hit, move again")
                    return True

        self.field[cor.x][cor.y] = "◦"
        print("miss")
        return False

    def reset(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError

    def move(self):
        while True:
            try:
                shoot = self.ask()
                shoot_again = self.enemy.shot(shoot)
                return shoot_again
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        cor = Dot(randint(0, 5), randint(0, 5))
        print(f'{cor.x + 1} {cor.y + 1}')
        return cor


class User(Player):
    def ask(self):
        while True:
            cords = input("Enter a two cord: ").split()

            if len(cords) != 2:
                print("two cord's!")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Input a numbers ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        player_ = self.random_board()
        ai_ = self.random_board()
        ai_.hid = True

        self.ai = AI(ai_, player_)
        self.us = User(player_, ai_)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.reset()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print(f'Welcome to the BattleShip GAME\n'
              f'   to move input a two cord\n'
              f'    x - row,   y - column'
              f'\n'
              f'\n')

    def loop(self):
        num = 0
        while True:
            print("Your board:")
            print(self.us.board)
            print("\n")
            print("AI Board:")
            print(self.ai.board)
            print("\n")
            if num % 2 == 0:
                print("Your move")
                repeat = self.us.move()
            else:
                print("AI move")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("\n")
                print("You win!!!")
                break

            if self.us.board.count == 7:
                print("\n")
                print("AI is win(((")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()
