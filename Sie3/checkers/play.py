import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers.game import Game
from checkers.GUI import GUI


class Play:
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
        game = Game()
        gui = GUI(self.win, game.board)
        while run:
            clock.tick(self.FPS)
            if game.check_winner():
                print(game.check_winner())
                run = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse(pos)
                    game.select_or_move_piece(row, col)
            gui.update(game.valid_moves, game.board)
        pygame.quit()