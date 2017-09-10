from lxml import html
import requests

"""
Functions for extracting player ratings from ratings.fide.com.
"""

def get_fide_tree(player):
    page = requests.get('http://ratings.fide.com/card.phtml?event=' + player.fide_id)
    tree = html.fromstring(page.content)
    
    return tree


def assign_rating(player):
    tree = get_fide_tree(player)
    player.rating = int(tree.xpath('//table//tr//td[@width="33%"]/text()')[1].replace('\n',''))
    try:
        player.rapid = int(tree.xpath('//table//tr//td//font/text()')[0])
    except:
        player.rapid = None
    try:
        player.blitz = int(tree.xpath('//table//tr//td//font/text()')[1])
    except:
        player.blitz = None


def scrape_ratings(players):
    for player in players:
        assign_rating(player)