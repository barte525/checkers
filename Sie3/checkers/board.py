from .constants import ROWS, COLS, WHITE, BROWN
from .piece import Piece
import copy


class Board:
    def __init__(self):
        self.board = []
        self.black_pieces = self.white_pieces = 12
        self.black_queens = self.white_queens = 0
        self.__create_board()

    def get_piece_from_cords(self, row, col) -> Piece:
        return self.board[row][col]

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        self.__update_queens(piece, row)

    def check_winner(self):
        if self.black_pieces <= 0:
            return WHITE
        elif self.white_pieces <= 0:
            return BROWN
        return None

    def remove(self, piece):
        if piece != 0:
            self.board[piece.row][piece.col] = 0
            self.__update_pieces(piece)

    def __create_board(self):
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

    def __update_queens(self, piece, row):
        if row == 0 and piece.color == WHITE:
            piece.make_queen()
            self.white_queens += 1
        if row == ROWS-1 and piece.color == BROWN:
            piece.make_queen()
            self.black_queens += 1

    def __update_pieces(self, piece):
        if piece.color == BROWN:
            self.black_pieces -= 1
        else:
            self.white_pieces -= 1

    def get_valid_moves(self, piece, possible_moves=[]):
        if piece.queen:
            return self.__get_valid_moves_for_king(piece, possible_moves)
        else:
            return self.__get_valid_moves_for_man(piece, possible_moves)

    def __get_valid_moves_for_king(self, piece, possible_moves):
        diagonals = self.__get_diagonals_for_piece(piece.row, piece.col)
        left_up_diagonal = diagonals[0]
        left_down_diagonal = diagonals[1]
        right_up_diagonal = diagonals[2]
        right_down_diagonal = diagonals[3]
        moves = self.__is_possible_to_move_for_king(piece, left_up_diagonal)
        if moves is not None:
            possible_moves.extend(moves)
        moves = self.__is_possible_to_move_for_king(piece, left_down_diagonal)
        if moves is not None:
            possible_moves.extend(moves)
        moves = self.__is_possible_to_move_for_king(piece, right_up_diagonal)
        if moves is not None:
            possible_moves.extend(moves)
        moves = self.__is_possible_to_move_for_king(piece, right_down_diagonal)
        if moves is not None:
            possible_moves.extend(moves)
        moves_with_jumping = list(filter(lambda move: len(move[2]) > 0, possible_moves))
        if moves_with_jumping:
            return self.__check_more_moves_after_jumping(piece, moves_with_jumping)
        else:
            return possible_moves

    def __get_valid_moves_for_man(self, piece, possible_moves):
        possible_moves_for_selected_piece = self.__check_corners_for_piece(piece)
        filtered_possible_moves = list(filter(lambda move: move is not None, possible_moves_for_selected_piece))
        moves_with_jumping = list(filter(lambda move: len(move[2]) > 0, filtered_possible_moves))
        for move in possible_moves:
            for jump_move in moves_with_jumping:
                if move[1] == jump_move[0]:
                    jump_move[2].extend(move[2])
        if len(moves_with_jumping) > 0:
            return self.__check_more_moves_after_jumping(piece, moves_with_jumping)
        else:
            possible_moves.extend(filtered_possible_moves)
            moves_with_jumping = list(filter(lambda move: len(move[2]) > 0, possible_moves))
            if len(moves_with_jumping) > 0:
                return moves_with_jumping
            else:
                return possible_moves

    def __get_diagonals_for_piece(self, row, column):
        left_up_diagonal = self.__get_diagonal_for_piece(row, column, False, False)
        left_down_diagonal = self.__get_diagonal_for_piece(row, column, True, False)
        right_up_diagonal = self.__get_diagonal_for_piece(row, column, False, True)
        right_down_diagonal = self.__get_diagonal_for_piece(row, column, True, True)
        return left_up_diagonal, left_down_diagonal, right_up_diagonal, right_down_diagonal

    def __is_possible_to_move_for_king(self, king, diagonal):
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

    def __check_more_moves_after_jumping(self, piece, moves_with_jumping):
        for start_piece_cords, destination_piece_cords, jumped_pieces in moves_with_jumping:
            updated_board = copy.deepcopy(self)
            moved_piece = copy.deepcopy(piece)
            updated_board.move(moved_piece, destination_piece_cords[0], destination_piece_cords[1])
            for jumped_piece_row, jumped_piece_column in jumped_pieces:
                jumped_piece = updated_board.get_piece_from_cords(jumped_piece_row, jumped_piece_column)
                updated_board.remove(jumped_piece)
            return updated_board.__get_valid_moves_for_man(moved_piece, moves_with_jumping)

    def __check_corners_for_piece(self, piece):
        possible_moves = []
        left_column, right_column = piece.col - 1, piece.col + 1
        up_row, down_row = piece.row + 1, piece.row - 1
        if 0 <= left_column <= COLS - 1:
            possible_moves.append(self.__check_piece_for_moving(piece, up_row, left_column, False, False))
            possible_moves.append(self.__check_piece_for_moving(piece, down_row, left_column, True, False))
        if 0 <= right_column <= COLS - 1:
            possible_moves.append(self.__check_piece_for_moving(piece, up_row, right_column, False, True))
            possible_moves.append(self.__check_piece_for_moving(piece, down_row, right_column, True, True))
        return possible_moves

    def __check_piece_for_moving(self, piece, destination_row, destination_column, down, right):
        possible_move = None
        start = piece.row, piece.col
        if 0 <= destination_row <= ROWS - 1:
            checked_piece = self.get_piece_from_cords(destination_row, destination_column)
            print(checked_piece)
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

    def __get_diagonal_for_piece(self, row, column, down, right):
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

    def __belong_to_board(self, row, column):
        return 0 <= row <= ROWS - 1 and 0 <= column <= COLS - 1


    def __is_correct_row_direction(self, color, from_row, to_row):
        if color == WHITE:
            return from_row >= to_row
        else:
            return from_row <= to_row

    def get_all_pieces_for_color(self, color):
        all_pieces = []
        for row in range(ROWS):
            for column in range(COLS):
                piece = self.board[row][column]
                if piece is not 0 and piece.color == color:
                    all_pieces.append(piece)
        return all_pieces