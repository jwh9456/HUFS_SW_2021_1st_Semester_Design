"""
Common methods used for daifugo playing.
"""
from collections import defaultdict
from itertools import combinations,permutations

RANKS = '34567890JQKA2B'
REV = False


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
    return RANKS.index(card[0])

def straights(cards):
    cards = sorted(cards, key=card_value)
    num_cards = len(cards)
    retval = []
    retval_j = []
    i = 3
    if num_cards < i:
        return retval  # 손에 쥔 카드 장수가 모자라면 빈 스트레이트를 반환한다.
    for j in range(num_cards - i + 1):
        gap = card_value(cards[j + i - 1]) - card_value(cards[j]) + 1
        # 계단은 3장으로 제한하고, 어차피 card_Value가 B를 가장 쎈걸로 반환하니까 딱히 조커를 추가할 필요는 없을듯?
        if gap == i:
            retval.append(cards[j:j + i])  # 3장짜리 가능한 카드 경우의수를 리턴한다
    if 'BB' in cards:                         #조커가 있는 경우 straights판단
                                              #연속된 세 자리 straights부터해서 카드의 갯수 만큼의 straights판단
        per = permutations(cards, 3)          #cards에서 나올 수 있는 모든 순열 경우의 수 계산
        nof = list(per)                       #nof는 nP3부터 nPn까지의 순열 경우의수가 들어있는 list


        for j in nof:             #j는 각각의 순열 튜플
            test = straights_joker(list(j))
            if test:               #j가 straights라면, retval_j에 append
                j = list(j)
                for k in range(2):
                    if card_value(j[k]) + 1 != (card_value(j[k + 1])):
                        if j[k] == 'BB':
                            j[k] = str(RANKS[card_value(j[k+1])-1]) +'B'
                        else:
                            j[k+1] = str(RANKS[card_value(j[k])+1]) + 'B'

                j = tuple(j)
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
           cards.append('BB')                     #조커가 있다면 cards리스트에 각각 append해주기 ex) [3C,3H,BB]
                                                  
       for n in range(1,5):
           plays.extend(combinations(cards, n))

   plays = list(set(plays))  #combinations함수에서 n=1일때 발생하는 하나 짜리 조커 중복 제거 ex)[B],[B]

   for i in range(len(plays)):

       if len(plays[i]) != 1 and 'BB' in plays[i]:
           plays[i] = list(plays[i])
           plays[i][-1] = plays[i][0][0]+'B'

           plays[i]=tuple(plays[i])


   # Generate straights
   suited = cards_by_index(hand,1)
   for suit in suited:
       #plays.extend(straights(suited[suit]))
       if 'BB' in hand:
           suited[suit].append('BB')
       plays.extend(straights(suited[suit]))
    
   #plays = list(set(plays)) 이걸 추가해서 중복제거를 하고 싶은데.. 이걸 넣으면 unhashable type: 'list' 이런거 떠서.. 문제
  
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
            if debug: print("INVALID: {0} is not a straight".format(play))
            return False
        if card_value(max(prev, key=card_value)) >= card_value(min(play, key=card_value)):
            # Proposed play does not have a higher max card
            if debug:
                print("INVALID: {0} does not have higher max card".format(play))
                print("prev:{0} play:{1}".format(max(prev, key=card_value), max(play, key=card_value)))
            return False
        else:
            return True
    else:
        # Previous play is a rankset
        if len(play) != len(prev):
            # Wrong number of cards
            if debug: print("INVALID: {0} has wrong number of cards".format(play))
            return False
        elif len(set(p[0] for p in play)) != 1:
            # Proposed play has cards of mixed rank
            if debug: print("INVALID: {0} of mixed rank".format(play))
            return False
        elif card_value(play[0]) <= card_value(prev[0]):
            # Proposed play is not worth more than prev
            if 'BB' in play:
                if card_value(play[0]) <= card_value(prev[0]):
                    if debug: print("INVALID: {0} not worth more".format(play))
                    return False
                else:
                    return True

            if debug: print("INVALID: {0} not worth more".format(play))
            return False
        
        else:
            return True

def get_valid_plays(prev, hand, generate=generate_plays, is_valid=is_valid_play):
    """
    Produce a list of valid plays given a previous play and a current hand.
    """
    return [ p for p in generate(hand) if is_valid(prev, p) ]


