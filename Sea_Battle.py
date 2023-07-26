import random

# Создаем пустое поле 10x10
board_size = 10
board = [["_" for _ in range(board_size)] for _ in range(board_size)]

# Создаем пустое поле 10x10 для противника (ИИ)
enemy_board = [["_" for _ in range(board_size)] for _ in range(board_size)]


# Функция для отображения поля
def print_board(board_or_enemy_board):
    print(" ", end=" ")
    for i in range(board_size):
        print(i, end=" ")
    print()
    for i in range(board_size):
        print(i, end=" ")
        for j in range(board_size):
            print(board_or_enemy_board[i][j], end=" ")
        print()


# Функция для проверки валидности координат
def is_valid_coordinate(x, y):
    return 0 <= x < board_size and 0 <= y < board_size


# Функция для расстановки кораблей
def place_ships():
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Размеры кораблей
    for ship_length in ships:
        if ship_length != 1:
            while True:
                print_board(board)
                print(f"Установите {ship_length} палубный корабль")
                try:
                    x = int(input("Введите координату X (от 0 до 9): "))
                    y = int(input("Введите координату Y (от 0 до 9): "))
                except ValueError:
                    print("Неверный символ. Введите число.")
                    continue
                if is_valid_coordinate(x, y):
                    orientation = input("Введите ориентацию (вправо(r)/влево(l)/вниз(d)/вверх(u)/): ")
                    if orientation == 'd' and x + ship_length <= len(board):
                        ship_coordinates = [(x + i, y) for i in range(ship_length)]
                    elif orientation == 'r' and y + ship_length <= len(board):
                        ship_coordinates = [(x, y + i) for i in range(ship_length)]
                    elif orientation == 'u' and -1 <= x - ship_length:
                        ship_coordinates = [(x - i, y) for i in range(ship_length)]
                    elif orientation == 'l' and -1 <= y - ship_length:
                        ship_coordinates = [(x, y - i) for i in range(ship_length)]
                    else:
                        print("Неверная ориентация. Попробуйте снова.")
                        continue

                    # Проверяем, что вокруг корабля все ячейки пустые и нет пересечения с другими кораблями
                    overlap = False
                    for coord in ship_coordinates:
                        try:
                            if board[coord[0]][coord[1]] == '*' or \
                                    board[coord[0] + 1][coord[1]] == '*' or \
                                    board[coord[0]][coord[1] + 1] == '*' or \
                                    board[coord[0]][coord[1] - 1] == '*' or \
                                    board[coord[0] - 1][coord[1]] == '*' or \
                                    board[coord[0] - 1][coord[1] - 1] == '*' or \
                                    board[coord[0] - 1][coord[1] + 1] == '*' or \
                                    board[coord[0] + 1][coord[1] + 1] == '*' or \
                                    board[coord[0] + 1][coord[1] - 1] == '*':
                                overlap = True
                                break
                        except IndexError:
                            continue

                    if not overlap:
                        break
                    else:
                        print("Корабль пересекается с другими кораблями или вокруг корабля " + \
                              "есть занятые позиции. Попробуйте снова.")

                else:
                    print("Неверные координаты. Попробуйте снова.")

            # Размещаем корабль на игровом поле
            for coord in ship_coordinates:
                board[coord[0]][coord[1]] = '*'

        else:
            while True:
                print_board(board)
                print(f"Установите {ship_length} палубный корабль")
                x = int(input("Введите координату X (от 0 до 9): "))
                y = int(input("Введите координату Y (от 0 до 9): "))
                if is_valid_coordinate(x, y):
                    ship_coordinates = [(x, y)]

                # Проверяем, что вокруг корабля все ячейки пустые и нет пересечения с другими кораблями
                overlap = False
                for coord in ship_coordinates:
                    try:
                        if board[coord[0]][coord[1]] == '*' or \
                                board[coord[0] + 1][coord[1]] == '*' or \
                                board[coord[0]][coord[1] + 1] == '*' or \
                                board[coord[0]][coord[1] - 1] == '*' or \
                                board[coord[0] - 1][coord[1]] == '*' or \
                                board[coord[0] - 1][coord[1] - 1] == '*' or \
                                board[coord[0] - 1][coord[1] + 1] == '*' or \
                                board[coord[0] + 1][coord[1] + 1] == '*' or \
                                board[coord[0] + 1][coord[1] - 1] == '*':
                            overlap = True
                            break
                    except IndexError:
                        continue

                if not overlap:
                    break
                else:
                    print("Корабль пересекается с другими кораблями или вокруг корабля " + \
                          "есть занятые позиции. Попробуйте снова.")

            # Размещаем корабль на игровом поле
            for coord in ship_coordinates:
                board[coord[0]][coord[1]] = '*'

    print("Ваши корабли успешно расставлены")
    print("Начинаем игру!")


# Функция для расстановки кораблей на поле ИИ
def place_enemy_ships():
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for ship_size in ships:
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                x = random.randint(0, board_size - 1)
                y = random.randint(0, board_size - ship_size)
                ship_coordinates = [(x, y + i) for i in range(ship_size)]
                overlap = False
                for coord in ship_coordinates:
                    try:
                        if enemy_board[coord[0]][coord[1]] == "■" or \
                                enemy_board[coord[0] + 1][coord[1]] == "■" or \
                                enemy_board[coord[0]][coord[1] + 1] == "■" or \
                                enemy_board[coord[0]][coord[1] - 1] == "■" or \
                                enemy_board[coord[0] - 1][coord[1]] == "■" or \
                                enemy_board[coord[0] - 1][coord[1] - 1] == "■" or \
                                enemy_board[coord[0] - 1][coord[1] + 1] == "■" or \
                                enemy_board[coord[0] + 1][coord[1] + 1] == "■" or \
                                enemy_board[coord[0] + 1][coord[1] - 1] == "■":
                            overlap = True
                            break
                    except IndexError:
                        continue

                if not overlap:
                    break

            else:
                x = random.randint(0, board_size - ship_size)
                y = random.randint(0, board_size - 1)
                ship_coordinates = [(x + i, y) for i in range(ship_size)]
                overlap = False
                for coord in ship_coordinates:
                    try:
                        if enemy_board[coord[0]][coord[1]] == "■" or \
                                enemy_board[coord[0] + 1][coord[1]] == "■" or \
                                enemy_board[coord[0]][coord[1] + 1] == "■" or \
                                enemy_board[coord[0]][coord[1] - 1] == "■" or \
                                enemy_board[coord[0] - 1][coord[1]] == "■" or \
                                enemy_board[coord[0] - 1][coord[1] - 1] == "■" or \
                                enemy_board[coord[0] - 1][coord[1] + 1] == "■" or \
                                enemy_board[coord[0] + 1][coord[1] + 1] == "■" or \
                                enemy_board[coord[0] + 1][coord[1] - 1] == "■":
                            overlap = True
                            break
                    except IndexError:
                        continue

                if not overlap:
                    break

        if orientation == 'horizontal' and y + ship_size <= board_size:
            if all(cell == "_" for cell in enemy_board[x][y:y + ship_size]):
                enemy_board[x][y:y + ship_size] = ["■"] * ship_size
        elif orientation != 'horizontal' and x + ship_size <= board_size:
            if all(enemy_board[i][y] == "_" for i in range(x, x + ship_size)):
                for i in range(x, x + ship_size):
                    enemy_board[i][y] = "■"


# Функция для хода игрока
def player_turn():
    while True:
        try:
            if all(all(cell != "■" for cell in row) for row in enemy_board):
                break
            x = int(input("Введите координату X (от 0 до 9): "))
            y = int(input("Введите координату Y (от 0 до 9): "))
            if is_valid_coordinate(x, y):
                if enemy_board[x][y] == "■":
                    print("Попадание!")
                    enemy_board[x][y] = 'X'
                    print_board([["_" if cell == "■" else cell for cell in row] for row in enemy_board])
                    continue
                elif enemy_board[x][y] == "_":
                    print("Мимо!")
                    enemy_board[x][y] = 'O'
                    break
                elif enemy_board[x][y] == "X" or "O":
                    print("Вы уже совершали ход в эту позицию. Попробуйте другую.")
                    continue
            else:
                print("Неверные координаты. Попробуйте снова.")

        except ValueError:
            print("Неверный ввод. Попробуйте снова.")


# Функция для хода компьютера
def computer_turn():
    while True:
        if all(all(cell != "*" for cell in row) for row in board):
            break
        x = random.randint(0, board_size - 1)
        y = random.randint(0, board_size - 1)
        if board[x][y] == '*':
            print("Компьютер попал!")
            board[x][y] = 'X'

            # Проверка соседних позиций для хода ИИ
            try:
                if board[[x + 1] in range(0, board_size - 1)][[y] in range(0, board_size - 1)] and \
                        board[x + 1][y] == '*':
                    board[x + 1][y] = "X"
                    if board[x + 1][y] == "*" and board[x + 2][y] == "*" and \
                            board[[x + 2] in range(0, board_size - 1)][[y] in range(0, board_size - 1)]:
                        board[x + 2][y] = "X"
                        if board[x + 2][y] == "*" and board[x + 3][y] == "*" and \
                                board[[x + 3] in range(0, board_size - 1)][[y] in range(0, board_size - 1)]:
                            board[x + 3][y] = "X"
                            continue
                elif board[[x + 1] in range(0, board_size - 1)][[y] in range(0, board_size - 1)] and \
                        board[x + 1][y] == '_':
                    board[x + 1][y] = "O"
                    break
                elif board[[x] in range(0, board_size - 1)][[y + 1] in range(0, board_size - 1)] and \
                        board[x][y + 1] == '*':
                    board[x][y + 1] = "X"
                    if board[x][y + 1] == "*" and board[x][y + 2] == "*" and \
                            board[[x] in range(0, board_size - 1)][[y + 2] in range(0, board_size - 1)]:
                        board[x][y + 2] = "X"
                        if board[x][y + 2] == "*" and board[x][y + 3] == "*" and \
                                board[[x] in range(0, board_size - 1)][[y + 3] in range(0, board_size - 1)]:
                            board[x][y + 3] = "X"
                            continue
                elif board[[x] in range(0, board_size - 1)][[y + 1] in range(0, board_size - 1)] and \
                        board[x][y + 1] == '_':
                    board[x][y + 1] = "O"
                    break
                elif board[[x - 1] in range(0, board_size - 1)][[y] in range(0, board_size - 1)] and \
                        board[x - 1][y] == '*':
                    board[x - 1][y] = "X"
                    if board[x - 1][y] == "*" and board[x - 2][y] == "*" and \
                            board[[x - 2] in range(0, board_size - 1)][[y] in range(0, board_size - 1)]:
                        board[x - 2][y] = "X"
                        if board[x - 2][y] == "*" and board[x - 3][y] == "*" and \
                                board[[x - 3] in range(0, board_size - 1)][[y] in range(0, board_size - 1)]:
                            board[x - 3][y] = "X"
                            continue
                elif board[[x - 1] in range(0, board_size - 1)][[y] in range(0, board_size - 1)] and \
                        board[x - 1][y] == '_':
                    board[x - 1][y] = "O"
                    break
                elif board[[x] in range(0, board_size - 1)][[y - 1] in range(0, board_size - 1)] and \
                        board[x][y - 1] == '*':
                    board[x][y - 1] = "X"
                    if board[x][y - 1] == "*" and board[x][y - 2] == "*" and \
                            board[[x] in range(0, board_size - 1)][[y - 2] in range(0, board_size - 1)]:
                        board[x][y - 2] = "X"
                        if board[x][y - 2] == "*" and board[x][y - 3] == "*" and \
                                board[[x] in range(0, board_size - 1)][[y - 3] in range(0, board_size - 1)]:
                            board[x][y - 3] = "X"
                            continue
                elif board[[x] in range(0, board_size - 1)][[y - 1] in range(0, board_size - 1)] and \
                        board[x][y - 1] == '_':
                    board[x][y - 1] = "O"
                    break
            except IndexError:
                pass
        elif board[x][y] == '_':
            print("Компьютер промахнулся!")
            board[x][y] = 'O'
            break
        elif board[x][y] == "X" or "O":
            continue


# Функция для автоматической расстановки кораблей на поле игрока
def place_ships_auto():
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for ship_size in ships:
        while True:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                x = random.randint(0, board_size - 1)
                y = random.randint(0, board_size - ship_size)
                ship_coordinates = [(x, y + i) for i in range(ship_size)]
                overlap = False
                for coord in ship_coordinates:
                    try:
                        if board[coord[0]][coord[1]] == '*' or \
                                board[coord[0] + 1][coord[1]] == '*' or \
                                board[coord[0]][coord[1] + 1] == '*' or \
                                board[coord[0]][coord[1] - 1] == '*' or \
                                board[coord[0] - 1][coord[1]] == '*' or \
                                board[coord[0] - 1][coord[1] - 1] == '*' or \
                                board[coord[0] - 1][coord[1] + 1] == '*' or \
                                board[coord[0] + 1][coord[1] + 1] == '*' or \
                                board[coord[0] + 1][coord[1] - 1] == '*':
                            overlap = True
                            break
                    except IndexError:
                        continue

                if not overlap:
                    break

            else:
                x = random.randint(0, board_size - ship_size)
                y = random.randint(0, board_size - 1)
                ship_coordinates = [(x + i, y) for i in range(ship_size)]
                overlap = False
                for coord in ship_coordinates:
                    try:
                        if board[coord[0]][coord[1]] == '*' or \
                                board[coord[0] + 1][coord[1]] == '*' or \
                                board[coord[0]][coord[1] + 1] == '*' or \
                                board[coord[0]][coord[1] - 1] == '*' or \
                                board[coord[0] - 1][coord[1]] == '*' or \
                                board[coord[0] - 1][coord[1] - 1] == '*' or \
                                board[coord[0] - 1][coord[1] + 1] == '*' or \
                                board[coord[0] + 1][coord[1] + 1] == '*' or \
                                board[coord[0] + 1][coord[1] - 1] == '*':
                            overlap = True
                            break
                    except IndexError:
                        continue

                if not overlap:
                    break

        for coord in ship_coordinates:
            board[coord[0]][coord[1]] = '*'

    print("Ваши корабли успешно расставлены")
    print("Начинаем игру!")


# Цикл выбора расстановки кораблей на поле игрока
while True:
    choose = input("Выберите способ расстановки флота автоматически(a) или самостоятельно(s):")
    if choose == "s":
        place_ships()  # Расставляем корабли
        break
    elif choose == "a":
        place_ships_auto()
        break
    else:
        print("Неверный символ. Повторите попытку.")

# Расставляем корабли на поле ИИ
place_enemy_ships()

# Игровой цикл
while True:
    print("Ваше поле:")
    print_board(board)
    print("Поле противника:")
    print_board([["_" if cell == "■" else cell for cell in row] for row in enemy_board])
    print("Ход игрока:")
    player_turn()

    # Проверяем, выиграл ли игрок
    if all(all(cell != "■" for cell in row) for row in enemy_board):
        print("Поздравляем! Вы выиграли!")
        print_board([["_" if cell == "■" else cell for cell in row] for row in enemy_board])
        break

    print("Ход компьютера:")
    computer_turn()

    # Проверяем, выиграл ли компьютер
    if all(all(cell != "*" for cell in row) for row in board):
        print("Компьютер выиграл. Попробуйте еще раз!")
        print_board(board)
        break
