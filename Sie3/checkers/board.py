from .gui_const import ROWS, COLS, WHITE, BROWN
from .piece import Piece
import copy
from typing import List, Tuple

Move = Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]]]
List_of_moves = List[Move]


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
        # for row in range(ROWS):
        #     self.board.append([])
        #     for col in range(COLS):
        #         if col % 2 == ((row + 1) % 2):
        #             if row < 3:
        #                 self.board[row].append(Piece(row, col, BROWN))
        #             elif row > 4:
        #                 self.board[row].append(Piece(row, col, WHITE))
        #             else:
        #                 self.board[row].append(0)
        #         else:
        #             self.board[row].append(0)

        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)
        queen = Piece(3, 6, color=WHITE)
        queen.queen = False

        self.board[3][6] = queen
        self.board[4][5] = Piece(4, 5, color=BROWN)
        self.board[4][3] = Piece(4, 3, color=BROWN)
        # for row in range(ROWS):
        #     self.board.append([])
        #     for col in range(COLS):
        #         self.board[row].append(0)
        # queen = Piece(2, 7, color=WHITE)
        # queen.queen = True
        #
        # self.board[2][7] = queen
        # self.board[4][5] = Piece(4, 5, color=BROWN)
        # self.board[3][2] = Piece(3, 2, color=BROWN)

    def __update_queens(self, piece: Piece, row: int) -> None:
        if row == 0 and piece.color == WHITE:
            piece.make_queen()
            self.white_queens += 1
        if row == ROWS - 1 and piece.color == BROWN:
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
            return self.__get_valid_moves_for_man_after_capture(piece, moves_with_jumping)
        else:
            return possible_moves

    def __get_valid_moves_for_man(self, piece: Piece, possible_moves_all_pieces: List_of_moves) -> List_of_moves:
        possible_moves: List_of_moves = self.__get_diagonals_for_piece(piece)
        moves_with_capture: List_of_moves = self.__get_moves_with_capture(possible_moves)
        self.__update_list_with_many_captures(moves_with_capture, possible_moves_all_pieces)
        if moves_with_capture:
            return self.__get_valid_moves_for_man_after_capture(piece, moves_with_capture)
        # after capture, did not find more captures
        elif possible_moves_all_pieces:
            return possible_moves_all_pieces
        return possible_moves

    @staticmethod
    def __update_list_with_many_captures(moves_with_capture: List_of_moves, possible_moves_all_pieces: List_of_moves) \
            -> None:
        for move in possible_moves_all_pieces:
            for captured in moves_with_capture:
                # jesli początkowe miejsce w ruchu z zbiciem jest równe docelowemu w ruchu
                if move[1] == captured[0]:
                    captured[2].extend(move[2])

    @staticmethod
    def __get_moves_with_capture(possible_moves: List_of_moves) -> List_of_moves:
        result: List_of_moves = []
        for move in possible_moves:
            if move[2]:
                result.append(move)
        return result

    def __get_valid_moves_for_man_after_capture(self, piece: Piece, moves_with_jumping: List_of_moves) -> List_of_moves:
        for move in moves_with_jumping:
            board_after_capture: Board = copy.deepcopy(self)
            moved_piece: Piece = copy.deepcopy(piece)
            board_after_capture.move(moved_piece, move[1][0], move[1][1])
            self.removed_captured_pieces(move[2], board_after_capture)
            return board_after_capture.__get_valid_moves_for_man(moved_piece, moves_with_jumping)

    @staticmethod
    def removed_captured_pieces(captured_pieces: List[Tuple[int, int]], board_after_capture) -> None:
        for captured_piece in captured_pieces:
            board_after_capture.remove(board_after_capture.get_piece_from_cords(captured_piece[0], captured_piece[1]))

    def __get_diagonals_for_piece(self, piece: Piece) -> List_of_moves:
        possible_moves: List_of_moves = []
        left: int = piece.col - 1
        right: int = piece.col + 1
        up: int = piece.row + 1
        down: int = piece.row - 1
        possible_moves.append(self.__check_diagonals_for_piece(piece, up, left, "up_left"))
        possible_moves.append(self.__check_diagonals_for_piece(piece, down, left, "down_left"))
        possible_moves.append(self.__check_diagonals_for_piece(piece, up, right, "up_right"))
        possible_moves.append(self.__check_diagonals_for_piece(piece, down, right, "down_right"))
        return self.__get_possible_moves_for_man(possible_moves)

    @staticmethod
    def __get_possible_moves_for_man(possible_moves: List_of_moves) -> List_of_moves:
        result: List_of_moves = []
        for move in possible_moves:
            if move:
                result.append(move)
        return result

    def __check_diagonals_for_piece(self, piece: Piece, destination_row: int, destination_column: int, direction: str) \
            -> Move:
        if not self.__check_if_in_board(destination_row, destination_column):
            return None
        if self.is_square_free(destination_row, destination_column):
            if Board.__move_one_square(piece, destination_row):
                return (piece.row, piece.col), (destination_row, destination_column), []
            return None
        if self.get_piece_from_cords(destination_row, destination_column).color == piece.color:
            return None
        return self.__try_to_capture(direction, piece, destination_row, destination_column)

    @staticmethod
    def __check_if_in_board(row: int, col: int):
        return 0 <= col <= COLS - 1 and 0 <= row <= ROWS - 1

    @staticmethod
    def __move_one_square(piece: Piece, destination_row: int) -> bool:
        if piece.queen:
            return True
        if piece.color == WHITE:
            return piece.row >= destination_row
        else:
            return piece.row <= destination_row

    def __try_to_capture(self, direction: str, piece: Piece, destination_row: int, destination_column: int) -> Move:
        captured_piece = (destination_row, destination_column)
        if direction == 'down_left' and self.__check_if_in_board(destination_row - 1, destination_column - 1) \
                and self.is_square_free(destination_row - 1, destination_column - 1):
            return (piece.row, piece.col), (destination_row - 1, destination_column - 1), [captured_piece]
        if direction == "up_left" and self.__check_if_in_board(destination_row + 1, destination_column - 1) \
                and self.is_square_free(destination_row + 1, destination_column - 1):
            return (piece.row, piece.col), (destination_row + 1, destination_column - 1), [captured_piece]
        if direction == "down_right" and self.__check_if_in_board(destination_row - 1, destination_column + 1) \
                and self.is_square_free(destination_row - 1, destination_column + 1):
            return (piece.row, piece.col), (destination_row - 1, destination_column + 1), [captured_piece]
        if direction == "up_right" and self.__check_if_in_board(destination_row + 1, destination_column + 1) \
                and self.is_square_free(destination_row + 1, destination_column + 1):
            return (piece.row, piece.col), (destination_row + 1, destination_column + 1), [captured_piece]
        return None

    def __get_diagonals_for_queen(self, row, column):
        left_up_diagonal = self.__get_diagonal_for_queen(row, column, False, False)
        left_down_diagonal = self.__get_diagonal_for_queen(row, column, True, False)
        right_up_diagonal = self.__get_diagonal_for_queen(row, column, False, True)
        right_down_diagonal = self.__get_diagonal_for_queen(row, column, True, True)
        return left_up_diagonal, left_down_diagonal, right_up_diagonal, right_down_diagonal

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
