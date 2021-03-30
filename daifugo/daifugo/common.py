"""
Common methods used for daifugo playing.
"""
from collections import defaultdict
from itertools import combinations

REV = False

ORG_RANKS = '34567890JQKA2B'
REV_RANKS = '2AKQJ09876543B'

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
    if REV:
        return REV_RANKS.index(card[0])
    return ORG_RANKS.index(card[0])

def straights(cards):   #straights 판단해주는 함수
    cards = sorted(cards, key=card_value)    #rank순으로 카드 정렬 ex) cards = [3H,4H,5H,2H]
    num_cards = len(cards)
    retval = []
    retval_j = []       #조커가 있는 경우 straights의 경우의 수를 넣을 list
    #for i in range(3,6): # straights of len 3 to 5
    i=3
    if num_cards < i:
         # Can't have a straight of length i or more: not enough cards
         return retval
    if 'BB' not in cards:
        for j in range(num_cards-i+1):
             # We check that the difference in values is the same as the
             # length of the straight. NB this only works if cards are unique
             gap = card_value(cards[j+i-1]) - card_value(cards[j]) + 1
             if gap == i:
                 retval.append(cards[j:j+i])
    elif 'BB' in cards: #조커가 있는 경우 straights판단
        for i in range(3, num_cards+1, 1):
        #연속된 세 자리 straights부터해서 카드의 갯수 만큼의 straights판단
            per = permutations(cards, i)  #cards에서 나올 수 있는 모든 순열 경우의 수 계산
            nof = list(per) #nof는 nP3부터 nPn까지의 순열 경우의수가 들어있는 list
            for j in nof: #j는 각각의 순열 튜플
                test = straights_joker(list(j))
                if test :  #j가 straights라면, retval_j에 append
                    retval_j.append(j)
        return retval_j
    return retval

def straights_joker(cards):  #cards는 각각의 순열들
   i = len(cards)
   lrank=list(RANKS)

   if 'BB' in cards:  #조커가 있을 경우
       j = 0
       while j < i-1:
           n1 = cards[j]
           n2 = cards[j+1]
           if n1 == 'BB' and card_value(n2) != 0:   #n1이 조커라면, j를 늘려가면서 다음 카드들의 rank들이 순차적으로
               j+=1                                 #차이 나는 지 확인
               continue
           elif n2 == 'BB':                         #n2가 조커인 경우
               temp = card_value(n1)

               if len(RANKS)-2 != temp:             #조커 앞의 카드가 2(가장강한카드)가 아니라면, 조커자리에 n1보다
                   cards[j+1] = lrank[temp+1]       #한 계단 높은 카드를 삽입하고, 그 뒤의 카드들의 rank 순차적 판단
                   j+=1
                   continue

               else:                                #조커 앞의 카드가 2라면, 조커가 마지막카드라면, True, 아니라면 False
                   if (j+2) == i:
                       return True
                   else:
                       return False
           else:                                     # 둘다 조커가 아니라면 계속해서 rank판단 후 계속 이어가기
               if card_value(n1)+1 == card_value(n2):
                   j +=1
               else:                                 # n1, n2가 rank가 두 단계 이상 차이라면 False
                   return False
       return True
   else:
       j=0
       while j < i-1:
           n1 = cards[j]
           n2 = cards[j + 1]

           if card_value(n1)+1 == card_value(n2):
               j+=1
           else:
               return False
       return True

def generate_plays(hand):                   #내가 낼 수 있는 경우의 수를 plays에 넣어서 return
   """
   Generate all possible plays from a given hand.
   """
   ranked = cards_by_index(hand,0)         #ranked는 리스트형 dic
   plays = []
   # Generate rank combinations
   for rank in ranked:                     #ranked는 key만 돌음
       cards = ranked[rank]                #cards는  같은 숫자 다른 모양들의 각각의 리스트 ex) [3C,3H],[5C,5H]

       if 'BB' in hand and rank !='B' :          #가지고 있는 패에 조커가 있는 지 확인 ['BB','BB']제거
           cards.append('BB')     #조커가 있다면 cards리스트에 각각 append해주기 ex) [3C,3H,BB]

       for n in range(1,5):
           plays.extend(combinations(cards, n))

   plays = list(set(plays))  #combinations함수에서 n=1일때 발생하는 하나 짜리 조커 중복 제거 ex)[B],[B]

   # Generate straights
   suited = cards_by_index(hand,1)
   for suit in suited:
       if 'BB' in hand:
           suited[suit].append('BB')

       plays.extend(straights(suited[suit]))
   return [list(p) for p in plays]

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
