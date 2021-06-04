from math import *
from operator import attrgetter
import random


class GameState:

    def __init__(self):
        self.number_of_players = 4
        self.player_to_move = 3

    def get_next_player(self, p):
        return (p % self.number_of_players) + 1

    def clone(self):
        st = GameState()
        st.player_to_move = self.player_to_move
        return st

    def clone_and_randomize(self, observer):
        return self.clone()

    def do_move(self, move):
        self.player_to_move = self.get_next_player(self.player_to_move)

    def get_moves(self):
        pass

    def get_result(self, player):
        pass

    def __repr__(self):
        pass


class Deck:

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in range(3, 15 + 1) for suit in
                      ['C', 'D', 'H', 'S']]
        self.cards.append(Card(16, 'B'))

    def shuffle(self):
        random.shuffle(self.cards)


NAMES = "???3456789TJQKA2B"


class Card(object):

    def __init__(self, rank=None, suit=None):
        if not suit:
            suit = rank[1].upper()
            rank = NAMES.index(rank[0].upper())
            if rank not in range(2, 16 + 1):
                raise Exception("Invalid rank")
            if suit not in ['C', 'D', 'H', 'S', 'B']:
                raise Exception("Invalid suit")

        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return NAMES[int(self.rank)] + PRETTY_SUITS[self.suit]

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return self.rank != other.rank or self.suit != other.suit


PRETTY_SUITS = {
    "S": u"\u2660",  # spades
    "H": u"\u2764",  # hearts
    "D": u"\u2666",  # diamonds
    "C": u"\u2663",  # clubs
    "B": u"\u220E"  # joker
}


class Node:

    def __init__(self, move=None, parent=None, player_just_moved=None):

        self.move = move
        self.parent_node = parent
        self.child_nodes = []
        self.wins = 0
        self.visits = 0
        self.avails = 1
        self.player_just_moved = player_just_moved

    def get_untried_moves(self, legal_moves):
        tried_moves = [child.move for child in self.child_nodes]

        return [move for move in legal_moves if move not in tried_moves]

    def ucb_select_child(self, legal_moves, exploration=0.7):

        # Filter the list of children by the list of legal moves
        legal_children = [child for child in self.child_nodes if
                          child.move in legal_moves]

        # Get the child with the highest UCB score
        s = max(legal_children, key=lambda c: float(c.wins) / float(
            c.visits) + exploration * sqrt(log(c.avails) / float(c.visits)))

        # update availability counts -- it is easier to do this now than during backpropagation
        for child in legal_children:
            child.avails += 1

        # Return the child selected above
        return s

    def add_child(self, m, p):

        n = Node(move=m, parent=self, player_just_moved=p)
        self.child_nodes.append(n)
        return n

    def update(self, terminal_state):

        self.visits += 1
        if self.player_just_moved is not None:
            self.wins += terminal_state.get_result(self.player_just_moved)

    def __repr__(self):
        return "[M:%s W/V/A: %4i/%4i/%4i]" % (self.move, self.wins, self.visits, self.avails)

    def tree_to_string(self, indent):

        s = self.indent_string(indent) + str(self)
        for c in sorted(self.child_nodes, key=attrgetter('visits', 'wins')):
            s += c.tree_to_string(indent + 1)
        return s

    @staticmethod
    def indent_string(indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def children_to_string(self):
        s = ""
        for c in sorted(self.child_nodes, key=attrgetter('visits', 'wins')):
            s += str(c) + "\n"
        return s


def ismcts(rootstate, itermax, verbose=False, quiet=False):
    rootnode = Node()
    if len(rootstate.get_moves()) > 1:
        # There are moves. Simulate them

        for i in range(itermax):
            node = rootnode

            # Determine
            state = rootstate.clone_and_randomize(rootstate.player_to_move)

            # Select
            while state.get_moves() != [] and node.get_untried_moves(
                    state.get_moves()) == []:  # node is fully expanded and non-terminal
                node = node.ucb_select_child(state.get_moves())
                state.do_move(node.move)

            # Expand
            untried_moves = node.get_untried_moves(state.get_moves())
            if untried_moves:  # if we can expand (i.e. state/node is non-terminal)
                m = random.choice(untried_moves)
                player = state.player_to_move
                state.do_move(m)
                node = node.add_child(m, player)  # add child and descend tree

            # Simulate
            """
            if i % 10 == 0:
                print("{0}번째 simulation".format(i))
            """
            while state.get_moves():  # while state is non-terminal
                state.do_move(random.choice(state.get_moves()))

            # Backpropagation
            while node:
                node.update(state)
                node = node.parent_node

    else:
        rootnode.add_child(rootstate.get_moves()[0], rootstate.player_to_move)

    # Output some information about the tree - can be omitted
    if verbose:
        print(rootnode.tree_to_string(0))
    elif not quiet:
        print(rootnode.children_to_string())

    best_mcts = max(rootnode.child_nodes, key=lambda c: c.visits)

    return (best_mcts.move,best_mcts.visits, best_mcts.wins)  # return the move that was most visited
