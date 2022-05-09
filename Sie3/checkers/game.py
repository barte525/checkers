from .constants import WHITE, BROWN
from checkers.board import Board


class Game:
    def __init__(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.all_valid_moves = []

    def check_winner(self):
        winner = self.board.check_winner()
        if winner == WHITE:
            return "WHITE WON!"
        if winner == BROWN:
            return "BLACK WON!"
        return None

    def select_or_move_piece(self, row, col):
        #Try to move if selected, if does not work select again
        if self.selected:
            if not self.__move(row, col):
                self.selected = None
                self.select_or_move_piece(row, col)

        # select
        piece = self.board.get_piece_from_cords(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.check_all_valid_moves()
            if not self.__is_piece_possible_to_select(self.selected):
                self.valid_moves = {}
                return False
            self.valid_moves = self.board.get_valid_moves(piece, possible_moves=[])
            return True
        return False

    def __move(self, selected_row, selected_column):
        piece = self.board.get_piece_from_cords(selected_row, selected_column)
        if self.selected != 0 and piece == 0:
            for move in self.valid_moves:
                cords_for_selected_piece, destination_cords, jumped_pieces = move
                if destination_cords[0] == selected_row and destination_cords[1] == selected_column:
                    if len(jumped_pieces) > 0:
                        for (jumped_piece_row, jumped_piece_column) in jumped_pieces:
                            jumped_piece = self.board.get_piece_from_cords(jumped_piece_row, jumped_piece_column)
                            self.board.remove(jumped_piece)
                    self.board.move(self.selected, destination_cords[0], destination_cords[1])
                    self.__change_turn()
                    break
        else:
            return False
        return True

    def check_all_valid_moves(self):
        max_jumped_pieces = 0
        all_pieces = self.board.get_all_pieces_for_color(self.turn)
        all_valid_moves = []
        for piece in all_pieces:
            valid_moves_for_piece = self.board.get_valid_moves(piece, possible_moves=[])
            if valid_moves_for_piece:
                jumped_pieces_for_move = len(valid_moves_for_piece[0][2])
                if jumped_pieces_for_move > max_jumped_pieces:
                    all_valid_moves = [(piece, valid_moves_for_piece)]
                    max_jumped_pieces = jumped_pieces_for_move
                elif jumped_pieces_for_move == max_jumped_pieces:
                    all_valid_moves.append((piece, valid_moves_for_piece))
        self.all_valid_moves = all_valid_moves

    def __is_piece_possible_to_select(self, piece):
        for possible_piece_to_select, _ in self.all_valid_moves:
            if possible_piece_to_select == piece:
                return True
        return False

    def __change_turn(self):
        self.all_valid_moves = []
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BROWN
        else:
            self.turn = WHITE
