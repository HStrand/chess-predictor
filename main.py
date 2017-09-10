import pandas as pd
from player import Player
from ratingscraper import *
from scorescraper import *
from estimation import *


W = 10 # weight of prior distribution in Bayes estimate

print("Reading players with FIDE IDs")
df = pd.read_csv('players.csv')
players = []

for x in df.iterrows():
    players.append( Player(x[1][0], x[1][1]))

print("Scraping ratings")
scrape_ratings(players)

print(players)

print("Scraping scores")
scrape_scores(players)

print("Estimating score between " + str(players[4] + " and " + str(players[23])))

rates = calculate_rates(estimate_score(players[4], players[23], W, "Blitz"))
print(rates)