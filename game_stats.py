import sys
import random
import numpy as np
import scipy.stats as ss

game_dict = {
    (1,3,2,4): "Prisoner's Dilemma",
    (1,2,3,4): "Deadlock",
    (2,1,3,4): "Delight",
    (3,1,2,4): "Hero",
    (3,2,1,4): "Battle",
    (2,3,1,4): "Chicken",
    (1,4,2,3): "Stag hunt",
    (1,4,3,2): "Assurance",
    (2,4,3,1): "Coordination",
    (3,4,2,1): "Mixed harmony",
    (3,4,1,2): "Harmony",
    (2,4,1,3): "No conflict"
}


def determine_game(game):
    # print(game)
    row = ss.rankdata(game)
    col = [row[0], row[2], row[1], row[3]]
    row_four = np.argmax(row)
    col_four = np.argmax(col)

    # print(row, col, row_four, col_four)

    if col_four > 1:
        # column's four is in second row, need to flip
        row = [row[2], row[3], row[0], row[1]]
        col = [col[2], col[3], col[0], col[1]]

    if row_four % 2 == 0:
        # row's four is in first column, need to flip
        row = [row[1], row[0], row[3], row[2]]
        col = [col[1], col[0], col[3], col[2]]

    # print(tuple(row))

    return game_dict[tuple(row)]


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: python game_stats.py [game_data.csv] [errors.csv] [n_randomizations]")

    games = []
    errors = []
    lines = []

    with open(sys.argv[1]) as infile:
        infile.readline()
        lines = infile.readlines()

    assert(len(lines) % 2 == 0)

    for i in range(0, len(lines), 2):
        new_game = lines[i].split(",")[1:] + lines[i+1].split(",")[1:] 
        new_game = [float(val.strip()) for val in new_game]
        games.append(new_game)

    with open(sys.argv[2]) as infile:
        infile.readline()
        lines = infile.readlines()

    assert(len(lines) % 2 == 0)

    for i in range(0, len(lines), 2):
        new_err = lines[i].split(",")[1:] + lines[i+1].split(",")[1:] 
        new_err = [float(val.strip()) for val in new_err]
        errors.append(new_err)

    for game_i in range(len(games)):
        game = games[game_i]
        error = errors[game_i]
        game_counts = {}
        for _ in range(int(sys.argv[3])):
            values = [random.gauss(game[pos], error[pos]) for pos in range(4)]
            game_class = determine_game(values)
            if game_class in game_counts:
                game_counts[game_class] += 1
            else:
                game_counts[game_class] = 1

        print(game_counts)