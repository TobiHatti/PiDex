# Importing Modules
import pygame
from pygame import gfxdraw
import time
import random
import sys
import sqlite3
import os

# PyGame Initialisation
pygame.init()
clock = pygame.time.Clock()
#pygame.mouse.set_visible(False)

# Window and Surface Initialisation
displayWidth = 800
displayHeight = 480

try:
    if os.uname()[1] == 'raspberrypi': 
        mainSurface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    else: 
        mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
        pygame.mouse.set_visible(True)
except:
    mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
    pygame.mouse.set_visible(True)


menuSurface = pygame.Surface((200,480)).convert()
dexSurface = pygame.Surface((600,380)).convert()

# DB-Initialisation and Setup
conn = sqlite3.connect('pokemon.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

running = True

clickCtr = 0
scrollCooldown = 0

backgroundImage = pygame.image.load("bg.jpg").convert()
mainSurface.blit(backgroundImage,(0,0))


dexScrollOffset = 0

while running:

    # Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Keypress Processing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q] != 0: 
        pygame.quit()
        sys.exit()


    mainSurface.blit(backgroundImage,(0,0))
    dexSurface.fill((0,0,0))
    dexSurface.set_colorkey((0,0,0))

    dexStartRange = 0
    dexEndRange = 6

    dexOffsetStep = abs(int(dexScrollOffset / 96))

    for x in range(dexStartRange + dexOffsetStep,dexEndRange + dexOffsetStep):
        for m in range(0,6):
            dexNumber = (x * 6 + m) + 1
            if dexNumber < 803:
                img = pygame.image.load("sprites/" + str('{0:03d}'.format(dexNumber)) + "/sprite-small-FN-" + str('{0:03d}'.format(dexNumber)) + ".png").convert_alpha()
                pygame.transform.scale(img,(96,96))
                dexSurface.blit(img,(m * 96, x * 96 + dexScrollOffset))
    mainSurface.blit(dexSurface,(170,50))

    
    mouseRel = pygame.mouse.get_rel()
    click = pygame.mouse.get_pressed()

    if click[0] == 1: clickCtr += 1
    else: clickCtr = 0

    if click[0] == 1 and clickCtr > 1:
        dexScrollOffset += mouseRel[1]

        if dexScrollOffset > 0: dexScrollOffset = 0
    

    clock.tick(60)
    pygame.display.update()