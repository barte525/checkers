import pygame
from checkers.const import WIDTH, HEIGHT, SQUARE, Color, WHITE, BROWN
from checkers.engine import Engine
from checkers.gui import Gui
from typing import Tuple, List, Optional
from .board import Board
from ai.algorithms import minimax
import time
import random


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

    def play(self, ai: bool, double_ai: bool, random_first_move: bool, alpha_beta: bool = False) -> Optional[Tuple[float, float]]:
        clock = pygame.time.Clock()
        engine: Engine = Engine()
        gui: Gui = Gui(self.win, engine.board)
        run: bool = True
        tie_iterator_queens: int = 0
        tie_iterator: int = 0
        first_moves_done: int = 0
        black_time: float = 0
        white_time: float = 0
        black_moves: float = 0
        white_moves: float = 0
        while run:
            clock.tick(self.FPS)
            if first_moves_done < 2 and random_first_move:
                GamePlay.__do_random_move(engine)
                first_moves_done += 1
            elif ai and engine.turn == BROWN:
                start = time.time()
                _, new_board = minimax(engine, False, alpha_beta=alpha_beta, depth=2)
                end = time.time()
                tie_iterator += 1
                black_time += (end-start)
                black_moves += 1
                engine.ai_move(new_board.board)
            elif double_ai and engine.turn == WHITE:
                start = time.time()
                _, new_board = minimax(engine, True, alpha_beta=alpha_beta, depth=5)
                end = time.time()
                tie_iterator += 1
                white_time += (end-start)
                white_moves += 1
                engine.ai_move(new_board.board)
            if engine.check_winner():
                GamePlay.__announce_winner(engine.check_winner(), engine)
                run = False
            if tie_iterator == 80:
                GamePlay.__announce_winner(None, engine)
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
                    tie_iterator_queens += GamePlay.__is_all_queen(engine.board)
                    if tie_iterator_queens >= 30:
                        GamePlay.__announce_winner(None)
                        run = False
            gui.update(engine.valid_moves, engine.board)
        pygame.quit()
        if engine.check_winner() == WHITE:
            return white_moves, white_time/white_moves

    @staticmethod
    def __do_random_move(engine: Engine):
        all_valid: List = engine.get_all_valid_moves(engine.turn)
        all_valid_flat: List = []
        for piece, moves in all_valid:
            for move in moves:
                all_valid_flat.append((piece, move))
        rand_inx: int = random.randint(0, len(all_valid_flat) - 1)
        engine.ai_special_move(all_valid_flat[rand_inx][0], all_valid_flat[rand_inx][1])

    @staticmethod
    def __announce_winner(winner: Color, engine, opposite=False) -> None:
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

