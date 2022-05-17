from .const import WHITE, BROWN, Color
from checkers.board import Board, Move
from checkers.piece import Piece
from typing import List, Tuple


class Engine:
    def __init__(self):
        self.selected: Piece = None
        self.board: Board = Board()
        self.turn: Color = WHITE
        self.valid_moves: List = []

    def check_winner(self) -> Color:
        return self.board.check_winner()

    def is_game_over(self):
        return self.check_winner() and self.__check__for_valid_moves()

    def ai_move(self, board: Board):
        self.board = board
        self.__change_turn()

    def select_or_move_piece(self, row: int, col: int) -> None:
        # try to move if selected
        if self.selected:
            if not self.__move(row, col):
                self.selected = None
            self.selected = None
        # select
        piece: Piece = self.board.get_piece_from_cords(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.update_valid_moves_with_max_captures(piece)

    def get_all_valid_moves(self, color: Color):
        result = []
        all_pieces: List[Piece] = self.board.get_all_pieces_of_color(color)
        for piece in all_pieces:
            result.append((piece, self.get_valid_moves_with_max_captures(piece, color)))
        return result

    def update_valid_moves_with_max_captures(self, piece: Piece) -> None:
        if not self.__is_piece_possible_to_select(self.selected, self.get_all_moves_with_max_captures(self.turn)):
            self.valid_moves = []
        else:
            self.valid_moves = self.board.get_valid_moves_for_piece(piece, possible_moves=[])

    def get_valid_moves_with_max_captures(self, piece: Piece, color) -> List:
        if not self.__is_piece_possible_to_select(piece, self.get_all_moves_with_max_captures(color)):
            return []
        else:
            return self.board.get_valid_moves_for_piece(piece, possible_moves=[])

    def ai_special_move(self, piece: Piece, move: Move) -> None:
        row, col, captured_pieces = self.__unpack_move(move)
        self.__remove_captured_pieces(captured_pieces)
        self.board.move(piece, row, col)
        self.__change_turn()

    def __move(self, selected_row: int, selected_col: int) -> bool:
        if self.selected is not None and self.board.is_square_free(selected_row, selected_col):
            for move in self.valid_moves:
                # do I need cords for selected piece
                row, col, captured_pieces = self.__unpack_move(move)
                if Engine.__check_if_move_is_valid(row, selected_row, col, selected_col):
                    self.__remove_captured_pieces(captured_pieces)
                    self.board.move(self.selected, row, col)
                    self.__change_turn()
                    return True
        return False

    def __remove_captured_pieces(self, captured_pieces: List[Tuple[int, int]]) -> None:
        if captured_pieces:
            for pieces_cords in captured_pieces:
                self.board.remove(self.board.get_piece_from_cords(pieces_cords[0], pieces_cords[1]))

    @staticmethod
    def __check_if_move_is_valid(row: int, selected_row: int, col: int, selected_col: int) -> bool:
        return row == selected_row and col == selected_col

    @staticmethod
    def __unpack_move(move: Tuple) -> Tuple[int, int, List[Tuple[int, int]]]:
        _, destination_cords, jumped_pieces = move
        row, col = destination_cords
        return row, col, jumped_pieces

    def get_all_moves_with_max_captures(self, color) -> List:
        max_captured_pieces: int = 0
        all_pieces: List[Piece] = self.board.get_all_pieces_of_color(color)
        moves_with_max_captures: list = []
        for piece in all_pieces:
            valid_moves_for_piece: list = self.board.get_valid_moves_for_piece(piece, possible_moves=[])
            if valid_moves_for_piece:
                moves_with_max_captures, max_captured_pieces = self.__update_moves_with_max_captures(
                    max_captured_pieces, moves_with_max_captures, piece, valid_moves_for_piece)
        return moves_with_max_captures

    @staticmethod
    def __update_moves_with_max_captures(max_captured_pieces: int, moves_with_max_captures: list,
                                         piece: Piece, valid_moves_for_piece: list) -> Tuple[List, int]:
        number_of_captured_pieces: int = len(valid_moves_for_piece[0][2])
        if number_of_captured_pieces > max_captured_pieces:
            moves_with_max_captures: list = [(piece, valid_moves_for_piece)]
            max_captured_pieces = number_of_captured_pieces
        if number_of_captured_pieces == max_captured_pieces:
            moves_with_max_captures.append((piece, valid_moves_for_piece))
        return moves_with_max_captures, max_captured_pieces

    @staticmethod
    def __is_piece_possible_to_select(piece: Piece, all_valid_moves: List) -> bool:
        for possible_piece_to_select, _ in all_valid_moves:
            if possible_piece_to_select == piece:
                return True
        return False

    def __check__for_valid_moves(self) -> bool:
        if not self.get_all_valid_moves(WHITE) or not self.get_all_valid_moves(BROWN):
            return True
        return False

    def __change_turn(self) -> None:
        self.valid_moves: list = []
        if self.turn == WHITE:
            self.turn = BROWN
        else:
            self.turn = WHITE
