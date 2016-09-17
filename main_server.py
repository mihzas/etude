#! /usr/bin/python3

from socket import *
import json
import threading

from core.board import Board, WHITE, BLACK
from core.engine import Engine, STATE_BLACK_WIN, STATE_WHITE_WIN, STATE_DRAW, STATE_CONTINUE, STATE_ERROR


def game(pl1, adr1, pl2, adr2):

    has_turn = {'has_turn': 1}
    pl1.send('black'.encode('utf-8'))
    pl2.send('white'.encode('utf-8'))

    engine = Engine(Board(), player1=BLACK, player2=WHITE)

    tmp_dict = engine.get_board().to_dict()
    pl1.send(json.dumps(tmp_dict).encode('utf-8'))
    tmp_dict.update(has_turn)
    pl2.send(json.dumps(tmp_dict).encode('utf-8'))

    order_turn = True
    game_state = True
    
    while game_state:
        game_state, order_turn = interact_with_client(order_turn, has_turn, engine)


def interact_with_client(order_turn, has_turn, engine):

    if order_turn:
        answer = json.loads(pl2.recv(1024).decode('utf-8'))
        state = engine.try_make_move(answer, WHITE)
        print('Send request to {} socket'.format(order_turn))
    else:
        answer = json.loads(pl1.recv(1024).decode('utf-8'))
        state = engine.try_make_move(answer, BLACK)
        print('Send request to {} socket'.format(order_turn))

    if state == STATE_CONTINUE:
        if order_turn:
            tmp_dict = engine.get_board().to_dict()
            pl2.send(json.dumps(tmp_dict).encode('utf-8'))
            tmp_dict.update(has_turn)
            pl1.send(json.dumps(tmp_dict).encode('utf-8'))
        else:
            tmp_dict = engine.get_board().to_dict()
            pl1.send(json.dumps(tmp_dict).encode('utf-8'))
            tmp_dict.update(has_turn)
            pl2.send(json.dumps(tmp_dict).encode('utf-8'))
        order_turn = not order_turn
        return True, order_turn

    elif state == STATE_ERROR:
        if order_turn:
            tmp_dict = engine.get_board().to_dict()
            pl1.send(json.dumps(tmp_dict).encode('utf-8'))
            tmp_dict.update(has_turn)
            tmp_dict.update({'state': state})
            pl2.send(json.dumps(tmp_dict).encode('utf-8'))
        else:
            tmp_dict = engine.get_board().to_dict()
            pl2.send(json.dumps(tmp_dict).encode('utf-8'))
            tmp_dict.update(has_turn)
            tmp_dict.update({'state': state})
            pl1.send(json.dumps(tmp_dict).encode('utf-8'))

        return True, order_turn

    else:
        tmp_dict = engine.get_board().to_dict()
        tmp_dict.update({'state': state})
        pl2.send(json.dumps(tmp_dict).encode('utf-8'))
        pl1.send(json.dumps(tmp_dict).encode('utf-8'))
        return False, order_turn


if __name__ == '__main__':

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 8888))

    s.listen(5)

    pl1, adr1 = s.accept()
    print('First player connect to server')

    pl2, adr2 = s.accept()
    print('Second player connect to server')

    s.close()

    t = threading.Thread(target=game, args=(pl1, adr1, pl2, adr2))
    t.start()





