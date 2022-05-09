import pygame
from checkers.gui_const import WIDTH, HEIGHT, SQUARE_SIZE
from checkers.engine import Engine
from checkers.gui import Gui


class GamePlay:
    def __init__(self):
        self.FPS = 60
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Checkers')

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def play(self):
        run = True
        clock = pygame.time.Clock()
        engine = Engine()
        gui = Gui(self.win, engine.board)
        while run:
            clock.tick(self.FPS)
            if engine.check_winner():
                print(engine.check_winner())
                run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse(pos)
                    engine.select_or_move_piece(row, col)
            gui.update(engine.valid_moves, engine.board)
        pygame.quit()