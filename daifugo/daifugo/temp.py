import random
import copy
from itertools import product, cycle
#random.seed("COMP10001")
import time
random.seed(time.time())
import cgi
DEBUG=False
import common

def get_deck(shuffle=False):
    suits = 'CSDH'
    ranks = '34567890JQKA2'
    deck = [''.join(c) for c in product(ranks, suits)]
    if shuffle:
        random.shuffle(deck)
    deck.append('BB') #'BB' means joker
    return deck

def deal(players=4):
    deck = get_deck(shuffle=True)
    hands = tuple(set() for i in range(players))
    players = cycle(hands)
    for card in deck:
        player = next(players)
        player.add(card)
    return hands

print(deal(4))