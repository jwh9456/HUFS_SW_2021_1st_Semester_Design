from collections import defaultdict
from itertools import combinations
import daifugo.common as common


REV = common.REV
ORG_RANKS = '34567890JQKA2B'
REV_RANKS = '2AKQJ09876543B'

def cards_by_index(cardset, index):
    retval = defaultdict(list)       #카드 분류.. 같은 숫자가 3개 잇으면 머가 3개 잇는지 알려줌
    for card in cardset:
        rank = card[index]
        retval[rank].append(card)
    return retval

def card_value(card):
    if REV:
        return REV_RANKS.index(card[0])
    return ORG_RANKS.index(card[0]) #카드의 rank를 알려줌

def straightsJoker(cards): #player가 조커를 가지고 있을 경우 straigth 가능한 수 알려주는 함수

    cards = sorted(cards, key=card_value) #카드 value 순으로 오름차순 정렬
    print(cards)
    num_cards = len(cards)
    retval = []

    #straight를 3장만 낼 수 있다고 정했기 때문에 3으로 고정이라 첫 for문 삭제

    if num_cards < 3:
        return retval

    for i in range(num_cards-2):
        if card_value(cards[i+2]) - card_value(cards[i]) + 1 == 3 and card_value(cards[i+2]) != 13: #조커 있지만 스트레이트인 경우
            retval.append(cards[i:i+3])
        if card_value(cards[i+1]) - card_value(cards[i]) + 1 == 3: #바로 옆이 2단계 위인 경우 조커 가운데로
            straight = []
            straight.append(cards[i])
            straight.append(cards[-1])
            straight.append(cards[i+1])
            retval.append(straight)
        if card_value(cards[i+1]) - card_value(cards[i]) + 1 == 2: #바로 옆이 한단계 위인 경우 조커가 양 옆에 올 수 있음
            if card_value(cards[i]) == 0:
                straight = []
                straight.append(cards[i])
                straight.append(cards[i + 1])
                straight.append(cards[-1])
                retval.append(straight)
            elif card_value(cards[i+1]) == 12:
                straight = []
                straight.append(cards[-1])
                straight.append(cards[i])
                straight.append(cards[i + 1])
                retval.append(straight)
            else:
                straight = []
                straight.append(cards[-1])
                straight.append(cards[i])
                straight.append(cards[i + 1])
                retval.append(straight)
                straight = []
                straight.append(cards[-1])
                straight.append(cards[i])
                straight.append(cards[i + 1])
                retval.append(straight)

    return retval


cards = ['3', '4', '8', 'B', 'A', '0']
joker = cards_by_index(cards, 0)


for elem in straightsJoker(joker):
    print(">", end= "")
    print(elem)

"""
print("/* 혁명 */")
REV = True
for elem in straightsJoker(joker):
    print(elem)
"""
'''
['5', '6', 'B']
['B', '5', '6']
['6', 'B', '8']
['8', '9', '0']
['8', '9', 'B']
['B', '8', '9']
['9', '0', 'B']
['B', '9', '0']
/* 혁명 */
['0', '9', '8']
['0', '9', 'B']
['B', '0', '9']
['9', '8', 'B']
['B', '9', '8']
['8', 'B', '6']
['6', '5', 'B']
['B', '6', '5']
'''