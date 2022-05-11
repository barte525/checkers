from .const import WHITE, BROWN
from checkers.board import Board
from checkers.piece import Piece
from typing import List, Tuple


class Engine:
    def __init__(self):
        self.selected: Piece = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves: List = []

    def check_winner(self) -> str:
        winner: tuple = self.board.check_winner()
        if winner == WHITE:
            return "WHITE WON!"
        if winner == BROWN:
            return "BLACK WON!"
        return None

    def select_or_move_piece(self, row: int, col: int) -> None:
        # try to move if selected
        if self.selected:
            if not self.__move(row, col):
                self.selected = None
                self.select_or_move_piece(row, col)
        # select
        piece: Piece = self.board.get_piece_from_cords(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.__get_valid_moves_with_max_captures(piece)

    def __get_valid_moves_with_max_captures(self, piece: Piece) -> None:
        if not self.__is_piece_possible_to_select(self.selected, self.__get_all_moves_with_max_captures()):
            self.valid_moves = []
        else:
            self.valid_moves = self.board.get_valid_moves_for_piece(piece, possible_moves=[])

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

    def __get_all_moves_with_max_captures(self) -> List:
        max_captured_pieces: int = 0
        all_pieces: List[Piece] = self.board.get_all_pieces_of_color(self.turn)
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

    def __change_turn(self) -> None:
        self.valid_moves: list = []
        if self.turn == WHITE:
            self.turn = BROWN
        else:
            self.turn = WHITE
