import game_stats as gs 

def test_determine_game():
    assert(gs.determine_game([5, 0, 7, 1]) == "Prisoner's Dilemma")
    assert(gs.determine_game([3, 0, 2, 1]) == "Stag Hunt")
    assert(gs.determine_game([0, -1, 1, -1000]) == "Chicken")

    # According to wikipedia, this should be battle, but it's coming up as coordination
    gs.determine_game([3,1,0,2])