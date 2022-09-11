def welcome():
    print("             XO XO XO!!!\n"
          "Welcome to the greatest game - tic tac toe\n"
          '    To move, enter two coordinates:\n'
          '       X(1) - row, Y(2) - column\n'
          "             Move of 'X'")


def next_turn():
    while True:
        coord = list(map(int, (input("Enter a nums: ").split())))

        if len(coord) != 2:
            print("Enter two num again with 'SPACE'")
            continue

        x = coord[0]
        y = coord[1]


        if len(coord) < 2:
            print("Enter two num again")
            continue

        if x > 2 or y > 2 or x < 0 or y < 0:
            print("Num is out of range!!!")  # condition for input numbers
            continue

        if field[x][y] != "-":
            print("field is busy, pick another)")
            continue

        return x, y


def field_():
    print ("     0    1    2")
    for i in range(3):
        print(f" {i} {field[i]}")
    return field


def win():
    win_list = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)), ((0, 0), (1, 1), (2, 2)), ((0,2), (1, 1), (0, 2)))
    for num_of_win in win_list:
        cordinates = []
        for w in num_of_win:
            cordinates.append(field[w[0]][w[1]])
        if cordinates == ["X", "X", "X"]:
            print('*** Win X ***')
            return True
        elif cordinates == ["O","O","O"]:
            print('Win O')
            return True
    return False


welcome()
field = [["-","-","-"] for i in range(3)]
count = 0
while True:
    field_()                        #Draw field
    count += 1                      #Count the moves
    x, y = next_turn()              #function taking position
    if count % 2 == 1:              #swap X or O
        field[x][y] = "X"
        print("    Move of 'O'")
    else:
        field[x][y] = "O"
        print("    Move of 'X'")

    if win():                       #win condition
        break

    if count == 9:                  #draw condition
        print(" * DRAW * ")
        break