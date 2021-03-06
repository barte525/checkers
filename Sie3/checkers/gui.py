import pygame
from .const import BLUE, SQUARE, GREY, ROWS, COLS, BLACK, PADDING, CURSOR_SIZE
from .const import CROWN
from typing import List
from .board import List_of_moves, Board
from .piece import Piece


class Gui:
    def __init__(self, win, board):
        self.win: pygame.Surface = win
        self.board: List[List[Piece]] = board.board

    def update(self, valid_moves: List_of_moves, board: Board) -> None:
        self.board: List[List[Piece]] = board.board
        self.__draw_board()
        self.__draw_valid_moves(valid_moves)
        pygame.display.update()

    def __draw_board(self) -> None:
        self.__draw_squares()
        for row in range(ROWS):
            for col in range(COLS):
                piece: Piece = self.board[row][col]
                if piece != 0:
                    self.__draw_piece(piece)

    def __draw_piece(self, piece: Piece):
        self.__calculate_position_of_piece(piece)
        pieceSize: float = SQUARE // 2 - PADDING
        pygame.draw.circle(self.win, GREY, (piece.x, piece.y), pieceSize)
        pygame.draw.circle(self.win, piece.color, (piece.x, piece.y), pieceSize)
        if piece.queen:
            # in the middle of the square
            self.win.blit(CROWN, (piece.x - CROWN.get_width()//2, piece.y - CROWN.get_height()//2))

    def __draw_squares(self) -> None:
        self.win.fill(BLACK)
        for row in range(ROWS):
            # draw from first column in every second row
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.win, GREY, (row * SQUARE, col * SQUARE, SQUARE, SQUARE))

    def __draw_valid_moves(self, moves: List_of_moves) -> None:
        for move in moves:
            _, destination, _ = move
            pygame.draw.circle(self.win, BLUE, (destination[1] * SQUARE + SQUARE // 2,
                                                destination[0] * SQUARE + SQUARE // 2), CURSOR_SIZE)

    @staticmethod
    def __calculate_position_of_piece(piece: Piece) -> None:
        # center of a given square
        piece.x = SQUARE * piece.col + SQUARE // 2
        piece.y = SQUARE * piece.row + SQUARE // 2