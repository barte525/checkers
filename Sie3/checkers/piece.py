class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = True
        self.x = 0
        self.y = 0

    def make_queen(self):
        self.queen = True

    def move(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return str(self.color)
