from checkers.board import Board
from checkers.piece import Piece
from checkers.const import WHITE, ROWS, BROWN, COLS
from ai.evaluations import Evaluator


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




