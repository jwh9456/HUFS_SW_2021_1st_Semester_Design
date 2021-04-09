from collections import defaultdict
from itertools import combinations
RANKS = '34567890JQKA2B'

def card_value(card):
    return RANKS.index(card[0])

def straights(cards):
    cards = sorted(cards, key=card_value)
    num_cards = len(cards)
    retval = []
    for i in range (3, 6):
        if num_cards < i:
            break
        for j in range(num_cards-i+1):
            gap = card_value(cards[j+i-1]) - card_value(cards[j]) + 1
            if gap == i:
                retval.append(cards[j:j+i])
    return retval

def is_valid_play(prev, play, debug=False):
    if play is None:
        return True

    if card_value(prev[0]) == 13:
        if (card_value(prev[1]) != card_value(prev[-1])):
            idx = card_value(prev[1])
            prev[0] = list(RANKS[idx-1])
        else:
            idx = card_value(prev[1])
            prev[0] = list(RANKS[idx])

    elif card_value(prev[-1]) == 13:
        if (card_value(prev[0]) != card_value(prev[1])):
            idx = card_value(prev[-2])
            prev[-1] = list(RANKS[idx+1])
        else:
            idx = card_value(prev[0])
            prev[-1] = list(RANKS[idx])

    if card_value(prev[0]) != card_value(prev[-1]):
        s = straights(play)
        if len(s) == 0:
            if debug:
                print("INVALID: {0} is not a straight".format(play))
            return False
        if card_value(max(prev, key=card_value)) >= card_value(max(play, key=card_value)):
            if debug:
                print("INVALID: {0} does not have higher max card".format(play))
                print("prev: {0} play: {1}".format(max(prev, key=card_value), max(play, key=card_value)))
            return False
        else:
            return True
            
    else:
        if len(play) != len(prev):
            if debug:
                print("INVALID: {0} has wrong number of cards".format(play))
            return False
        elif len(set(p[0] for p in play)) != 1:
            if debug:
                print("INVALID: {0} of mixed rank".format(play))
            return False
        elif card_value(play[0]) <= card_value(prev[0]):
            if debug:
                print("INVALID: {0} not worth more".format(play))
            return False

        else:
            return True




if card_value(prev[0]) == 13:
    if (card_value(prev[1]) != card_value(prev[-1])):
        idx = card_value(prev[1])
        prev[0] = list(RANKS[idx-1])
    else:
        idx = card_value(prev[1])
        prev[0] = list(RANKS[idx])

elif card_value(prev[-1]) == 13:
    if (card_value(prev[0]) != card_value(prev[1])):
        idx = card_value(prev[-2])
        prev[-1] = list(RANKS[idx+1])
    else:
        idx = card_value(prev[0])
        prev[-1] = list(RANKS[idx])


print(prev)