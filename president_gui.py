from copy import copy
from operator import attrgetter
import random
import common
import pygame
import time

from framework import GameState, ismcts, Deck

CLEAN_PACK = Deck().cards


class PresidentGameState(GameState):

    def __init__(self):
        GameState.__init__(self)
        self.player_to_move = 0
        self.player_hands = [[], [], [], []]
        self.discards = []
        self.on_the_table = []
        self.pass_count = 0

    def clone(self):
        st = PresidentGameState()
        st.player_to_move = self.player_to_move
        st.player_hands = [copy(self.player_hands[0]), copy(self.player_hands[1]), copy(self.player_hands[2]), copy(self.player_hands[3])]
        st.discards = copy(self.discards)
        st.on_the_table = copy(self.on_the_table)
        st.pass_count = copy(self.pass_count)

        return st

    def clone_and_randomize(self, observer):

        st = self.clone()

        flattened_current_trick = [a for b in st.on_the_table for a in b]
        seen_cards = st.player_hands[observer] + st.discards + flattened_current_trick

        unseen_cards = [card for card in CLEAN_PACK
                        if card not in seen_cards]

        random.shuffle(unseen_cards)

        for p in (0, 1, 2, 3):
            if p != observer:
                num_cards = 52 - len(st.discards) - len(st.player_hands[observer])

                st.player_hands[p] = sorted(unseen_cards[:num_cards],
                                            key=attrgetter('rank', 'suit'))

        return st

    def get_next_player(self, p):
        return (p + 1) % self.number_of_players

    def _deal(self):

        deck = Deck()
        deck.shuffle()

        # Player zero gets the first 13 cards
        self.player_hands[0] = sorted(deck.cards[:13],
                                      key=attrgetter('rank', 'suit'))

        # Player one gets the last 13 cards
        self.player_hands[1] = sorted(deck.cards[13:26],
                                      key=attrgetter('rank', 'suit'))

        # Player one gets the last 13 cards
        self.player_hands[2] = sorted(deck.cards[26:39],
                                      key=attrgetter('rank', 'suit'))

        # Player one gets the last 13 cards
        self.player_hands[3] = sorted(deck.cards[-13:],
                                      key=attrgetter('rank', 'suit'))

    def do_move(self, move):

        if move == "PASS":
            if self.pass_count >= 3:
                self.discards.extend([a for b in self.on_the_table for a in b])
                self.on_the_table = []
                self.player_to_move = self.get_next_player(self.player_to_move)
                self.pass_count = 0
            else:
                self.player_to_move = self.get_next_player(self.player_to_move)
                self.pass_count += 1
        else:
            self.pass_count = 0
            self.on_the_table.append(move)

            for card in move:
                if card in self.player_hands[self.player_to_move]:
                    self.player_hands[self.player_to_move].remove(card)

            if self.player_hands[self.player_to_move]:
                self.player_to_move = self.get_next_player(self.player_to_move)

    def get_moves(self):

        hand = sorted(self.player_hands[self.player_to_move],
                      key=attrgetter('rank', 'suit'))
        if not hand:
            # If there are no moves left, then return the empty list.
            return hand
        else:
            if not self.on_the_table:
                candidate_cards = common.generate_plays(hand)
            else:
                candidate_cards = common.get_valid_plays(hand, self.on_the_table[-1])

            moves = []

            for cards in candidate_cards:
                moves.append(cards)

            return moves + ["PASS"]

    def get_result(self, player):
        return 1 if not self.player_hands[player] else 0

    def __repr__(self):
        result = "P%i: %s Trick: %s Discards: %s" % (
            self.player_to_move,
            self.player_hands[self.player_to_move],
            self.on_the_table,
            self.discards)
        return result

def play_self():
    # Margins
    MARGIN_LEFT = 380
    MARGIN_TOP = 200
 
    # WINDOW SIZE
    WIDTH = 900
    HEIGHT = 460
 
    # COLORS
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (110, 110, 110)
    BLUE = (0,0,255)

    # Initializing PyGame
    pygame.init()
 
    # Setting up the screen and background
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(GRAY)
 
    # Setting up caption
    pygame.display.set_caption("Daifugo")
 
    # Types of fonts to be used
    small_font = pygame.font.SysFont('Arial', 40)
    large_font = pygame.font.SysFont('Arial', 60)

    over = False

    print_card1 = pygame.image.load(r'./cards/' + 'back' + '.png')
    print_card2 = pygame.image.load(r'./cards/' + 'back' + '.png')
    print_card3 = pygame.image.load(r'./cards/' + 'back' + '.png')
    print_card4 = pygame.image.load(r'./cards/' + 'back' + '.png')
    

    while True:
        # Tracking the mouse movements
        mouse = pygame.mouse.get_pos()
 
        # Loop events occuring inside the game window 
        for event in pygame.event.get():
 
            # Qutting event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if not over:

                state = PresidentGameState()
                state._deal()

                while state.get_moves():
                    #print(str(state))
                    # Use different numbers of iterations (simulations, tree nodes) for different players
                    if state.player_to_move == 0:
                        player_name = "MCTS"
                        m,v,w = ismcts(rootstate=state, itermax=70, verbose=False)

                        if v!=0:
                            mcts_winningRate = w/v*100
                        else:
                            mcts_winningRate = 0
                        
                        print("Best Move: " + str(m) + "\n")

                    elif state.player_to_move in [1, 2, 3]:
                        cards = state.get_moves()
                        
                        for card in cards:
                            print(card, end = " ")
                        player_name = "RANDOM"
                        m = random.choice(cards)
                        
                        print("\nrandom Move: " + str(m) + "\n")
            
                    # elif state.player_to_move == 3:
                    #     cards = state.get_moves()
                        
                    #     for card in cards:
                    #         print(card, end=" ")
                        
                    #     if len(cards) == 1 and cards[0] == 'PASS':
                    #         m = 'PASS'
                    #     else:
                    #         m = cards[0]
                    #     player_name = "SMALL"

                    #     print("\nsmallest Move: " + str(m) + "\n")
            
                    # elif state.player_to_move == 0:
                    #     cards = state.get_moves()
                        
                    #     for card in cards:
                    #        print(card, end=" ")
                        
                    #     if len(cards) == 1 and cards[0] == 'PASS':
                    #         m = 'PASS'
                    #     else:
                    #         m = cards[-2]
                            
                    #     player_name = "LARGE"

                    #     print("\nlargest Move: " + str(m) + "\n")
            
                    if m != 'PASS':
                        for card in m:
                            if card.suit == 'B':
                                card.rank = 16
                    if m != 'PASS':            
                        card_num = len(m)
                        if card_num == 1:
                            print_card1 = pygame.image.load(r'./cards/' + str(m[0].rank) + m[0].suit + '.png')
                            print_card2 = pygame.image.load(r'./cards/' + 'back' + '.png')
                            print_card3 = pygame.image.load(r'./cards/' + 'back' + '.png')
                            print_card4 = pygame.image.load(r'./cards/' + 'back' + '.png')
                            Rank1 = m[0].rank
                            Suit1 = m[0].suit

                            if m[0].rank == 14:
                                Rank1 = "A"
                            elif m[0].rank == 15:
                                Rank1 = 2
                            elif m[0].rank == 16:
                                Rank1 = "JOKER"
                                Suit1 = ""
                            score_text = small_font.render("PLAYER{0} ({1}) discard {2}".format(state.player_to_move,player_name,str(Rank1)+str(Suit1)), True, BLACK)

                        elif card_num == 2:
                            print_card1 = pygame.image.load(r'./cards/' + str(m[0].rank) + m[0].suit + '.png')
                            print_card2 = pygame.image.load(r'./cards/' + str(m[1].rank) + m[1].suit + '.png')
                            print_card3 = pygame.image.load(r'./cards/' + 'back' + '.png')
                            print_card4 = pygame.image.load(r'./cards/' + 'back' + '.png')
                            Rank1 = m[0].rank
                            Suit1 = m[0].suit
                            Rank2 = m[1].rank
                            Suit2 = m[1].suit

                            if m[0].rank == 14:
                                Rank1 = "A"
                            elif m[0].rank == 15:
                                Rank1 = 2
                            elif m[0].rank == 16:
                                Rank1 = "JOKER"
                                Suit1 = ""

                            if m[1].rank == 14:
                                Rank2 = "A"
                            elif m[1].rank == 15:
                                Rank2 = 2
                            elif m[1].rank == 16:
                                Rank2 = "JOKER"
                                Suit2 = ""
                                
                            score_text = small_font.render("PLAYER{0} ({1}) discard {2} {3}".format(state.player_to_move,player_name,str(Rank1)+str(Suit1), str(Rank2)+str(Suit2)), True, BLACK)
                       
                        elif card_num == 3:
                            print_card1 = pygame.image.load(r'./cards/' + str(m[0].rank) + m[0].suit + '.png')
                            print_card2 = pygame.image.load(r'./cards/' + str(m[1].rank) + m[1].suit + '.png')
                            print_card3 = pygame.image.load(r'./cards/' + str(m[2].rank) + m[2].suit + '.png')
                            print_card4 = pygame.image.load(r'./cards/' + 'back' + '.png')
                            Rank1 = m[0].rank
                            Suit1 = m[0].suit
                            Rank2 = m[1].rank
                            Suit2 = m[1].suit
                            Rank3 = m[2].rank
                            Suit3 = m[2].suit

                            if m[0].rank == 14:
                                Rank1 = "A"
                            elif m[0].rank == 15:
                                Rank1 = 2
                            elif m[0].rank == 16:
                                Rank1 = "JOKER"
                                Suit1 = ""

                            if m[1].rank == 14:
                                Rank2 = "A"
                            elif m[1].rank == 15:
                                Rank2 = 2
                            elif m[1].rank == 16:
                                Rank2 = "JOKER"
                                Suit2 = ""

                            if m[2].rank == 14:
                                Rank3 = "A"
                            elif m[2].rank == 15:
                                Rank3 = 2
                            elif m[2].rank == 16:
                                Rank3 = "JOKER"
                                Suit3 = ""
                            score_text = small_font.render("PLAYER{0} ({1}) discard {2} {3} {4}".format(state.player_to_move,player_name,str(Rank1)+str(Suit1), str(Rank2)+str(Suit2),str(Rank3)+str(Suit3)), True, BLACK)
                        elif card_num == 4:
                            print_card1 = pygame.image.load(r'./cards/' + str(m[0].rank) + m[0].suit + '.png')
                            print_card2 = pygame.image.load(r'./cards/' + str(m[1].rank) + m[1].suit + '.png')
                            print_card3 = pygame.image.load(r'./cards/' + str(m[2].rank) + m[2].suit + '.png')
                            print_card4 = pygame.image.load(r'./cards/' + str(m[3].rank) + m[3].suit + '.png')

                            Rank1 = m[0].rank
                            Suit1 = m[0].suit
                            Rank2 = m[1].rank
                            Suit2 = m[1].suit
                            Rank3 = m[2].rank
                            Suit3 = m[2].suit
                            Rank4 = m[3].rank
                            Suit4 = m[3].suit



                            if m[0].rank == 14:
                                Rank1 = "A"
                            elif m[0].rank == 15:
                                Rank1 = 2
                            elif m[0].rank == 16:
                                Rank1 = "JOKER"
                                Suit1 = ""

                            if m[1].rank == 14:
                                Rank2 = "A"
                            elif m[1].rank == 15:
                                Rank2 = 2
                            elif m[1].rank == 16:
                                Rank2 = "JOKER"
                                Suit2 = ""

                            if m[2].rank == 14:
                                Rank3 = "A"
                            elif m[2].rank == 15:
                                Rank3 = 2
                            elif m[2].rank == 16:
                                Rank3 = "JOKER"
                                Suit3 = ""

                            if m[3].rank == 14:
                                Rank4 = "A"
                            elif m[3].rank == 15:
                                Rank4 = 2
                            elif m[3].rank == 16:
                                Rank4 = "JOKER"
                                Suit4 = ""
                            score_text = small_font.render("PLAYER{0} ({1}) discard {2} {3} {4} {5}".format(state.player_to_move,player_name,str(Rank1)+str(Suit1), str(Rank2)+str(Suit2),str(Rank3)+str(Suit3),str(Rank4)+str(Suit4)), True, BLACK)
                            

                    else:
                        print_card1 = pygame.image.load(r'./cards/' + 'back' + '.png')
                        print_card2 = pygame.image.load(r'./cards/' + 'back' + '.png')
                        print_card3 = pygame.image.load(r'./cards/' + 'back' + '.png')
                        print_card4 = pygame.image.load(r'./cards/' + 'back' + '.png')
                        score_text = small_font.render("PLAYER{0} ({1}) PASS".format(state.player_to_move,player_name), True, BLACK)
                        

                    

                    # 카드 출력
                    print_card1 = pygame.transform.scale(print_card1 , (100,160))
                    print_card2 = pygame.transform.scale(print_card2 , (100,160))
                    print_card3 = pygame.transform.scale(print_card3 , (100,160))
                    print_card4 = pygame.transform.scale(print_card4 , (100,160))
                    screen.blit(print_card1, (MARGIN_LEFT,MARGIN_TOP))
                    screen.blit(print_card2, (MARGIN_LEFT+120, MARGIN_TOP))
                    screen.blit(print_card3, (MARGIN_LEFT+240, MARGIN_TOP))
                    screen.blit(print_card4, (MARGIN_LEFT+360, MARGIN_TOP))



                    #스코어 보드 출력
                    pygame.draw.rect(screen, WHITE, [100, 40, 700, 120])
                    score_text_rect = score_text.get_rect()
                    score_text_rect.center = (450, 100)
                    screen.blit(score_text, score_text_rect)

                    # 승률계산
                    pygame.draw.rect(screen, WHITE, [60, MARGIN_TOP, 280, 200])
                    if state.player_to_move == 0 and m != "PASS":
                        winning_player = small_font.render("MCTS winning rate", True, BLACK)
                        winning_rate = large_font.render("{:.2f}%".format(mcts_winningRate), True, BLUE)
                        
                    else:
                        winning_player = small_font.render("player", True, BLACK)
                        winning_rate = small_font.render(player_name, True, BLACK)


                    winning_player_rect = winning_player.get_rect()
                    winning_player_rect.center = (200, 260)
                    winning_rate_rect = winning_rate.get_rect()
                    winning_rate_rect.center = (200, 340)

                    
                    screen.blit(winning_player, winning_player_rect)
                    screen.blit(winning_rate, winning_rate_rect)
                        

                    time.sleep(1)
                    pygame.display.update()
                    
                    state.do_move(m)

                for p in (0, 1, 2, 3):
                    if state.get_result(p) > 0:
                        print("Player " + str(p) + " wins!")
                        winner = p
                        over = True
                        return winner
        
        
        # Setting up all the buttons, images and texts on the screen
        #이미지 세팅
        
        screen.blit(print_card1, (MARGIN_LEFT,MARGIN_TOP))
        screen.blit(print_card2, (MARGIN_LEFT+120, MARGIN_TOP))
        screen.blit(print_card3, (MARGIN_LEFT+240, MARGIN_TOP))
        screen.blit(print_card4, (MARGIN_LEFT+360, MARGIN_TOP))


        if over == True:
            # rect(왼쪽x, 위y, 너비, 높이)순서
            pygame.draw.rect(screen, WHITE, [100, 40, 700, 120])
            score_text = large_font.render("PLAYER {0} WINS!!".format(winner), True, BLACK)
            score_text_rect = score_text.get_rect()
            score_text_rect.center = (450, 100)
            screen.blit(score_text, score_text_rect)
 
        # Update the display after each game loop
        pygame.display.update()

if __name__ == "__main__":
    output = []
    for i in range(1,200):
        result = play_self()
        if result == 0 : output.append("mcts")
        if result == 1 : output.append("rand1")
        if result == 2 : output.append("rand2")
        if result == 3 : output.append("rand3")
        print("try",i," : ")
        print(output.count('mcts'))
        print(output.count('rand1'))
        print(output.count('rand2'))
        print(output.count('rand3'))
