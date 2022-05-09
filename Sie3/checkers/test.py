import pytest
from checkers.board import Board
from checkers.piece import Piece
from checkers.constants import WHITE


def test_valid_moves_start():
    board_obj = Board()
    board = board_obj.board
    piece = Piece(5, 0, WHITE)
    board_obj.get_valid_moves(piece)