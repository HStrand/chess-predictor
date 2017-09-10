from lxml import html
import requests

"""
Functions for extracting head-to-head scores between players from chessgames.com.
"""

def get_chessgames_tree(player1, player2):
    name1 = player1.name.replace(" ", "+")
    name2 = player2.name.replace(" ", "+")
    page = requests.get('http://www.chessgames.com/perl/chess.pl?yearcomp=exactly&year=&playercomp=either&pid=&player=' + name1 + '&pid2=&player2=' + name2 + '&movescomp=exactly&moves=&opening=&eco=&result=')
    tree = html.fromstring(page.content)
    
    return tree


def get_scores(player1, player2):
    tree = get_chessgames_tree(player1, player2)
    classical_winner = tree.xpath('//tr//td//a/text()')[13]
    classical_loser = tree.xpath('//tr//td//a/text()')[14]
    classical_score_text = " " + classical_winner + " beat " + classical_loser + tree.xpath('//tr//td/text()')[7]
    rapid_blitz_score_text = tree.xpath('//tr//td//font/text()')[28]    
    
    return classical_score_text, rapid_blitz_score_text


def assign_scores(player1, player2, score_text, time_control):
    score_list = score_text.split(' ')
    
    # If the players haven't played each other at this format, we won't find the text with the score
    if score_text.find(player1.name) == -1:
        player1.scores[time_control][player2] = [0,0,0]
        player2.scores[time_control][player1] = [0,0,0]
        return
    if score_text.find(player2.name) == -1:
        player1.scores[time_control][player2] = [0,0,0]
        player2.scores[time_control][player1] = [0,0,0]
        return
    
    if score_text.find(player1.name) < score_text.find(player2.name):
        winner = player1
        loser = player2
    elif score_text.find(player1.name) > score_text.find(player2.name):
        winner = player2
        loser = player1
    
    score = [int(s) for s in score_text.replace('.','').replace(',','').split() if s.isdigit()]

    if len(score) == 2:
        score.append(0)
    
    elif len(score) == 0:
        score = [0,0,0]
    
    reverse_score = score[:]
    reverse_score[0], reverse_score[1] = reverse_score[1], reverse_score[0]
    
    winner.scores[time_control][loser.name] = score    
    loser.scores[time_control][winner.name] = reverse_score


def score_players(player1, player2):
    try:
        classical_score_text, rapid_blitz_score_text = get_scores(player1, player2)
    except:
        player1.scores["Classical"][player2.name] = [0,0,0]
        player2.scores["Classical"][player1.name] = [0,0,0]
        player1.scores["RapidBlitz"][player2.name] = [0,0,0]
        player2.scores["RapidBlitz"][player1.name] = [0,0,0]
        return
    assign_scores(player1, player2, classical_score_text, "Classical")
    assign_scores(player1, player2, rapid_blitz_score_text, "RapidBlitz")


def scrape_scores(players):
    for player1 in players:
        for player2 in players:
            print("Fetching head-to-head score between " + player1.name + " and " + player2.name)
            score_players(player1, player2)