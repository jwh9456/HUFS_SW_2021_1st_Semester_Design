'''
Daifugo player backend.
'''
import common as common
import random
import copy
from itertools import product, cycle
import time
random.seed(time.time())
DEBUG = True
import interactive
import html
  # 같은 폴더에 있는 파일
DEBUG = True 

def get_deck(shuffle=False):
    suits = 'CSDH'
    ranks = '34567890JQKA2'

    print("덱을 만들겠습니다.")
    deck = [''.join(c) for c in product(ranks, suits)]  
    # 카드만들기 deck = ['3C', '3S', '3D', '3H', '4C',...,'2H']
    deck.append('BB') # deck에 조커 카드 추가
    if shuffle:
        random.shuffle(deck)

    print("덱이 생성되었습니다.")
    print(deck)
    return deck  # 섞인 deck 반환

def deal(players=4):  # 카드 배분하기
    deck = get_deck(shuffle=True) # 섞인 deck 반환됨.
    hands = tuple(set() for i in range(players))  
    # --> hands=(set(), set(), set(), set())
    players = cycle(hands)  #cycle : 무한반복자
    for card in deck:
        player = next(players)  #next(players) -> 수정
        player.add(card)
        '''
        hands = 
        ({'4H', '4C', '6D', '5C', 'AH', '7C', '5H', '9D', '3S', '0D', 'JC', '8S', 'KS'},
        {'2C', '7D', '7S', '9H', '3C', 'QS', 'AC', 'AS', '5D', '9S', 'AD', '0C', 'QD'},
        {'0S', '4D', '0H', '6H', '6S', '3H', 'KD', '8H', '8C', 'KH', '7H', '6C', 'QH'},
        {'KC', '8D', 'QC', '2H', '4S', '2D', 'JD', '9C', '3D', '2S', 'JH', 'JS', '5S', 'BB'})

        '''
    return hands

def ishachikire(play):  #하치키레 구현
    roundOver = False

    if common.RANKS == common.REV_RANKS: # 혁명 상태에서 8의 value는 7
        for i in range(len(play)):
            if common.card_value(play[i]) == 7:
                roundOver = True
                return roundOver
    elif common.REV == common.ORG_RANKS:  # 기본 상태에서 8의 value는 5
        for i in range(len(play)):
            if common.card_value(play[i]) == 5:
                roundOver = True
                return roundOver

    return roundOver

##class Exception(*args : object)##

class InvalidAction(Exception): # ?? 상속..?
    def __init__(self, reason, call):
        self.reason = reason
        self.call = call
    
    def __str__(self):
        return self.reason


def play_round(hands, players, discard=None, first_player=0, invalid_action='pass'):
    """
    Execute simulation of one round of gameplay.
    """
    if invalid_action not in ['pass', 'raise']: # invalid_action 은 'pass' or 'raise'
        raise ValueError("invalid_action cannot be '{0}'".format(invalid_action))

        # invalid_action이 pass나 raise 가 아닐 겨우 에러를 일으킴.
    
    
    num_players = len(players)  # num_players = 4
    #print("에러 : 플레이어 수와 카드가 분배된 사람의 수가 다릅니다.")
    if len(hands) != num_players:
        print("에러 : 플레이어 수와 카드가 분배된 사람의 수가 다릅니다.")
    assert len(hands) == num_players
    
    # len(hands) != num_players 이면 에러 발생
    
    prev = None #last hand played
    if discard is None:
        # First round played
        # 버려진 카드가 없다면, 첫번째 플레이.
        discard = [[]]
    else:
        # 버려진카드가 있다면, 두 번째 이후 플레이.
        # add an empty list representing the start of a new round
        # 새 라운드의 시작을 나타내는 빈 리스트 추가
        # discard = [[1라운드에서 버려진 카드],[2라운드에서 버려진 카드]...]
        discard.append([])

    #indices = range(num_players)  #indices = range(0,4) ...?? 왜 있는거지?
    pass_count = 0
    last_player=first_player   # 끝낸 사람이 처음으로 다시 시작.
    index = first_player  # index = 처음사람

    while True:
        player = players[index]
        hand = hands[index]
        holding = tuple(len(hands[(index+i)%num_players]) for i in range(num_players)) 
        #3명..?? 4명으로 돌리려면 range(num_players)로 범위 바꾸기
        
        print("각자 가지고 있는 카드의 개수")
        print(holding)

        args = [copy.deepcopy(prev), list(hand), copy.deepcopy(discard), holding]
        #arge =[[이전에 낸 카드],[손에 들고 있는 카드],[버린 카드],(각자 가지고 있는 카드의 개수)] 

        # ..???
        kwargs = dict(valid=common.get_valid_plays, generate=common.generate_plays, 
            is_valid=common.is_valid_play)
        call_str = "play({args[0]},{args[1]},{args[2]},{args[3]})".format(args=args)

        play = interactive.play(prev, hand, discard, holding)
        print("해당 카드를 선택했습니다.")
        print(play)

        if play is not None and len(play) == 4:
            if common.RANKS == common.ORG_RANKS:
                common.RANKS = common.REV_RANKS
            else:
                common.RANKS = common.ORG_RANKS


        """

        try:
            # TODO: Suppress stdout
            # TODO: impose timelimit
            play = interactive.play(prev, hand, discard, holding)
            print("해당 카드를 선택했습니다.")
            print(play)

               
        except Exception as e:
            if DEBUG: print("  {0} failed with exception: '{1}'".format(index, e))
            if invalid_action == 'pass':
                play = None
            elif invalid_action == 'raise':
                raise InvalidAction("player {0} raised {1}: '{2}'".format(index, html.escape(e.__class__.__name__), e), call_str)

        """

        if DEBUG: 
          if play is None:
            print("  {0} ({2} cards) --> {1}".format(index, "pass", len(hands[index])))
          else:
            print("  {0} ({2} cards) --> {1}".format(index, play, len(hands[index])-len(play)))
            #print("버리는 사람의 번호", (남은 카드 수) --> [버리는 카드])

        # need to check a play is a valid play
        if play and frozenset(play) not in map(frozenset,common.generate_plays(hand)):
            #플레이가 None 이 아니고, 낼 수 있는 카드 목록에 없다면,
            if DEBUG: 
                print("  {0} invalid play {1}".format(index, play))

            # Force player to pass if their play is invalid
            if invalid_action=='pass':
                play = None
            elif invalid_action =='raise':
                raise InvalidAction("player {0} attempted invalid play {1}".format(index, play), call_str)
        
        if prev is None:  #전에 낸 카드가 없다면
            if play is None:
                if DEBUG: 
                    print("  {0} passed as first player".format(index))
                if invalid_action=='pass':
                    play = None
                elif invalid_action =='raise':
                    raise InvalidAction("player {0} passed as first player".format(index), call_str)
            
        else: #전에 낸 카드가 있다면
            # need to check a play is valid in the context of the previous play
            # 플레이가 이전 플레이의 맥락에서 유효한지 확인해야합니다.
            if not common.is_valid_play(prev, play):
                if DEBUG: 
                    print("  {0} invalid play {1} -> {2}".format(index, prev, play))
                # Force player to pass if their play is invalid
                if invalid_action=='pass':
                    play = None
                elif invalid_action =='raise':
                    raise InvalidAction("player {0} attempted invalid play {1} -> {2}".format(index, prev, play), call_str)
        
        discard[-1].append(play)
        print("해당 카드를 버립니다.")
        print(discard[-1])
        
        if play is not None and len(play) >= 4:
            if common.REV:
                common.REV = False
            else:
                common.REV = True

        if play is None:  #선택한 게 없으면
            pass_count += 1  # pass_count 한 번 추가
            print("지금까지 {0} 번 pass했습니다.\n".format(pass_count))
        else:       # 선택한 게 있으면
            hand -= set(play) # 카드 버림
            prev = play # prev = 전에 버린 카드
            pass_count = 0 # pass_count 리셋
            last_player = index # 낸 사람이 마지막 사람이 됨.
            
        if play is not None:
            hachikire = ishachikire(play)

        # Assess end of round
        if len(hands[index]) == 0:
            # 손에 든게 없다면
            if DEBUG: print("ROUND OVER: Player {0} wins".format(index))
            # 이김
            return hands, last_player, True, discard
        elif pass_count == num_players:
            # 모두 다 패스한다면
            if DEBUG: print("ROUND OVER: All passed - LP {0}".format(last_player))
            # 마지막으로 낸 사람이 이김
            return hands, last_player, False, discard
        elif prev is not None and prev[-1][0] == '2':
            # 마지막으로 낸 카드가 2라면
            if DEBUG: print("ROUND OVER: 2 played - LP {0}".format(last_player))
            # 마지막 사람이 이김
            return hands, last_player, False, discard
        elif play is not None and hachikire:
            if DEBUG:
                print("ROUND OVER: hachikire - LP {0}".format(last_player))
                return hands, last_player, False, discard

        index = (index+1) % num_players
        print("{0} 번 플레이어로 차례가 넘어갑니다.\n".format(index))
        # index는 다음 플레이어로 +1 


def play_game(players, invalid_action='raise', initial_deal=None):  # invalid_action = 'raise'
    # assert all(callable(p) for p in players)
    # assert는 뒤의 조건이 True가 아니면 AssertError를 발생

    print("::::::::::대부호 게임 시작::::::::::\n")
    print("플레이어 수는 4명으로 고정합니다.\n")


    lp_hist = []  #last player history
    hands_hist = []
    if initial_deal is None:
        print("패를 나누겠습니다.\n")
        initial_deal = deal()
        
        print("나눠진 패는 다음과 같습니다.\n")
        print("player1 :",initial_deal[0])
        print("player2 :",initial_deal[1])
        print("player3 :",initial_deal[2])
        print("player4 :",initial_deal[3])
        print()

    else:
        initial_deal = copy.deepcopy(initial_deal)
        print("지금까지의 각 플레이어의 패의 상황입니다.\n")
        print("player1 :",initial_deal[0])
        print("player2 :",initial_deal[1])
        print("player3 :",initial_deal[2])
        print("player4 :",initial_deal[3])
        print()

     # 적어도 한 번 플레이
    hands_hist.append(copy.deepcopy(initial_deal)) 
    print("게임 시작부터 현재까지의 패의 기록입니다.\n")
    print(hands_hist)
    print()

    print("게임을 시작합니다.\n")
    hands, lp, game_over, discard = play_round(initial_deal, players)   # players 의 type -> tuple (p1,p2,p3,p4)
    print("라운드가 끝났습니다.")
    hands_hist.append(copy.deepcopy(hands))
    lp_hist.append(lp)
    while not game_over:
        print("라운드를 다시 시작합니다.")
        hands, lp, game_over, discard = play_round(hands, players, discard, lp)  #lp : 마지막에 낸 사람
        print("라운드가 끝났습니다.")
        hands_hist.append(copy.deepcopy(hands))
        lp_hist.append(lp)
    return lp_hist, discard, hands_hist

players = ('A','B','C','D')
play_game(players)
