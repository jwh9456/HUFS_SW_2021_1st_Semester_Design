"""
Common methods used for daifugo playing.
"""
from collections import defaultdict
from itertools import combinations
RANKS = '34567890JQKA2B'
REV_RANKS = "2AKQJ09876543B"

def cards_by_index(cardset, index):
    """
    Organize cards by rank (index 0) or suit (index 1)
    """
    retval = defaultdict(list)
    for card in cardset:
        rank = card[index]
        retval[rank].append(card)
    return retval

def card_value(card):
    """
    Return an index value that can be used for comparing cards
    """
    return RANKS.index(card[0])

def straights(cards):
    """
    Generate all possible staights from a group of cards
    """
    cards = sorted(cards, key=card_value)
    num_cards = len(cards)
    retval = []
    i = 3
    if num_cards < i:
        # Can't have a straight of length i or more: not enough cards
        return retval #손에 쥔 카드 장수가 모자라면 빈 스트레이트를 반환한다.
    for j in range(num_cards-i+1):
        # We check that the difference in values is the same as the
        # length of the straight. NB this only works if cards are unique
        gap = card_value(cards[j+i-1]) - card_value(cards[j]) + 1 #계단은 3장으로 제한하고, 어차피 card_Value가 B를 가장 쎈걸로 반환하니까 딱히 조커를 추가할 필요는 없을듯?
        if gap == i:
            retval.append(cards[j:j+i]) #3장짜리 가능한 카드 경우의수를 리턴한다
    return retval

def generate_plays(hand):
    """
    Generate all possible plays from a given hand.
    """
    ranked = cards_by_index(hand,0)
    plays = []
    # Generate rank combinations
    for rank in ranked:
        cards = ranked[rank]
        for n in range(1,3):
            plays.extend(combinations(cards, n))
    # Generate straights
    suited = cards_by_index(hand,1)
    for suit in suited:
        plays.extend(straights(suited[suit]))
    return [list(p) for p in plays]

def is_valid_play(prev, play, debug=False):
    """
    Determine if a play is valid given a previous play
    """
    if play is None:
        # it is always ok to pass
        return True
    if card_value(prev[0]) != card_value(prev[-1]):
        # Previous play is a straight
        s = straights(play)
        if len(s) == 0:
            # Proposed play is not a straight
            if debug: print ("INVALID: {0} is not a straight").format(play)
            return False
        if card_value(max(prev, key=card_value)) >= card_value(max(play, key=card_value)):
            # Proposed play does not have a higher max card
            if debug: 
                print ("INVALID: {0} does not have higher max card").format(play)
                print ("prev:{0} play:{1}").format(max(prev, key=card_value), max(play, key=card_value))
            return False
        else:
            return True
    else:
        # Previous play is a rankset
        if len(play) != len(prev):
            # Wrong number of cards
            if debug: print ("INVALID: {0} has wrong number of cards").format(play)
            return False
        elif len(set(p[0] for p in play)) != 1:
            # Proposed play has cards of mixed rank
            if debug: print ("INVALID: {0} of mixed rank").format(play)
            return False
        elif card_value(play[0]) <= card_value(prev[0]):
            # Proposed play is not worth more than prev
            if debug: print ("INVALID: {0} not worth more").format(play)
            return False
        else:
            return True

def get_valid_plays(prev, hand, generate=generate_plays, is_valid=is_valid_play):
    """
    Produce a list of valid plays given a previous play and a current hand.
    """
    return [ p for p in generate(hand) if is_valid(prev, p) ]


