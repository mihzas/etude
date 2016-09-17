from collections import namedtuple


SIDE_BOARD = 8
BLACK = 1
WHITE = 0


__Coordinate = namedtuple('Coordinate', 'x y')
__letters = namedtuple('_', 'a b c d e f g h')(0, 1, 2, 3, 4, 5, 6, 7)


def get_value_from_user_input(player):

    while True:
        try:
            print(player)
            src = input('Input your move here: ')
            src_y = 8 - int(src[1])

            if hasattr(__letters, src[0]):
                src_x = getattr(__letters, src[0])
            else:
                print('Invalid value')
                continue

            src = __Coordinate(src_x, src_y)

            dest = input('Finish your moving here: ')
            dest_y = 8 - int(dest[1])

            if hasattr(__letters, dest[0]):
                dest_x = getattr(__letters, dest[0])
            else:
                print('Invalid value')
                continue

            dest = __Coordinate(dest_x, dest_y)
            break

        except Exception:
            continue

    return {'src': src, 'dest': dest}


def print_board(dict_figures):
    board = __create_board(dict_figures.pop('Cell'))
    __fill_in_board_with_figures(dict_figures, board)
    s = __create_str(board)

    print(s)


def __create_board(cells):
    board = []

    for i in range(SIDE_BOARD):

        tmp = []
        for j in range(SIDE_BOARD):
            if (i + 1 + j + 1) % 2 == BLACK:
                tmp.append(cells[0])
            else:
                tmp.append(cells[1])

        board.append(tmp)

    return board


def __fill_in_board_with_figures(dict_figures, board):
    for k in dict_figures.keys():
        for t in dict_figures[k]:
            board[t[1]][t[2]] = t[0]


def __create_str(board):
    s = ''

    for i in range(len(board)):
        for j in range(len(board)):
            s += str(board[i][j])
        s += '\n'

    return s




