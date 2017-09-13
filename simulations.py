import random
from estimation import *


def simulate_game(player1, player2, W, time_control, verbosity):
    rates = calculate_rates(bayes_estimate(player1, player2, W, time_control))
    u = random.random()
    if u < rates[0]:
        if verbosity == 1:
            print(player1.name + " won")
        return 1
    elif u < rates[0] + rates[1]:
        if verbosity == 1:
            print(player2.name + " won")
        return 0
    else:
        if verbosity == 1:
            print("Draw")
        return 0.5


def simulate_worldcup_match(player1, player2, score, W, verbosity):
    if player1.current_score is not None and player2.current_score is not None:
        score = [player1.current_score, player2.current_score]
    player1.current_score = None
    player2.current_score = None
    current_game = sum(score) + 1

    if current_game == 1:
        if verbosity == 1:            
            print("Game " + str(int(current_game)) + ": Classical")
        player1_score = simulate_game(player1, player2, W, "Classical", verbosity)
        score[0] += player1_score
        score[1] += 1 - player1_score
        return simulate_worldcup_match(player1, player2, score, W, verbosity)

    elif current_game == 2:
        if verbosity == 1:
            print("Game " + str(int(current_game)) + ": Classical")
        player1_score = simulate_game(player1, player2, W, "Classical", verbosity)
        score[0] += player1_score
        score[1] += 1 - player1_score
        if score[0] > score[1]:
            return player1
        if score[0] < score[1]:
            return player2
        return simulate_worldcup_match(player1, player2, score, W, verbosity)

    elif current_game == 3 or current_game == 5:
        if verbosity == 1:
            print("Game " + str(int(current_game)) + ": Rapid")
        player1_score = simulate_game(player1, player2, W, "Rapid", verbosity)
        score[0] += player1_score
        score[1] += 1 - player1_score
        return simulate_worldcup_match(player1, player2, score, W, verbosity)

    elif current_game == 4 or current_game == 6:
        if verbosity == 1:
            print("Game " + str(int(current_game)) + ": Rapid")
        player1_score = simulate_game(player1, player2, W, "Rapid", verbosity)
        score[0] += player1_score
        score[1] += 1 - player1_score
        if score[0] > score[1]:
            return player1
        if score[0] < score[1]:
            return player2
        return simulate_worldcup_match(player1, player2, score, W, verbosity)

    elif current_game == 7:
        if verbosity == 1:
            print("Game " + str(int(current_game)) + ": Blitz")
        player1_score = simulate_game(player1, player2, W, "Blitz", verbosity)
        score[0] += player1_score
        score[1] += 1 - player1_score
        return simulate_worldcup_match(player1, player2, score, W, verbosity)

    elif current_game == 8:
        if verbosity == 1:
            print("Game " + str(int(current_game)) + ": Blitz")
        player1_score = simulate_game(player1, player2, W, "Blitz", verbosity)
        score[0] += player1_score
        score[1] += 1 - player1_score
        if score[0] > score[1]:
            return player1
        if score[0] < score[1]:
            return player2
        return simulate_worldcup_match(player1, player2, score, W, verbosity)

    elif current_game == 9: 
        if verbosity == 1:
            print("Game " + str(int(current_game)) + ": Armageddon!")
        player1_score = simulate_game(player1, player2, W, "Blitz", verbosity)
        score[0] += player1_score
        score[1] += 1 - player1_score
        if score[0] > score[1]:
            return player1
        if score[0] < score[1]:
            return player2
        if score[0] == score[1]:
            winner = random.choice([player1, player2])
            return winner
    
    elif current_game > 9:
        if score[0] > score[1]:
            return player1
        if score[0] < score[1]:
            return player2


def worldcup_match_simulations(player1, player2, W, N, verbosity):   
    winners = []
    current_scores = [player1.current_score, player2.current_score]
    for i in range(N):
        player1.current_score = current_scores[0]
        player2.current_score = current_scores[1]
        winners.append(simulate_worldcup_match(player1, player2, [0,0], W, verbosity))

    for player in [player1, player2]:
        player.wins = winners.count(player)
        player.win_percentage = player.wins/N

    print(player1, player1.win_percentage)
    print(player2, player2.win_percentage)



def simulate_worldcup_round(players, W, verbosity):
    next_round = []
    while True:
        player1 = players.pop(0)
        player2 = players.pop(0)
        if verbosity == 1:
            print("Match " + str(player1) + " vs. " + str(player2))
        winner = simulate_worldcup_match(player1, player2, [0,0], W, verbosity)
        if verbosity == 1:
            print(str(winner) + " won the match")
        next_round.append(winner)
        if len(players) == 0:
            return next_round


def simulate_worldcup(players, current_round, W, verbosity):
    players = players[:]
    while True:
        if verbosity == 1:
            print("----------")
            print("Round " + str(current_round))
            print("----------")
        players = simulate_worldcup_round(players, W, verbosity)
        current_round += 1
        if len(players) == 1:            
            return players[0]


def worldcup_simulations(players, current_round, N, W, verbosity):    
    winners = []
    current_scores = [player.current_score for player in players]
    for i in range(N):
        for player in players:
            player.current_score = current_scores[players.index(player)]
        winners.append(simulate_worldcup(players, current_round, W, verbosity))
        
    for player in players:
        player.wins = winners.count(player)
        player.win_percentage = player.wins/N

    sorted_players = sorted(players, key=lambda x: x.win_percentage, reverse=True)    

    return sorted_players