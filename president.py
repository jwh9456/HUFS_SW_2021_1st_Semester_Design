from copy import copy
from operator import attrgetter
import random
import common

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

    state = PresidentGameState()
    state._deal()

    while state.get_moves():
        print(str(state))
        # Use different numbers of iterations (simulations, tree nodes) for different players
        if state.player_to_move == 0:
            m = ismcts(rootstate=state, itermax=10, verbose=False)
            print("Best Move: " + str(m) + "\n")

        elif state.player_to_move == 1:
            cards = state.get_moves()

            for card in cards:
                print(card, end = " ")

            m = random.choice(cards)
            print("\nrandom Move: " + str(m) + "\n")
            
        elif state.player_to_move == 2:
            cards = state.get_moves()

            for card in cards:
                print(card, end=" ")

            if len(cards) == 1 and cards[0] == 'PASS':
                m = 'PASS'
            else:
                m = cards[-2]

            print("\nsmallest Move: " + str(m) + "\n")
            
        elif state.player_to_move == 3:
            cards = state.get_moves()

            for card in cards:
                print(card, end=" ")

            if len(cards) == 1 and cards[0] == 'PASS':
                m = 'PASS'
            else:
                m = cards[-2]

            print("\nlargest Move: " + str(m) + "\n")
            
        if m != 'PASS':
            for card in m:
                if card.suit == 'B':
                    card.rank = 16

        state.do_move(m)

    for p in (0, 1, 2, 3):
        if state.get_result(p) > 0:
            print("Player " + str(p) + " wins!")

if __name__ == "__main__":
    play_self()
