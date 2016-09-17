from core.board import SIDE_BOARD, BLACK, WHITE
from core.pieces import *


def check_move(src, dest, board, handle_dict, change_enpassant, current_player_colour):
    return __validate(src, dest, board, handle_dict, change_enpassant, current_player_colour)


def __validate(src, dest, board, handle_dict, change_enpassant, current_player_colour):
    if src.x < 0 or src.y < 0 or dest.x >= SIDE_BOARD or dest.y >= SIDE_BOARD:
        return False

    chessman_type_src = type(board.get_cell(src.y, src.x))
    chessman_type_dest = type(board.get_cell(dest.y, dest.x))
    chessman_colour_src = board.get_cell(src.y, src.x).get_colour()
    chessman_colour_dest = board.get_cell(dest.y, dest.x).get_colour()

    result = None

    if chessman_colour_src != current_player_colour:
        result = False
    elif chessman_type_src == Cell:
        result = False
    elif chessman_colour_src == chessman_colour_dest and chessman_type_dest != Cell:
        result = False
    elif chessman_type_src == Pawn:
        result = __check_move_pawn(src, dest, chessman_colour_src, chessman_colour_dest, board, change_enpassant)
    elif chessman_type_src == Queen:
        result = __check_move_queen(src, dest, board)
    elif chessman_type_src == King:
        result = __check_move_king(src, dest, board)
    elif chessman_type_src == Rook:
        result = __check_move_rook(src, dest, board)
    elif chessman_type_src == Bishop:
        result = __check_move_bishop(src, dest, board)
    elif chessman_type_src == Horse:
        result = __check_move_horse(src, dest, board)

    if result and chessman_type_dest == King:
        if chessman_colour_dest:
            handle_dict('black_king')
        else:
            handle_dict('white_king')

        return True

    return result


def __check_move_pawn(src, dest, colour_src, colour_dest, board, change_enpassant):
    if colour_src == BLACK:
        if src.y == 1 and dest.y - src.y <= 2 and\
                        type(board.get_cell(src.y+1, src.x)) == Cell:

            board.get_cell(src.y, src.x).make_log(src, dest)
            board.get_cell(src.y, src.x).set_enpassant(True)
            change_enpassant(True)
            return True

        elif src.y > 1 and dest.y - src.y == 1 and src.x == dest.x:

            board.get_cell(src.y, src.x).make_log(src, dest)
            board.get_cell(src.y, src.x).set_enpassant(False)
            return True

        elif src.y == 4 and dest.y == 5:

            if type(board.get_cell(src.y, src.x + 1)) == Pawn and board.get_cell(src.y, src.x + 1).get_colour() == WHITE\
                    and board.get_cell(src.y, src.x + 1).get_enpassant():
                board.destroy(src.y, src.x+1)
                return True

            if type(board.get_cell(src.y, src.x - 1)) == Pawn and board.get_cell(src.y, src.x - 1).get_colour() == WHITE\
                    and board.get_cell(src.y, src.x - 1).get_enpassant():
                board.destroy(src.y, src.x-1)
                return True

        elif colour_dest == WHITE and dest.y == src.y + 1 and abs(dest.x - src.x) == 1:

            board.get_cell(src.y, src.x).make_log(src, dest)
            board.get_cell(src.y, src.x).set_enpassant(False)
            return True

    elif colour_src == WHITE:
        if src.y == 6 and src.y - dest.y <= 2 and\
                        type(board.get_cell(src.y - 1, src.x)) == Cell:

            board.get_cell(src.y, src.x).make_log(src, dest)
            board.get_cell(src.y, src.x).set_enpassant(True)
            change_enpassant(True)
            return True

        elif src.y < 6 and src.y - dest.y == 1 and src.x == dest.x:
            board.get_cell(src.y, src.x).make_log(src, dest)
            board.get_cell(src.y, src.x).set_enpassant(False)
            return True

        elif src.y == 3 and dest.y == 2:

            if type(board.get_cell(src.y, src.x + 1)) == Pawn and\
                board.get_cell(src.y, src.x + 1).get_colour() == BLACK and board.get_cell(src.y, src.x + 1).get_enpassant():
                        board.destroy(src.y, src.x + 1)
                        return True

            if type(board.get_cell(src.y, src.x - 1)) == Pawn and board.get_cell(src.y, src.x - 1).get_colour() == BLACK\
                and board.get_cell(src.y, src.x - 1).get_enpassant():
                        board.destroy(src.y, src.x - 1)
                        return True

        elif colour_dest == BLACK and dest.y == src.y - 1 and abs(dest.x - src.x) == 1:
            board.get_cell(src.y, src.x).make_log(src, dest)
            board.get_cell(src.y, src.x).set_enpassant(False)
            return True

    return False


def __check_move_queen(src, dest, board):
    return __check_move_rook(src, dest, board) or __check_move_bishop(src, dest, board)


def __check_move_king(src, dest, board):
    if abs(src.x - dest.x) == 1 and abs(src.y - dest.y) == 1:
        board.get_cell(src.y, src.x).make_log(src, dest)
        return True
    elif (abs(src.x - dest.x) == 1 and src.y == dest.y) or \
            (src.x == dest.x and abs(src.y - dest.y) == 1):
        board.get_cell(src.y, src.x).make_log(src, dest)
        return True

    return False


def __check_move_rook(src, dest, board):
    if src.x == dest.x:
        if src.y > dest.y:
            for i in range(src.y-1, dest.y, -1):
                if type(board.get_cell(i, src.x)) != Cell:
                    return False

        else:
            for i in range(src.y+1, dest.y):
                if type(board.get_cell(i, src.x)) != Cell:
                    return False

        board.get_cell(src.y, src.x).make_log(src, dest)
        return True

    elif src.y == dest.y:
        if src.x > dest.x:
            for i in range(src.x-1, dest.x, -1):
                if type(board.get_cell(src.y, i)) != Cell:
                    return False

        else:
            for i in range(src.x+1, dest.x):
                if type(board.get_cell(src.y, i)) != Cell:
                    return False

        board.get_cell(src.y, src.x).make_log(src, dest)
        return True

    return False


def __check_move_bishop(src, dest, board):
    if dest.x + dest.y > src.x + src.y:
        tmp = src.x + 1
        for i in range(src.y+1, dest.y):
            if type(board.get_cell(i, tmp)) != Cell:
                return False

            tmp += 1

    elif dest.x + dest.y < src.x + src.y:
        tmp = src.x - 1
        for i in range(src.y-1, dest.y, -1):
            if type(board.get_cell(i, tmp)) != Cell:
                return False

            tmp -=1

    elif src.y < dest.y:

        tmp = src.x - 1

        for i in range(src.y+1, dest.y):
            if type(board.get_cell(i, tmp)) != Cell:
                return False
            tmp -= 1

    elif src.y > dest.y:

        tmp = src.x + 1

        for i in range(src.y-1, dest.y, -1):
            if type(board.get_cell(i, tmp)) != Cell:
                return False
            tmp += 1

    board.get_cell(src.y, src.x).make_log(src, dest)
    return True


def __check_move_horse(src, dest, board):
    dx = abs(src.x - dest.x)
    dy = abs(src.y - dest.y)

    if dx == 1 and dy == 2 or dx == 2 and dy == 1:
        board.get_cell(src.y, src.x).make_log(src, dest)
        return True

    return False
