import random
from estimation import *


def simulate_game(player1, player2, W, time_control, verbosity):
    rates = calculate_rates(estimate_score(player1, player2, W, time_control))
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


def simulate_match(player1, player2, W, verbosity):
    if verbosity == 1:
        print("Match " + str(player1) + " vs. " + str(player2))
    score = 0
    # Classical
    if verbosity == 1:
        print("Classical")
    score += simulate_game(player1, player2, W, "Classical", verbosity)
    score += simulate_game(player1, player2, W, "Classical", verbosity)    
    if score > 1:
        return player1
    if score < 1:
        return player2
    
    #Rapid
    if verbosity == 1:
        print("Rapid")
    score += simulate_game(player1, player2, W, "Rapid", verbosity)
    score += simulate_game(player1, player2, W, "Rapid", verbosity)    
    if score > 2:
        return player1
    if score < 2:
        return player2
    
    #Rapid
    if verbosity == 1:
        print("10-minute")
    score += simulate_game(player1, player2, W, "Rapid", verbosity)
    score += simulate_game(player1, player2, W, "Rapid", verbosity)    
    if score > 3:
        return player1
    if score < 3:
        return player2
    
    #Blitz
    if verbosity == 1:
        print("Blitz")
    score += simulate_game(player1, player2, W, "Blitz", verbosity)
    score += simulate_game(player1, player2, W, "Blitz", verbosity)    
    if score > 4:
        return player1
    if score < 4:
        return player2
    
    #Armageddon
    if verbosity == 1:
        print("Armageddon!")
    score += simulate_game(player1, player2, W, "Blitz", verbosity)
    if score == 4:
        return player2
    if score == 5:
        return player1
    if score == 4.5:
        return random.choice([player1, player2])


def match_simulations(player1, player2, W, N, verbosity):
    winners = []
    for i in range(N):
        winners.append(simulate_match(player1, player2, W, verbosity))

    for player in [player1, player2]:
        player.wins = winners.count(player)
        player.win_percentage = player.wins/N

    print(player1, player1.win_percentage)
    print(player2, player2.win_percentage)



def simulate_round(players, W, verbosity):
    next_round = []
    while True:
        player1 = players.pop(0)
        player2 = players.pop(0)
        winner = simulate_match(player1, player2, W, verbosity)
        if verbosity == 1:
            print(str(winner) + " won the match")
        next_round.append(winner)
        if len(players) == 0:
            return next_round


def simulate_cup(players, W, verbosity):
    players = players[:]
    r = 3
    while True:
        if verbosity == 1:
            print("Round " + str(r))
        players = simulate_round(players, W, verbosity)
        r += 1
        if len(players) == 1:            
            return players[0]


def cup_simulations(players, N, W, verbosity):
    winners = []
    for i in range(N):
        winners.append(simulate_cup(players, W, 0))
        
    for player in players:
        player.wins = winners.count(player)
        player.win_percentage = player.wins/N

    sorted_players = sorted(players, key=lambda x: x.win_percentage, reverse=True)    

    return sorted_players