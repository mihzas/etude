from abc import ABCMeta
from core.logging import LoggingMixIn


WHITE = 0
BLACK = 1


class Cell:

    def __init__(self, colour):
        self._colour = colour

        if colour == BLACK:
            self.__value = '\u25A0'
        else:
            self.__value = '\u25A1'

    def get_value(self):
        return self.__value

    def get_colour(self):
        return self._colour


class Piece(LoggingMixIn, metaclass=ABCMeta):

    def __init__(self, colour, value):
        self._colour = colour
        self._value = value

    def get_value(self):
        return self._value

    def get_colour(self):
        return self._colour

    def make_log(self, src, dest):
        tmp_s = ' ({0}, {1}) --> ({2}, {3})'.format(src.x, src.y, dest.x, dest.y)
        self.write_log(self._short_name + tmp_s)


class King(Piece):

    def __init__(self, colour):
        if colour == BLACK:
            super(King, self).__init__(colour, '\u265A')
        else:
            super(King, self).__init__(colour, '\u2654')

        self._short_name = 'K'


class Queen(Piece):

    def __init__(self, colour):
        if colour == BLACK:
            super(Queen, self).__init__(colour, '\u265B')
        else:
            super(Queen, self).__init__(colour, '\u2655')

        self._short_name = 'Q'


class Rook(Piece):

    def __init__(self, colour):
        if colour == BLACK:
            super(Rook, self).__init__(colour, '\u265C')
        else:
            super(Rook, self).__init__(colour, '\u2656')

        self._short_name = 'R'


class Bishop(Piece):

    def __init__(self, colour):
        if colour == BLACK:
            super(Bishop, self).__init__(colour, '\u265D')
        else:
            super(Bishop, self).__init__(colour, '\u2657')

        self._short_name = 'B'


class Horse(Piece):

    def __init__(self, colour):

        if colour == BLACK:
            super(Horse, self).__init__(colour, '\u265E')
        else:
            super(Horse, self).__init__(colour, '\u2658')

        self._short_name = 'H'


class Pawn(Piece):

    def __init__(self, colour):

        if colour == BLACK:
            super(Pawn, self).__init__(colour, '\u265F')
        else:
            super(Pawn, self).__init__(colour, '\u2659')

        self._short_name = 'P'
        self.__state_enpassant = False

    def get_enpassant(self):
        return self.__state_enpassant

    def set_enpassant(self, state):
        self.__state_enpassant = state



