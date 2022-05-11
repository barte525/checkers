import pygame
from checkers.const import WIDTH, HEIGHT, SQUARE, Color, WHITE, BROWN
from checkers.engine import Engine
from checkers.gui import Gui
from typing import Tuple


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
        while run:
            clock.tick(self.FPS)
            if engine.check_winner():
                GamePlay.announce_winner(engine.check_winner())
                run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse_pos(pos)
                    engine.select_or_move_piece(row, col)
            gui.update(engine.valid_moves, engine.board)
        pygame.quit()

    @staticmethod
    def announce_winner(winner: Color) -> None:
        if winner == WHITE:
            print("WHITE WON!!!")
        if winner == BROWN:
            print("BLACK WON!!!")
