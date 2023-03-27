# Код полу-скопирован полу-спамяти написан.
# Изменения в коде:
#      - вывод доски (параллельно)
#      - добавлено таймслип
#      - очистка доски (очистка в пайчарме не работает почемуто)
#        с командной строки виндоуса очень даже ничего играется.

from random import randint
import time
import os

class BoardExceptions(Exception):
    pass

class BoardOutException(BoardExceptions):
    def __str__(self):
        return "Вне поля"

class BoardUsedException(BoardExceptions):
    def __str__(self):
        return "Клетка занята"

class BoardWrongShipException(BoardExceptions):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, l, V_or_H):
        self.l = l
        self.bow = bow
        self.V_or_H = V_or_H
        self.health = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            d_x = self.bow.x
            d_y = self.bow.y
            if self.V_or_H == 0:
                d_x += i
            elif self.V_or_H == 1:
                d_y += i
            ship_dots.append(Dot(d_x, d_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size
        self.downed_ships = 0
        self.field = [["□"]*size for i in range(size)]
        self.busy = []
        self.ships = []

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

        for i in ship.dots:
            for ix, iy in near:
                cur = Dot(i.x + ix, i.y + iy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "◦"
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "□")
        return res

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.health -= 1
                self.field[d.x][d.y] = "X"
                if ship.health == 0:
                    self.downed_ships += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "◦"
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardExceptions as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue
            x, y = cords
            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
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
        board.begin()
        return board

    def print_two_board(self):
        board_ai = self.ai.board.field
        if self.ai.board.hid:
            for i, I in enumerate(board_ai):
                for e, E in enumerate(I):
                    if E == "■":
                         board_ai[i][e] = "□"
        print("      Пользователь                Компьютер")
        print("      1 2 3 4 5 6       |         1 2 3 4 5 6")
        for i, e in enumerate(self.us.board.field):
           print(*f"  {i + 1}{''.join(e)}   |   {i + 1}{''.join(board_ai[i])}")

    def greet(self):
        print("-------------------------------------------------")
        print("       Приветсвуем вас в игре МОРСКОЙ БОЙ        ")
        print("-------------------------------------------------")
        print(" формат ввода: x y (номер строки, номер столбца) ")

    def loop(self):
        num = 0
        while True:
            self.greet()
            print("-" * 49)
            self.print_two_board()
            if num % 2 == 0:
                print("-" * 49)
                print("Ход пользователя!")
                repeat = self.us.move()
                time.sleep(2)
                os.system("cls")
            else:
                print("-" * 49)
                print("Ходит компьютер!")
                time.sleep(1.5)
                repeat = self.ai.move()
                time.sleep(2.5)
                os.system("cls")
            if repeat:
                num -= 1
            if self.ai.board.downed_ships == 7:
                print("-" * 49)
                print("Пользователь выиграл!")
                break
            if self.us.board.downed_ships == 7:
                print("-" * 49)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.loop()

g = Game()
g.start()