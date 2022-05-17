from checkers.board import Board
from checkers.engine import Engine
from checkers.piece import Piece
from checkers.const import WHITE, ROWS, BROWN, COLS
from ai.algorithms import minimax


def init_board():
    board_obj = Board()
    board_obj.board = []
    for row in range(ROWS):
        board_obj.board.append([])
        for col in range(COLS):
            board_obj.board[row].append(0)
    return board_obj


def test_minimax_depth_1():
    engine = Engine()
    engine.board = init_board()
    piece = Piece(3, 6, WHITE)
    engine.board.board[3][6] = piece
    piece = Piece(1, 2, BROWN)
    engine.board.board[1][2] = piece
    score, move = minimax(engine, True, 1)
    assert move.board.board[2][7] != 0
    assert move.board.board[3][6] == 0


def test_minimax_depth_2():
    engine = Engine()
    engine.board = init_board()
    piece = Piece(2, 5, WHITE)
    engine.board.board[2][5] = piece
    piece = Piece(6, 1, WHITE)
    engine.board.board[6][1] = piece
    piece = Piece(1, 2, BROWN)
    engine.board.board[1][2] = piece
    score, move = minimax(engine, True, 3)
    assert move.board.board[1][4] != 0 or move.board.board[1][6] != 0


def test_ab_depth_1():
    engine = Engine()
    engine.board = init_board()
    piece = Piece(3, 6, WHITE)
    engine.board.board[3][6] = piece
    piece = Piece(1, 2, BROWN)
    engine.board.board[1][2] = piece
    score, move = minimax(engine, True, 1, True)
    assert move.board.board[2][7] != 0
    assert move.board.board[3][6] == 0


def test_ab_depth_2():
    engine = Engine()
    engine.board = init_board()
    piece = Piece(2, 5, WHITE)
    engine.board.board[2][5] = piece
    piece = Piece(6, 1, WHITE)
    engine.board.board[6][1] = piece
    piece = Piece(1, 2, BROWN)
    engine.board.board[1][2] = piece
    score, move = minimax(engine, True, 3, True)
    assert move.board.board[1][4] != 0 or move.board.board[1][6] != 0




