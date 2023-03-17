win_list = ([[1, 0, 0], [1, 0, 0], [1, 0, 0]],
            [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
            [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
            [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
            [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
            [[0, 0, 0], [0, 0, 0], [1, 1, 1]],
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
            )

player_1 = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

player_2 = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

desk = [
    ['-', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-'],
]

cells_positions = {1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [1, 0], 5: [1, 1], 6: [1, 2], 7: [2, 0], 8: [2, 1], 9: [2, 2]}

#a = input("Напишите номер квадрата где хотите положить крестик или нолик -- ")
a = True
pos = []

while a:
    b = int(input("wirte player 1 -- "))
    while b in pos:
        b = int(input("wirte other cell -- "))
    q = cells_positions.get(b)
    pos.append(b)
    player_1[q[0]][q[1]] = 1
    desk[q[0]][q[1]] = 'X'
    if player_1 in win_list:
        break

    b = int(input("wirte player 2 -- "))
    while b in pos:
        b = int(input("wirte other cell -- "))
    q = cells_positions.get(b)
    pos.append(b)
    player_2[q[0]][q[1]] = 1
    desk[q[0]][q[1]] = "O"
    if player_2 in win_list:
        break

print("won 1" if player_1 in win_list else "won 2")
#print(list in win_list)
#print(player_2)
#print(q)
