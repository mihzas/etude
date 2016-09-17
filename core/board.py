#! /usr/bin/env python3


from core.pieces import Cell, King, Queen, Rook, Bishop, Horse, Pawn

WHITE = 0
BLACK = 1
SIDE_BOARD = 8


class Board:
    """simple board"""

    def __init__(self):

        self.__board = []
        for i in range(SIDE_BOARD):

            tmp = []
            for j in range(SIDE_BOARD):
                if (i + 1 + j + 1) % 2 == BLACK:
                    tmp.append(Cell(BLACK))
                else:
                    tmp.append(Cell(WHITE))

            self.__board.append(tmp)

        self.__init_board()

    def to_dict(self):
        d = dict()

        d['King'] = []
        d['Queen'] = []
        d['Rook'] = []
        d['Bishop'] = []
        d['Horse'] = []
        d['Pawn'] = []
        d['Cell'] = [Cell(BLACK).get_value(), Cell(WHITE).get_value()]

        for i in range(len(self.__board)):
            for j in range(len(self.__board)):
                if type(self.__board[i][j]) == King:
                    d['King'].append((self.__board[i][j].get_value(), i, j))

                elif type(self.__board[i][j]) == Queen:
                    d['Queen'].append((self.__board[i][j].get_value(), i, j))

                elif type(self.__board[i][j]) == Rook:
                    d['Rook'].append((self.__board[i][j].get_value(), i, j))

                elif type(self.__board[i][j]) == Bishop:
                    d['Bishop'].append((self.__board[i][j].get_value(), i, j))

                elif type(self.__board[i][j]) == Horse:
                    d['Horse'].append((self.__board[i][j].get_value(), i, j))

                elif type(self.__board[i][j]) == Pawn:
                    d['Pawn'].append((self.__board[i][j].get_value(), i, j))

        return d

    def get_cell(self, y, x):
        return self.__board[y][x]

    def destroy(self, y, x):
        if (x + 1 + y + 1) % 2 == BLACK:
            self.__board[y][x] = Cell(BLACK)
        else:
            self.__board[y][x] = Cell(WHITE)

    def move(self, src, dest):
        self.__board[dest.y][dest.x] = self.__board[src.y][src.x]

        if (src.x + 1 + src.y + 1) % 2 == BLACK:
            self.__board[src.y][src.x] = Cell(BLACK)
        else:
            self.__board[src.y][src.x] = Cell(WHITE)

    def count_pieces(self):

        count = 0

        for i in range(SIDE_BOARD):
            for j in range(SIDE_BOARD):
                if type(self.__board[i][j]) != Cell:
                    count += 1

        return count

    def cancel_enpassant(self):

        for i in range(SIDE_BOARD):
            for j in range(SIDE_BOARD):
                if type(self.__board[i][j]) == Pawn and self.__board[i][j].get_enpassant():
                    self.__board[i][j].set_enpassant(False)

    def __init_board(self):
        """Function fills in the board by chessmans"""
        for y in range(SIDE_BOARD):
            self.__board[1][y] = Pawn(BLACK)
            self.__board[6][y] = Pawn(WHITE)

        self.__board[0][4] = King(BLACK)
        self.__board[7][4] = King(WHITE)

        self.__board[0][3] = Queen(BLACK)
        self.__board[7][3] = Queen(WHITE)

        self.__board[0][0], self.__board[0][7] = Rook(BLACK), Rook(BLACK)
        self.__board[7][0], self.__board[7][7] = Rook(WHITE), Rook(WHITE)

        self.__board[0][2], self.__board[0][5] = Bishop(BLACK), Bishop(BLACK)
        self.__board[7][2], self.__board[7][5] = Bishop(WHITE), Bishop(WHITE)

        self.__board[0][1], self.__board[0][6] = Horse(BLACK), Horse(BLACK)
        self.__board[7][1], self.__board[7][6] = Horse(WHITE), Horse(WHITE)


