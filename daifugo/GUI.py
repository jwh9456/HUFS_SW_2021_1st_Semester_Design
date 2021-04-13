import pygame
import sys
from pathlib import Path as p
import game
import interactive
import common

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
imgpath = p.cwd()/'daifugo'/'assets'/'cards'
pos_x = 200
pos_y = 200

background = (36,41,46)

pygame.init()
pygame.display.set_caption("Daifugo with MCTS")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

deck = game.get_deck()
for card in deck:
    card_image = pygame.image.load(str(imgpath)+'/'+card+'.png')
    card_image = pygame.transform.scale(card_image,(100,130))
clock = pygame.time.Clock()

back_image = pygame.image.load(p.cwd()/'daifugo'/'assets'/'cards'/'back.png').convert()
back_image = pygame.transform.scale(back_image,(100,155))
while True:

    # key_event = pygame.key.get_pressed()
    # if key_event[pygame.K_LEFT]:
    #     cursor -= 1

    # if key_event[pygame.K_RIGHT]:
    #     cursor += 1

    # if key_event[pygame.K_ESCAPE]:
    #     pygame.quit()

    screen.fill(background)
    screen.blit(back_image,(200,200))
    pygame.display.update()