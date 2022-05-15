import pygame
from checkers.const import WIDTH, HEIGHT, SQUARE, Color, WHITE, BROWN
from checkers.engine import Engine
from checkers.gui import Gui
from typing import Tuple
from .board import Board


class GamePlay:
    def __init__(self):
        self.FPS: int = 60
        self.win: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Checkers')

    @staticmethod
    def get_row_col_from_mouse_pos(pos: Tuple[int, int]) -> Tuple[int, int]:
        row: int = pos[1] // SQUARE
        col: int = pos[0] // SQUARE
        return row, col

    def play(self) -> None:
        clock = pygame.time.Clock()
        engine: Engine = Engine()
        gui: Gui = Gui(self.win, engine.board)
        run: bool = True
        tie_iterator: int = 0
        while run:
            clock.tick(self.FPS)
            if engine.check_winner():
                GamePlay.__announce_winner(engine.check_winner())
                run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse_pos(pos)
                    engine.select_or_move_piece(row, col)
                    if GamePlay.__check__for_valid_moves(engine):
                        run = False
                    tie_iterator += GamePlay.__is_all_queen(engine.board)
                    print(tie_iterator)
                    if tie_iterator >= 30:
                        GamePlay.__announce_winner(None)
                        run = False
            gui.update(engine.valid_moves, engine.board)
        pygame.quit()

    @staticmethod
    def __announce_winner(winner: Color, opposite=False) -> None:
        if (winner == WHITE and not opposite) or (winner == BROWN and opposite):
            print("WHITE WON!!!")
        if (winner == BROWN and not opposite) or (winner == WHITE and opposite):
            print("BLACK WON!!!")
        if winner is None:
            print("TIE!")

    @staticmethod
    def __check__for_valid_moves(engine: Engine) -> bool:
        if not engine.get_all_moves_with_max_captures(engine.turn):
            GamePlay.__announce_winner(engine.turn, True)
            return True
        return False

    @staticmethod
    def __is_all_queen(board: Board) -> int:
        return board.black_pieces - board.black_queens == 0 and board.white_pieces - board.white_queens == 0

