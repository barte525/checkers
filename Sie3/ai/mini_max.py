from .evaluations import Evaluator
from checkers.engine import Engine
from checkers.board import Move
from typing import Tuple, List
import copy
from checkers.const import WHITE, BROWN


def minimax(position: Engine, maximize: bool, depth: int = 4) -> Tuple[int, Engine]:
    if depth == 0 or position.is_game_over():
        return Evaluator(position.board).evaluate(), None
    if maximize:
        max_eval: float = float("-inf")
        best_move = None
        for move_board in get_boards_for_each_move(position, maximize):
            state_score = minimax(move_board, False, depth - 1)[0]
            max_eval = max(max_eval, state_score)
            if max_eval == state_score:
                best_move = move_board
        return max_eval, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move_board in get_boards_for_each_move(position, maximize):
            state_score = minimax(move_board, True, depth - 1)[0]
            min_score = min(min_score, state_score)
            if min_score == state_score:
                best_move = move_board
        return min_score, best_move


def get_boards_for_each_move(game: Engine, is_white: bool) -> List[Engine]:
    boards = []
    color = WHITE if is_white else BROWN
    print(color)
    all_moves = game.get_all_valid_moves(color)
    print(all_moves)

    for piece, moves in all_moves:
        for move in moves:
            start_piece_cords, destination_piece_cords, jumped_pieces = move
            updated_board = copy.deepcopy(game)
            moved_piece = updated_board.board.get_piece_from_cords(piece.row, piece.col)
            updated_board.board.move(moved_piece, destination_piece_cords[0], destination_piece_cords[1])
            for jumped_piece_row, jumped_piece_column in jumped_pieces:
                jumped_piece = updated_board.board.get_piece_from_cords(jumped_piece_row, jumped_piece_column)
                updated_board.board.remove(jumped_piece)
            boards.append(updated_board)
    return boards