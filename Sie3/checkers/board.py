from .gui_const import ROWS, COLS, WHITE, BROWN
from .piece import Piece
import copy
from typing import List, Tuple

List_of_moves = List[Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]]]]

class Board:
    def __init__(self):
        self.board: List = []
        self.black_pieces: int = 12
        self.white_pieces: int = 12
        self.black_queens: int = 0
        self.white_queens: int = 0
        self.__create_board()

    def is_square_free(self, row: int, col: int) -> bool:
        if self.board[row][col] == 0:
            return True
        return False

    def get_piece_from_cords(self, row: int, col: int) -> Piece:
        return self.board[row][col]

    def move(self, piece: Piece, row: int, col: int) -> None:
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        self.__update_queens(piece, row)

    def check_winner(self) -> tuple:
        if self.black_pieces <= 0:
            return WHITE
        elif self.white_pieces <= 0:
            return BROWN
        return None

    def remove(self, piece: Piece) -> None:
        if piece != 0:
            self.board[piece.row][piece.col] = 0
            self.__update_pieces(piece)

    def __create_board(self) -> None:
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BROWN))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def __update_queens(self, piece: Piece, row: int) -> None:
        if row == 0 and piece.color == WHITE:
            piece.make_queen()
            self.white_queens += 1
        if row == ROWS-1 and piece.color == BROWN:
            piece.make_queen()
            self.black_queens += 1

    def __update_pieces(self, piece: Piece) -> None:
        if piece.color == BROWN:
            self.black_pieces -= 1
            if piece.queen:
                self.black_queens -= 1
        else:
            self.white_pieces -= 1
            if piece.queen:
                self.white_queens -= 1

    def get_all_pieces_of_color(self, color: Tuple[int, int, int]) -> List[Piece]:
        all_pieces: List = []
        for row in range(ROWS):
            for column in range(COLS):
                piece: Piece = self.board[row][column]
                if piece is not 0 and piece.color == color:
                    all_pieces.append(piece)
        return all_pieces

    def get_valid_moves_for_piece(self, piece: Piece, possible_moves: List = []) -> List:
        if piece.queen:
            return self.__get_valid_moves_for_queen(piece, possible_moves)
        return self.__get_valid_moves_for_man(piece, possible_moves)

    def __get_valid_moves_for_queen(self, piece, possible_moves):
        diagonals = self.__get_diagonals_for_queen(piece.row, piece.col)
        left_up_diagonal = diagonals[0]
        left_down_diagonal = diagonals[1]
        right_up_diagonal = diagonals[2]
        right_down_diagonal = diagonals[3]
        moves = self.__is_possible_to_move_for_queen(piece, left_up_diagonal)
        if moves is not None:
            possible_moves.extend(moves)
        moves = self.__is_possible_to_move_for_queen(piece, left_down_diagonal)
        if moves is not None:
            possible_moves.extend(moves)
        moves = self.__is_possible_to_move_for_queen(piece, right_up_diagonal)
        if moves is not None:
            possible_moves.extend(moves)
        moves = self.__is_possible_to_move_for_queen(piece, right_down_diagonal)
        if moves is not None:
            possible_moves.extend(moves)
        moves_with_jumping = self.__get_moves_with_capture(possible_moves)
        if moves_with_jumping:
            return self.__check_more_moves_after_jumping(piece, moves_with_jumping)
        else:
            return possible_moves

    # piece
    def __get_valid_moves_for_man(self, piece: Piece, possible_moves_all_pieces: List_of_moves) -> List_of_moves:
        corners_for_piece: List_of_moves = self.__get_corners_for_man(piece)
        possible_moves: List_of_moves = self.__get_possible_moves_for_man(corners_for_piece)
        moves_with_capture: List_of_moves = self.__get_moves_with_capture(possible_moves)
        self.__update_list_with_many_captures(moves_with_capture, possible_moves_all_pieces)
        if moves_with_capture:
            return self.__check_more_moves_after_jumping(piece, moves_with_capture)
        elif possible_moves_all_pieces:
            return possible_moves_all_pieces
        else:
            return possible_moves

    # piece
    # jesli jest ruch z wieloma biciami to stackujemy pionki zbite podrodze
    @staticmethod
    def __update_list_with_many_captures(moves_with_capture: List_of_moves, possible_moves_all_pieces: List_of_moves)\
            -> None:
        for move in possible_moves_all_pieces:
            for jump_move in moves_with_capture:
                if move[1] == jump_move[0]:
                    jump_move[2].extend(move[2])

    # piece
    @staticmethod
    def __get_moves_with_capture(possible_moves: List_of_moves) -> List_of_moves:
        return list(filter(lambda move: len(move[2]) > 0, possible_moves))

    # piece
    @staticmethod
    def __get_possible_moves_for_man(corners_for_piece: List_of_moves) -> List_of_moves:
        return list(filter(lambda move: move is not None, corners_for_piece))


    # piece and queen
    def __check_more_moves_after_jumping(self, piece, moves_with_jumping):
        for start_piece_cords, destination_piece_cords, jumped_pieces in moves_with_jumping:
            updated_board = copy.deepcopy(self)
            moved_piece = copy.deepcopy(piece)
            updated_board.move(moved_piece, destination_piece_cords[0], destination_piece_cords[1])
            for jumped_piece_row, jumped_piece_column in jumped_pieces:
                jumped_piece = updated_board.get_piece_from_cords(jumped_piece_row, jumped_piece_column)
                updated_board.remove(jumped_piece)
            return updated_board.__get_valid_moves_for_man(moved_piece, moves_with_jumping)

    # piece
    def __get_corners_for_man(self, piece: Piece) -> List_of_moves:
        possible_moves: List_of_moves = []
        left: int = piece.col - 1
        right: int = piece.col + 1
        up: int = piece.row + 1
        down: int = piece.row - 1
        if 0 <= left <= COLS - 1:
            possible_moves.append(self.__check_piece_for_man(piece, up, left, False, False))
            possible_moves.append(self.__check_piece_for_man(piece, down, left, True, False))
        if 0 <= right <= COLS - 1:
            possible_moves.append(self.__check_piece_for_man(piece, up, right, False, True))
            possible_moves.append(self.__check_piece_for_man(piece, down, right, True, True))
        return possible_moves

    # piece
    def __check_piece_for_man(self, piece, destination_row, destination_column, down, right):
        possible_move = None
        start = piece.row, piece.col
        if 0 <= destination_row <= ROWS - 1:
            checked_piece = self.get_piece_from_cords(destination_row, destination_column)
            if (not piece.queen and self.__is_correct_row_direction(piece.color, piece.row, destination_row) and \
                checked_piece is 0) or (piece.queen and checked_piece is 0):
                destination = destination_row, destination_column
                possible_move = (start, destination, [])
            elif checked_piece is not 0:
                if checked_piece.color != piece.color:
                    if down and not right and self.__belong_to_board(destination_row - 1, destination_column - 1):
                        if self.get_piece_from_cords(destination_row - 1, destination_column - 1) is 0:
                            destination = destination_row - 1, destination_column - 1
                            jumped_pieces_cords = destination_row, destination_column
                            possible_move = (start, destination, [jumped_pieces_cords])
                    if not down and not right and self.__belong_to_board(destination_row + 1, destination_column - 1):
                        if self.get_piece_from_cords(destination_row + 1, destination_column - 1) is 0:
                            destination = destination_row + 1, destination_column - 1
                            jumped_pieces_cords = destination_row, destination_column
                            possible_move = (start, destination, [jumped_pieces_cords])
                    if down and right and self.__belong_to_board(destination_row - 1, destination_column + 1):
                        if self.get_piece_from_cords(destination_row - 1, destination_column + 1) is 0:
                            destination = destination_row - 1, destination_column + 1
                            jumped_pieces_cords = destination_row, destination_column
                            possible_move = (start, destination, [jumped_pieces_cords])
                    if not down and right and self.__belong_to_board(destination_row + 1, destination_column + 1):
                        if self.get_piece_from_cords(destination_row + 1, destination_column + 1) is 0:
                            destination = destination_row + 1, destination_column + 1
                            jumped_pieces_cords = destination_row, destination_column
                            possible_move = (start, destination, [jumped_pieces_cords])
        return possible_move

    # piece
    def __belong_to_board(self, row, column):
        return 0 <= row <= ROWS - 1 and 0 <= column <= COLS - 1

    # piece
    def __is_correct_row_direction(self, color, from_row, to_row):
        if color == WHITE:
            return from_row >= to_row
        else:
            return from_row <= to_row

    # queen
    def __get_diagonals_for_queen(self, row, column):
        left_up_diagonal = self.__get_diagonal_for_queen(row, column, False, False)
        left_down_diagonal = self.__get_diagonal_for_queen(row, column, True, False)
        right_up_diagonal = self.__get_diagonal_for_queen(row, column, False, True)
        right_down_diagonal = self.__get_diagonal_for_queen(row, column, True, True)
        return left_up_diagonal, left_down_diagonal, right_up_diagonal, right_down_diagonal

    # queen
    def __is_possible_to_move_for_queen(self, king, diagonal):
        possible_moves = []
        jumped_pieces = []
        i = 0
        while i < len(diagonal):
            checked_piece_row, checked_piece_column = diagonal[i]
            checked_piece = self.get_piece_from_cords(checked_piece_row, checked_piece_column)
            start_cords = king.row, king.col
            destination_cords = checked_piece_row, checked_piece_column
            if checked_piece is 0:
                possible_moves.append((start_cords, destination_cords, jumped_pieces))
            elif checked_piece.color != king.color:
                if i + 1 < len(diagonal):
                    jumped_piece_row, jumped_piece_column = checked_piece_row, checked_piece_column
                    checked_piece_row, checked_piece_column = diagonal[i + 1]
                    checked_piece = self.get_piece_from_cords(checked_piece_row, checked_piece_column)
                    if checked_piece is 0:
                        jumped_pieces = jumped_pieces.copy()
                        jumped_pieces.append((jumped_piece_row, jumped_piece_column))
                        possible_moves.append((start_cords, (checked_piece_row, checked_piece_column), jumped_pieces))
                        i += 1
            else:
                return possible_moves
            i += 1
        return possible_moves

    #queen
    def __get_diagonal_for_queen(self, row, column, down, right):
        diagonal_pieces_cords = []
        while 0 <= row < ROWS and 0 <= column < COLS:
            if down:
                row += 1
            else:
                row -= 1
            if right:
                column += 1
            else:
                column -= 1
            if 0 <= row < ROWS and 0 <= column < COLS:
                diagonal_pieces_cords.append((row, column))
        return diagonal_pieces_cords