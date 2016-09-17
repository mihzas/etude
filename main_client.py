#!/usr/bin/env python3

import json
import subprocess
from socket import *

from ui import print_board, get_value_from_user_input

STATE_ERROR = -1
STATE_BLACK_WIN = 2
STATE_WHITE_WIN = 3
STATE_DRAW = 4


if __name__ == '__main__':
    player = input('Player name: ')

    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('', 8888))

    print("Waiting for your opponent")
    colour = s.recv(250)
    print('Your colour is {}'.format(colour.decode('utf-8')))

    while True:
        board = s.recv(1024)
        d = json.loads(board.decode('utf-8'))
        has_turn = d.pop('has_turn', None)
        state = d.pop('state', None)
        subprocess.call('clear')

        if state == STATE_ERROR:
            print('Invalid move')
            print_board(d)
            move = get_value_from_user_input(player)
            s.send(json.dumps(move).encode('utf-8'))
        elif has_turn:
            print_board(d)
            move = get_value_from_user_input(player)
            s.send(json.dumps(move).encode('utf-8'))
        elif state == STATE_DRAW:
            print('Draw')
            break
        elif state == STATE_WHITE_WIN:
            print('White win!!!')
            break
        elif state == STATE_BLACK_WIN:
            print('Black win!!!')
            break
        else:
            print_board(d)
            print('Please waiting for your partner')

    s.close()



