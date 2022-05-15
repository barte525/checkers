from .evaluations import Evaluator
from checkers.engine import Engine
from typing import Tuple, List
from checkers.board import Move
from checkers.piece import Piece
import copy
from checkers.const import WHITE, BROWN, Color


def minimax(position: Engine, maximize: bool, depth: int = 4, alpha_beta: bool = False):
    if alpha_beta:
        return __minimax(position, maximize, depth, float("-inf"), float("inf"))
    else:
        return __minimax(position, maximize, depth)


def __minimax(position: Engine, maximize: bool, depth: int, alpha: float = None, beta: float = None) -> Tuple[int, Engine]:
    if depth == 0 or position.is_game_over():
        return Evaluator(position.board).evaluate(), position
    if maximize:
        max_eval: float = float("-inf")
        position_after_best_move = None
        for moved_board in get_boards_for_each_move(position, maximize):
            if not alpha:
                eval: float = __minimax(moved_board, False, depth - 1)[0]
            else:
                eval: float = __minimax(moved_board, False, depth - 1, alpha, beta)[0]
            max_eval: float = max(max_eval, eval)
            if max_eval == eval:
                position_after_best_move: Engine = moved_board
            if alpha:
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval, position_after_best_move
    else:
        min_score = float('inf')
        position_after_best_move = None
        for moved_board in get_boards_for_each_move(position, maximize):
            if not alpha:
                eval: float = __minimax(moved_board, True, depth - 1)[0]
            else:
                eval: float = __minimax(moved_board, True, depth - 1, alpha, beta)[0]
            min_score: float = min(min_score, eval)
            if min_score == eval:
                position_after_best_move: Engine = moved_board
            if alpha:
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_score, position_after_best_move


def get_boards_for_each_move(game: Engine, is_white: bool) -> List[Engine]:
    result: List[Engine] = []
    color: Color = WHITE if is_white else BROWN
    all_moves: List[Piece, Move] = game.get_all_valid_moves(color)

    for piece, moves in all_moves:
        for move in moves:
            _, future_cords, captured_pieces = move
            new_board: Engine = copy.deepcopy(game)
            moved_piece: Piece = new_board.board.get_piece_from_cords(piece.row, piece.col)
            new_board.board.move(moved_piece, future_cords[0], future_cords[1])
            for captured_piece_row, captured_piece_column in captured_pieces:
                jumped_piece: Piece = new_board.board.get_piece_from_cords(captured_piece_row, captured_piece_column)
                new_board.board.remove(jumped_piece)
            result.append(new_board)
    return result