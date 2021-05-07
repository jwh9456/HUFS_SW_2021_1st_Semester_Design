"""
Interactive player.
"""
DEBUG = True
import sys
from collections import defaultdict
import new_common as common

def play(prev, hand, discard, holding, valid=common.get_valid_plays, generate=common.generate_plays, is_valid=common.is_valid_play):
  if prev is None:
    plays = generate(hand)
  else:
    plays = valid(prev,hand)

  # Just pass straight away if we dont actually have a choice
  if not plays:
    return None
  
  new_plays = []
  if prev:
    for elem in plays:
      if len(elem) == len(prev):
        new_plays.append(elem)
  else:
    new_plays = plays

  new_plays.sort(key=lambda p: (len(p), max(map(common.card_value,p))))
  if DEBUG:print ("PLAYS",new_plays)

  discard_summary = defaultdict(list)
  for round in discard:
    for play in round:
      if play is not None:
        for card in play:
          discard_summary[card[1]].append(card)

  if discard_summary:
    if DEBUG:print ("    Discard Summary:")
    for suit in sorted(discard_summary):
      cards = sorted(discard_summary[suit], key=common.card_value)
      ranks = [c[0] for c in cards]
      disp = ''.join( c if c in ranks else ' ' for c in common.RANKS)
      if DEBUG:print ("      {0}: {1}".format(suit, disp))

  if DEBUG:print ("    Hand: {0}".format(sorted(hand, key=common.card_value)))
  if prev is not None:
    if DEBUG:print ("    Prev: {0}".format(sorted(prev, key=common.card_value)))
  #if DEBUG:print ("    [0] Pass")
  for i, play in enumerate(new_plays):
    if DEBUG:print ("    [{0}] {1}".format(i+1, play))

  while True:
    try:
      c = int(input("    CHOICE: "))
      if c == 0:
        return None
      elif str(c) == 'exit':
        break
      else:
        return new_plays[c-1]
        
    except:
      if DEBUG:print("    올바른 번호를 입력해 주세요")
      continue
    
