from random import randint
# Основа построенного кода взята из вебинара по игре "Морской бой"
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

#Добавлены исключения для доски

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Coordinates out of range!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Area already hit!Check your radar"

class BoardWrongShipException(BoardException):
    pass

#Класс для кораблей

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

#Функция для попадания снаряда

    def shooten(self, shot):
        return shot in self.dots

#Класс для игрового поля

class Board:
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["0"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

#Методы добавления корабля на доску

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

#Метод для выстрела

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("HIT!Enemy ship damaged")
                    return False
                else:
                    print("DIRECT HIT!Enemy ship destroyed!!!")
                    return True

        self.field[d.x][d.y] = "."
        print("Negative, you miss!")
        return False

    def begin(self):
        self.busy = []

#Класс игрока

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
            except BoardException as e:
                print(e)

#Класс игрока AI

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Opponents turn: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Your turn, choose target wisely: ").split()

            if len(cords) != 2:
                print("Don't you remember your training?\nEnter 2 coordinates\n")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Don't you remember your training?\nType a number\n")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

#Класс игры

class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

#Метод создания доски, без ошибки None

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

    def greet(self):
        print("\n\n***********************")
        print("Welcome to Battleships!")
        print("***********************\n")
        print(" Input format: x y ")
        print(" x - row number  ")
        print(" y - col number ")

# Игровой цикл

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Your ocean:")
            print(self.us.board)
            print("-" * 20)
            print("Computer ocean:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Your turn!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Computer turn!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("fleet has been destroyed, You wins!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("fleet has been destroyed, Computer wins!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()