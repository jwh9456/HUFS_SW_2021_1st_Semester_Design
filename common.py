
from collections import defaultdict
from itertools import combinations, permutations
from framework import Card
from operator import attrgetter

RANKS = '???34567890JQKA2B'
DEBUG = False

def cards_by_index(cardset):

    if type(cardset[0]) == list:
        new = []
        for card in cardset[0]:
            new.append(card)
        cardset = new


    retval = defaultdict(list)

    for card in cardset:
        rank = card.rank
        retval[rank].append(card)
    return retval

def cards_by_rank(cardset):
    if type(cardset[0]) == list:
        new = []
        for card in cardset[0]:
            new.append(card)
        cardset = new

    retval = defaultdict(list)

    for card in cardset:
        suit = card.suit
        retval[suit].append(card)

    return retval

def find_joker(hands):
    if type(hands[0]) == list:
        new = []
        for card in hands[0]:
            new.append(card)
        hands = new

    for i in range(len(hands)):
        if hands[i].suit == 'B':
            return True
    return False

def straights(cards):

    num_cards = len(cards)
    retval = []
    retval_j = []
    i = 3

    if num_cards < i:
        return retval  # 손에 쥔 카드 장수가 모자라면 빈 스트레이트를 반환한다.
    for j in range(num_cards - i + 1):
        gap = cards[j + i - 1].rank - cards[j].rank + 1
        if gap == i:
            retval.append(cards[j:j + i])  # 3장짜리 가능한 카드 경우의수를 리턴한다

    if Card(16, 'B') in cards:  # 조커가 있는 경우 straights판단
        # 연속된 세 자리 straights부터해서 카드의 갯수 만큼의 straights판단
        per = permutations(cards, 3)  # cards에서 나올 수 있는 모든 순열 경우의 수 계산
        nof = list(per)  # nof는 nP3부터 nPn까지의 순열 경우의수가 들어있는 list

        for j in nof:  # j는 각각의 순열 튜플
            test = straights_joker(list(j))
            for card in j:
                if card.suit == 'B':
                    card.rank = 16
            if test:  # j가 straights라면, retval_j에 append
                j = list(j)
                for k in range(2):
                    if int(j[k].rank) + 1 != int(j[k + 1].rank):
                        if j[k].suit == 'B':
                            j[k] = Card(j[k+1].rank - 1, 'B')
                        else:
                            j[k + 1] = Card(j[k].rank + 1, 'B')

                j = tuple(j)
                retval_j.append(j)

        return retval_j

    return retval

def straights_joker(cards):  # cards는 각각의 순열들
    i = len(cards)

    if Card(16, 'B') in cards:  # 조커가 있을 경우
        j = 0
        while j < i - 1:
            n1 = cards[j]
            n2 = cards[j + 1]
            if n1.suit == 'B' and n2.rank != 0:  # n1이 조커라면, j를 늘려가면서 다음 카드들의 rank들이 순차적으로
                if n1.rank + 1 == n2.rank:
                    return True
                else:
                    return False
            elif n2.suit == 'B':  # n2가 조커인 경우
                temp = n1.rank

                if temp != 2:  # 조커 앞의 카드가 2(가장강한카드)가 아니라면, 조커자리에 n1보다
                    cards[j + 1].rank = temp + 1 # 한 계단 높은 카드를 삽입하고, 그 뒤의 카드들의 rank 순차적 판단
                    j += 1
                    continue

                else:  # 조커 앞의 카드가 2라면, 조커가 마지막카드라면, True, 아니라면 False
                    if (j + 2) == i:
                        return True
                    else:
                        return False
            else:  # 둘다 조커가 아니라면 계속해서 rank판단 후 계속 이어가기
                if n1.rank + 1 == n2.rank:
                    j += 1
                else:  # n1, n2가 rank가 두 단계 이상 차이라면 False
                    return False
        return True
    else:
        j = 0
        while j < i - 1:
            n1 = cards[j]
            n2 = cards[j + 1]

            if n1.rank + 1 == n2.rank:
                j += 1
            else:
                return False
        return True

def generate_plays(hand):  # 내가 낼 수 있는 경우의 수를 plays에 넣어서 return

    ranked = cards_by_index(hand)  # ranked는 리스트형 dic
    plays = []
    # Generate rank combinations
    for rank in ranked:  # ranked는 key만 돌음
        cards = ranked[rank]  # cards는  같은 숫자 다른 모양들의 각각의 리스트 ex) [3C,3H],[5C,5H]
        if (Card(16, 'B') in hand) and not (Card(16, 'B') in cards):
            cards.append(Card(16, 'B')) #조커가 있다면 cards리스트에 각각 append해주기 ex) [3C,3H,BB]

        for n in range(1, 5):
            plays.extend(combinations(cards, n))

    retval = []

    for play in plays:
        if play in retval:
            continue
        else:
            retval.append(play)

    for i in range(len(retval)):
        if len(retval[i]) != 1 and Card(16, 'B') in retval[i]:
            retval[i] = list(retval[i])
            retval[i][-1] = Card(retval[i][0].rank, 'B')

            retval[i] = tuple(retval[i])

    # Generate straights
    suited = cards_by_index(hand)
    for suit in suited:
        # plays.extend(straights(suited[suit]))
        if Card(16, 'B') in hand and suited[suit][0].rank != 16:
            suited[suit].append(Card(16, 'B'))
        retval.extend(straights(suited[suit]))

    plays = []

    for play in retval:
        if play in plays:
            continue
        else:
            plays.append(play)

    return [list(p) for p in plays]

def is_valid_play(prev, play):
    if play is None:
        return True
    if prev[0].rank != prev[-1].rank:
        # Previous play is a straight
        s = straights(play)
        if len(s) == 0:
            # Proposed play is not a straight
            return False

        max = 0
        for card in prev:
            if max < int(card.rank):
                max = int(card.rank)

        min = 17
        for card in play:
            if min > int(card.rank):
                min = int(card.rank)

        if max >= min:
            # Proposed play does not have a higher max card
            return False
        else:
            return True
    else:
        length = 0
        pl = []

        for p in play:
            pl.append(p)
            length = len(pl)

        if len(play) != len(prev):
            return False
        elif length != 1:
            return False
        elif int(play[0].rank) <= int(prev[0].rank):
            # Proposed play is not worth more than prev
            if Card(16, 'B') in play:
                if play[0].rank <= prev[0].rank:
                    return False
                else:
                    return True
            return False
        else:
            return True

def get_valid_plays(hand, prev, generate=generate_plays, is_valid=is_valid_play):
    return [p for p in generate(hand) if is_valid(prev, p)]
