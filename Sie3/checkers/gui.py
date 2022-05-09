import pygame
from .gui_const import BLUE, SQUARE_SIZE, CROWN, GREY, ROWS, COLS, BLACK, PADDING, OUTLINE


class Gui:
    def __init__(self, win, board):
        self.win = win
        self.board = board.board

    def update(self, valid_moves, board):
        self.board = board.board
        self.__draw_board()
        self.__draw_valid_moves(valid_moves)
        pygame.display.update()

    def __draw_board(self):
        self.__draw_squares()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    self.__draw_piece(piece)

    def __draw_piece(self, piece):
        self.__calculate_position_of_piece(piece)
        radius = SQUARE_SIZE//2 - PADDING
        pygame.draw.circle(self.win, GREY, (piece.x, piece.y), radius + OUTLINE)
        pygame.draw.circle(self.win, piece.color, (piece.x, piece.y), radius)
        if piece.queen:
            self.win.blit(CROWN, (piece.x - CROWN.get_width()//2, piece.y - CROWN.get_height()//2))

    def __draw_squares(self):
        self.win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.win, GREY, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def __draw_valid_moves(self, moves):
        for move in moves:
            _, destination, _ = move
            pygame.draw.circle(self.win, BLUE, (destination[1] * SQUARE_SIZE + SQUARE_SIZE//2, destination[0] * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    @staticmethod
    def __calculate_position_of_piece(piece):
        piece.x = SQUARE_SIZE * piece.col + SQUARE_SIZE // 2
        piece.y = SQUARE_SIZE * piece.row + SQUARE_SIZE // 2