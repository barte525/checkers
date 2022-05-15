from checkers.board import Board
from checkers.engine import Engine
from checkers.piece import Piece
from checkers.const import WHITE, ROWS, BROWN, COLS
from ai.evaluations import Evaluator
from ai.mini_max import minimax


def init_board():
    board_obj = Board()
    board_obj.board = []
    for row in range(ROWS):
        board_obj.board.append([])
        for col in range(COLS):
            board_obj.board[row].append(0)
    return board_obj


def test_band():
    board_obj = init_board()
    piece = Piece(5, 0, WHITE)
    board_obj.board[5][0] = piece
    evaluator = Evaluator(board_obj)
    assert evaluator.evaluate() == 3
    piece = Piece(5, 7, BROWN)
    board_obj.board[5][0] = 0
    board_obj.board[5][7] = piece
    assert evaluator.evaluate() == -3


def test_almost_band_col():
    board_obj = init_board()
    piece = Piece(5, 1, WHITE)
    board_obj.board[5][1] = piece
    evaluator = Evaluator(board_obj)
    assert evaluator.evaluate() == 2
    piece = Piece(5, 6, BROWN)
    board_obj.board[5][1] = 0
    board_obj.board[5][6] = piece
    assert evaluator.evaluate() == -2


def test_almost_band_row():
    board_obj = init_board()
    piece = Piece(6, 3, WHITE)
    board_obj.board[6][3] = piece
    evaluator = Evaluator(board_obj)
    assert evaluator.evaluate() == 2
    piece = Piece(6, 3, BROWN)
    board_obj.board[6][3] = piece
    assert evaluator.evaluate() == -1
    piece = Piece(6, 6, BROWN)
    board_obj.board[1][3] = piece
    assert evaluator.evaluate() == -3


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




