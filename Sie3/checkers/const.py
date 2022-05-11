import pygame
from typing import Tuple
WIDTH: int = 800
HEIGHT: int = 800
ROWS: int = 8
COLS: int = 8
SQUARE: float = WIDTH // COLS
PADDING: int = 15

Color = Tuple[int, int, int]
WHITE: Color = (255, 255, 255)
BLACK: Color = (0, 0, 0)
BLUE: Color = (0, 0, 255)
GREY: Color = (128, 128, 128)
BROWN: Color = (110, 64, 48)

CROWN: pygame.Surface = pygame.transform.scale(pygame.image.load('checkers/crown.png'), (50, 50))
