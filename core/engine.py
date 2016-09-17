"""
Module is dedicated game's engine
"""
from collections import namedtuple
from core.board import SIDE_BOARD, BLACK, WHITE
from core.pieces import Cell
from core.rules import check_move

STATE_ERROR = -1
STATE_CONTINUE = 1
STATE_BLACK_WIN = 2
STATE_WHITE_WIN = 3
STATE_DRAW = 4


class Engine:
    """Entity which controls the game"""
    def __init__(self, board, player1, player2):
        self.__state_move = WHITE
        self.__board = board
        self.__player1 = player1
        self.__player2 = player2
        self.is_enpassant = False
        self.__turn = True
        self.__cache = {'black_king': board.get_cell(0, 4),
                        'white_king': board.get_cell(7, 4)}

    def get_board(self):
        return self.__board

    def try_make_move(self, coord, current_player_colour):

        __Coordinate = namedtuple('Coordinate', 'x y')
        src = __Coordinate(coord['src'][0], coord['src'][1])
        dest = __Coordinate(coord['dest'][0], coord['dest'][1])

        if coord and check_move(src, dest, self.__board, self.__handle_dict, self.__change_is_enpassant, current_player_colour):
            self.__board.move(src, dest)
            self.__switch_enpassant()
            state = self.winning_conditions()

            return state

        return STATE_ERROR

    def winning_conditions(self):

        if not self.__cache.get('black_king', None):
            return STATE_WHITE_WIN

        elif not self.__cache.get('white_king', None):
            return STATE_BLACK_WIN

        elif self.__board.count_pieces() == 2:
            return STATE_DRAW

        return STATE_CONTINUE

    def __switch_enpassant(self):

        if self.is_enpassant and self.__turn:
            self.__board.cancel_enpassant()


        self.__turn = not self.__turn

    def __handle_dict(self, key):
        self.__cache.pop(key)

    def __change_is_enpassant(self, value):
        self.is_enpassant = value
