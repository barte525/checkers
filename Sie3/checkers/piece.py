from .const import Color


class Piece:
    def __init__(self, row: int, col: int, color: Color):
        self.row: int = row
        self.col: int = col
        self.color: Color = color
        self.queen: bool = False
        # fields for gui
        self.x: float = 0
        self.y: float = 0

    def make_queen(self) -> None:
        self.queen = True

    def move(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __repr__(self):
        return str(self.color)
