import sys
import random
import numpy as np
import scipy.stats as ss
import pandas as pd

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


def get_uv(game):
    # print(game)

    R,S,T,P = game

    if R < P:
        R,S,T,P = P,T,S,R

    U = (S - P) / (R - P)
    V = (T - P) / (R - P)

    # print(R,S,T,P,U,V)

    return U, V

def get_data(game_file, std_file):
    games = []
    errors = []
    lines = []

    with open(game_file) as infile:
        infile.readline()
        lines = infile.readlines()

    assert(len(lines) % 2 == 0)

    for i in range(0, len(lines), 2):
        new_game = lines[i].split(",")[1:] + lines[i+1].split(",")[1:] 
        new_game = [float(val.strip()) for val in new_game]
        games.append(new_game)

    with open(std_file) as infile:
        infile.readline()
        lines = infile.readlines()

    assert(len(lines) % 2 == 0)

    for i in range(0, len(lines), 2):
        new_err = lines[i].split(",")[1:] + lines[i+1].split(",")[1:] 
        new_err = [float(val.strip()) for val in new_err]
        errors.append(new_err)

    return games, errors


def simulate_games(games, errors, n):
    Us = []
    Vs = []
    condition_list = []
    label_list = []

    for game_i in range(len(games)):
        game = games[game_i]
        error = errors[game_i]
        game_counts = {}
        for _ in range(n):
            values = [random.gauss(game[pos], error[pos]) for pos in range(4)]
            game_class = determine_game(values)
            label_list.append(game_class)
            u, v = get_uv(values)
            Us.append(u)
            Vs.append(v)
            condition_list.append(game_i)
 
    df = pd.DataFrame({"U": Us, "V": Vs, "Condition": condition_list, "Label":label_list})

    return df, game_counts

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Usage: python game_stats.py [game_data.csv] [errors.csv] [n_randomizations]")

    games, errors = get_data(sys.argv[1], sys.argv[2])
    uv_df, game_counts = simulate_games(games, errors, int(sys.argv[3]))
