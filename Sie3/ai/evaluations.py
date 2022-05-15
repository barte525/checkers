from checkers.board import Board
from checkers.const import WHITE, COLS, BROWN, ROWS
from typing import List
from checkers.piece import Piece


class Evaluator:
    queen_weight: float = 6
    band_weight: float = 3
    close_to_band_weight: float = 2
    man_weight: float = 1

    def __init__(self, board: Board):
        self.board: Board = board

    def evaluate(self) -> float:
        print(type(self.board))
        white: List[Piece] = self.board.get_all_pieces_of_color(WHITE)
        black: List[Piece] = self.board.get_all_pieces_of_color(BROWN)
        return Evaluator.__evaluate_one_site(white) - Evaluator.__evaluate_one_site(black)


    @staticmethod
    def __evaluate_one_site(pieces: List[Piece]) -> float:
        result: float = 0
        for piece in pieces:
            if piece.queen:
                result += Evaluator.queen_weight
            elif piece.col == 0 or piece.col == COLS - 1:
                result += Evaluator.band_weight
            elif Evaluator.__is_piece_close_to_band(piece):
                result += Evaluator.close_to_band_weight
            else:
                result += Evaluator.man_weight
        return result

    @staticmethod
    def __is_piece_close_to_band(piece: Piece):
        return piece.col == 1 or piece.col == COLS - 2 or (piece.color == BROWN and piece.row == 1) or\
               (piece.color == WHITE and piece.row == ROWS - 2)