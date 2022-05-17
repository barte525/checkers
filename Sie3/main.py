from checkers.gameplay import GamePlay

number_of_loops = 5

if __name__ == '__main__':
    moves = []
    times = []
    while len(moves) < 5:
        play = GamePlay()
        result = play.play(ai=True, double_ai=True, random_first_move=True, alpha_beta=True)
        if result:
            moves.append(result[0])
            times.append(round(result[1], 3))
    print('ab5')
    print('moves', moves)
    print('times', times)
    print('avg_moves', round(sum(moves)/len(moves), 3))
    print('avg_time', round(sum(times)/len(times), 3))

    moves = []
    times = []
    while len(moves) < 5:
        play = GamePlay()
        result = play.play(ai=True, double_ai=True, random_first_move=True, alpha_beta=False)
        if result:
            moves.append(result[0])
            times.append(round(result[1], 3))
    print('mm5')
    print('moves', moves)
    print('times', times)
    print('avg_moves', round(sum(moves) / len(moves), 3))
    print('avg_time', round(sum(times) / len(times), 3))

    moves = []
    times = []
    while len(moves) < 10:
        play = GamePlay()
        result = play.play(ai=True, double_ai=True, random_first_move=True, alpha_beta=True)
        if result:
            moves.append(result[0])
            times.append(round(result[1], 3))
    print('ab10')
    print('moves', moves)
    print('times', times)
    print('avg_moves', round(sum(moves) / len(moves), 3))
    print('avg_time', round(sum(times) / len(times), 3))

    moves = []
    times = []
    while len(moves) < 10:
        play = GamePlay()
        result = play.play(ai=True, double_ai=True, random_first_move=True, alpha_beta=False)
        if result:
            moves.append(result[0])
            times.append(round(result[1], 3))
    print('mm10')
    print('moves', moves)
    print('times', times)
    print('avg_moves', round(sum(moves) / len(moves), 3))
    print('avg_time', round(sum(times) / len(times), 3))

    moves = []
    times = []
    while len(moves) < 20:
        play = GamePlay()
        result = play.play(ai=True, double_ai=True, random_first_move=True, alpha_beta=True)
        if result:
            moves.append(result[0])
            times.append(round(result[1], 3))
    print('ab20')
    print('moves', moves)
    print('times', times)
    print('avg_moves', round(sum(moves) / len(moves), 3))
    print('avg_time', round(sum(times) / len(times), 3))

    moves = []
    times = []
    while len(moves) < 20:
        play = GamePlay()
        result = play.play(ai=True, double_ai=True, random_first_move=True, alpha_beta=False)
        if result:
            moves.append(result[0])
            times.append(round(result[1], 3))
    print('mm20')
    print('moves', moves)
    print('times', times)
    print('avg_moves', round(sum(moves) / len(moves), 3))
    print('avg_time', round(sum(times) / len(times), 3))