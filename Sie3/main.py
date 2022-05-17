from checkers.gameplay import GamePlay
from typing import List, Optional, Tuple


def simulation(number_of_white_wins: int, ai: bool, double_ai: bool, random_first_move: bool, alpha_beta: bool,
               white_depth: int, black_depth: int):
    moves: List[int] = []
    times: List[float] = []
    number_of_games: int = 0
    while len(moves) < number_of_white_wins:
        number_of_games += 1
        play: GamePlay = GamePlay()
        result: Optional[Tuple[float, float]] = play.play(ai=ai, double_ai=double_ai, random_first_move=random_first_move,
                                                          alpha_beta=alpha_beta, white_depth=white_depth, black_depth=black_depth)
        if result:
            moves.append(result[0])
            times.append(round(result[1], 3))
    print('ab5')
    print('moves', moves)
    print('times', times)
    print('avg_moves', round(sum(moves)/len(moves), 3))
    print('avg_time', round(sum(times)/len(times), 3))
    print('number of games:', number_of_games)


if __name__ == '__main__':
    simulation(3, True, True, True, True, 5, 2)