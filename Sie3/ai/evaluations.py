from checkers.board import Board
from checkers.const import WHITE, COLS, BROWN, ROWS
from typing import List
from checkers.piece import Piece


class Evaluator:
    first_queen: float = 10
    second_queen: float = 3
    band_weight: float = 1.8
    close_to_band_weight: float = 1.5
    man_weight: float = 1

    def __init__(self, board: Board):
        self.board: Board = board

    def evaluate(self) -> float:
        white: List[Piece] = self.board.get_all_pieces_of_color(WHITE)
        black: List[Piece] = self.board.get_all_pieces_of_color(BROWN)
        return self.__evaluate_one_site(white, "white") - self.__evaluate_one_site(black, "black")

    def __evaluate_one_site(self, pieces: List[Piece], color: str) -> float:
        result: float = 0
        for piece in pieces:
            if piece.queen and getattr(self.board, color+"_queens") != 0:
                result += Evaluator.first_queen
            elif piece.queen:
                result += Evaluator.second_queen
            elif piece.col == 0 or piece.col == COLS - 1:
                result += Evaluator.band_weight
            elif Evaluator.__is_piece_close_to_band(piece):
                result += Evaluator.close_to_band_weight
            else:
                result += Evaluator.man_weight
        return result

    @staticmethod
    def __is_piece_close_to_band(piece: Piece):
        return piece.col == 1 or piece.col == COLS - 2 or (piece.color == BROWN and piece.row == ROWS-2) or\
               (piece.color == WHITE and piece.row == 1) or (piece.color == BROWN and piece.row == 0) or\
               (piece.color == WHITE and piece.row == ROWS-1)