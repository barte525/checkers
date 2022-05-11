import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
PADDING = 15
OUTLINE = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
BROWN = (110, 64, 48)

CROWN = pygame.transform.scale(pygame.image.load('assets/assets/crown.png'), (44, 25))
