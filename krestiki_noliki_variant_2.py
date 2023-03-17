win_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

player_1 = []
player_2 = []
pl_1 = "<Игорк 1>", "X"
pl_2 = "<Игорк 2>", "O"

desk = [
    ['-', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-'],
]

desk_numbers = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
]

cells_positions = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 9: [2, 2]}

a = True
pos = []

print("-----------")
print("Правила игры в крестики нолики:")
print("Вводим номер клетки от 1 до 9, куда хотим поставить 'X' или 'O'")
print("Как на сетке внизу")
print("-----------")
for i in desk_numbers:
    print(*[f"{x:>2}" for x in i])
print("-----------")

def check_winner(player):
    for i in win_list:
        if i[0] in player and i[1] in player and i[2] in player:
            return True

def inp_cells(player, pl, pl_):
    c = int(input(f"Клетка {pl} -- "))
    if c < 1 or c > 9:
        print(("Нет такой клетки, выбери от 1 до 9."))
        return inp_cells(player, pl, pl_)
    if c in pos:
        print(("Клетка занята, выберу другую."))
        return inp_cells(player, pl, pl_)
    pos.append(c)
    player.append(c)
    q = cells_positions.get(c)
    desk[q[0]][q[1]] = pl_
    for i in desk:
        print(*[f"{x:>2}" for x in i])

while a:
    inp_cells(player_1, pl_1[0], pl_1[1])

    if check_winner(player_1):
        print(f'{pl_1[0]} ВЫГРАЛ!')
        break

    inp_cells(player_2, pl_2[0], pl_2[1])

    if check_winner(player_2):
        print(f'{pl_2[0]} ВЫИГРАЛ!')
        break
