import random
import pandas as pd
from simulations import calculate_rates, bayes_estimate


def game(player1, player2, rating_weight, time_control, verbosity):
    rates = calculate_rates(bayes_estimate(player1, player2, rating_weight, time_control))
    u = random.random()
    if u < rates[0]:
        if verbosity == 2:
            print(player1.name + " won")
        return 1
    elif u < rates[0] + rates[1]:
        if verbosity == 2:
            print(player2.name + " won")
        return 0
    else:
        if verbosity == 2:
            print("Draw")
        return 0.5


class Tournament:

    def __init__(self, players, rating_weight, verbosity):
        self.players = players
        self.verbosity = verbosity
        self.rating_weight = rating_weight
        self.player_dict = playerdict = {player.name: player for player in players}

    def get_sorted_players(self):
        return sorted(self.players, key=lambda x: x.win_percentage, reverse=True)
        
    def print_results(self):
        for player in self.get_sorted_players():
            print(player, round(player.win_percentage*100, 3), "%")

    def plot_results(self, title=""):
        import matplotlib
        import matplotlib.pyplot as plt
        import seaborn as sns
        names = [player.name.split(" ")[-1] for player in self.players]

        win_percentages = [player.win_percentage for player in self.players]
        player_df = pd.DataFrame({"Name": names, "Win percentage": win_percentages})

        matplotlib.rcParams['figure.figsize'] = (16, 10)
        matplotlib.rcParams['font.size'] = 40
        sns.barplot(x="Name", y="Win percentage", data=player_df[player_df["Win percentage"]>0.01]).set_title(title)


class Swiss(Tournament):

    def __init__(self, players, rounds, rating_weight, verbosity):
        super().__init__(players, rating_weight, verbosity)
        self.rounds = rounds


class Dutch(Swiss):

    def __init__(self, players, rounds, rating_weight, verbosity):
        super().__init__(players, rounds, rating_weight, verbosity)


class Monrad(Swiss):

    def __init__(self, players, rounds, rating_weight, verbosity):
        super().__init__(players, rounds, rating_weight, verbosity)


class AcceleratedSwiss(Swiss):

    def __init__(self, players, rounds, rating_weight, verbosity):
        super().__init__(players, rounds, rating_weight, verbosity)


class RoundRobin(Tournament):

    def __init__(self, players, rounds, rating_weight, verbosity):
        super().__init__(players, rating_weight, verbosity)
        self.rounds = rounds


class Cup(Tournament):
    
    def __init__(self, players, rating_weight, verbosity):
        super().__init__(players, rating_weight, verbosity)

"""
This class contains the pairing format of the FIDE World Cup.
Knockout matches are played as follows:
1. 2 classical games
2. If undecided, 2 rapid games
3. If undecided, 2 more rapid games
4. If undecided, 2 blitz games
5. If undecided, an armageddon game
"""
class WorldCup(Cup):

    def __init__(self, players, rating_weight, verbosity):
        super().__init__(players, rating_weight, verbosity)

    def match(self, player1, player2, score, final=False):
        if isinstance(player1, str):
            player1 = self.player_dict[player1]
        if isinstance(player2, str):
            player2 = self.player_dict[player2]

        if player1.current_score is not None and player2.current_score is not None:
            score = [player1.current_score, player2.current_score]
        player1.current_score = None
        player2.current_score = None
        current_game = int(sum(score) + 1)

        if current_game > 9:
            if self.verbosity > 1:
                print("Match has ended")
            if score[0] > score[1]:
                return player1
            elif score[0] < score[1]:
                return player2
            else:
                return random.choice([player1, player2])

        game_formats = ["Classical", "Classical", "Rapid", "Rapid", "Rapid", "Rapid", "Blitz", "Blitz", "Blitz"]
        match_ends = [False, True, False, True, False, True, False, True, True]
        if final:
            game_formats = ["Classical", "Classical"] + game_formats
            match_ends = [False, False] + match_ends

        if self.verbosity > 1:
            print("Game " + str(current_game) + ": " + game_formats[current_game-1])
        player1_score = game(player1, player2, self.rating_weight, game_formats[current_game-1], self.verbosity)
        score[0] += player1_score
        score[1] += 1 - player1_score

        if match_ends[current_game-1]:
            if score[0] > score[1]:
                return player1
            if score[0] < score[1]:
                return player2

        if current_game == 9 and score[0] == score[1]:
            return random.choice([player1, player2])

        else:
            return self.match(player1, player2, score, final)
    
    def matches(self, player1, player2, N):
        if isinstance(player1, str):
            player1 = self.player_dict[player1]
        if isinstance(player2, str):
            player2 = self.player_dict[player2]
            
        winners = []
        current_scores = [player1.current_score, player2.current_score]
        for i in range(N):
            winners.append(self.match(player1, player2, [0,0]))
            player1.current_score = current_scores[0]
            player2.current_score = current_scores[1]

        for player in [player1, player2]:
            player.wins = winners.count(player)
            player.win_percentage = player.wins/N

        if self.verbosity > 0:
            print(player1, player1.win_percentage)
            print(player2, player2.win_percentage)

    def cup_round(self, players, final=False):
        next_round = []
        while True:
            player1 = players.pop(0)
            player2 = players.pop(0)
            if self.verbosity > 1:
                print("Match " + str(player1) + " vs. " + str(player2))
            winner = self.match(player1, player2, [0,0], final)
            if self.verbosity > 1:
                print(str(winner) + " won the match")
            next_round.append(winner)
            if len(players) == 0:
                return next_round   

    def cup(self):
        current_round = 1
        players = self.players[:]
        while True:
            if self.verbosity > 1:
                print("----------")
                print("Round " + str(current_round))
                print("----------")
            if len(players) == 2:
                players = self.cup_round(players, True)
            else:
                players = self.cup_round(players)
            current_round += 1
            if len(players) == 1:            
                return players[0] 

    def cups(self, N):    
        players = self.players[:]
        winners = []
        current_scores = [player.current_score for player in players]
        for i in range(N):
            for player in players:
                player.current_score = current_scores[players.index(player)]
            winners.append(self.cup())
        
        for player in players:
            player.current_score = current_scores[players.index(player)]
            player.wins = winners.count(player)
            player.win_percentage = player.wins/N