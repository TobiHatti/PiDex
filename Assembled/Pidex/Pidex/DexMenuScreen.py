# Importing Modules
import pygame
from pygame import gfxdraw
import time
import random
import sys
import sqlite3
import os
from basics import Basic

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

selectionEngaged = False
engagedMousePos = (0,0)


clickCtr = 0
scrollCooldown = 0

backgroundImage = pygame.image.load("bg.jpg").convert()
mainSurface.blit(backgroundImage,(0,0))


dexScrollOffset = 0



scrollDecayEngaged = False
scrDecFirstValue = (0,0)
scrDecSecondValue = (0,0)
scrDecCounter = 0
scrollDecay = 0
scrollDirectionUp = False


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

    mouse = pygame.mouse.get_pos()
    mouseRel = pygame.mouse.get_rel()
    click = pygame.mouse.get_pressed()

    for x in range(dexStartRange + dexOffsetStep,dexEndRange + dexOffsetStep):
        for m in range(0,6):
            dexNumber = (x * 6 + m) + 1
            if dexNumber < 803:
                img = pygame.image.load("sprites/" + str('{0:03d}'.format(dexNumber)) + "/sprite-small-FN-" + str('{0:03d}'.format(dexNumber)) + ".png").convert_alpha()
                pygame.transform.scale(img,(96,96))

                if (m*96+170) < mouse[0]  < (m*96+96+170) and (x*96+dexScrollOffset+50) < mouse[1]  < (x*96+dexScrollOffset+96+50): 
                    pygame.draw.rect(dexSurface,(0,255,0),((m*96),(x*96+dexScrollOffset),96,96))
                    
                    # Additional condition for scroll support
                    if click[0] == 1 and engagedMousePos == (0,0):
                        selectionEngaged = True
                        engagedMousePos = mouse
                    if selectionEngaged and click[0] == 0:
                        selectionEngaged = False
                        if engagedMousePos[0] - 10 < mouse[0] < engagedMousePos[0] + 10 and engagedMousePos[1] - 10 < mouse[1] < engagedMousePos[1] + 10:
                            print("Load " + str('{0:03d}'.format(dexNumber)) + "...")
                            pygame.quit()
                            os.system("python3 InfoScreen_Rev3.py " + str(dexNumber))
                            sys.exit()
                        engagedMousePos = (0,0)


                dexSurface.blit(img,(m * 96, x * 96 + dexScrollOffset)) 


    mainSurface.blit(dexSurface,(170,50))

    # Scrolling generall
    if click[0] == 1: clickCtr += 1
    else: clickCtr = 0

    if click[0] == 1 and clickCtr > 1:
        dexScrollOffset += mouseRel[1]
        if dexScrollOffset > 0: dexScrollOffset = 0

  
    # Scroll decay
    if click[0] == 1: scrollDecayEngaged = True

    if scrollDecayEngaged:
        if scrDecCounter == 2 : scrDecFirstValue = mouse
        if scrDecCounter == 3: scrDecSecondValue = mouse

        if scrDecCounter > 3:
            if scrDecFirstValue[1] < scrDecSecondValue[1]: 
                scrollDirectionUp = True
                if mouseRel[1] > scrollDecay: scrollDecay = abs(mouseRel[1])
            else:
               scrollDirectionUp = False
               if mouseRel[1] < -abs(scrollDecay): scrollDecay = abs(mouseRel[1])

        scrDecCounter += 1

    if click[0] == 0 and not scrollDecay <= 0:
        scrollDecay -= 3
        if scrollDirectionUp: dexScrollOffset += scrollDecay
        else: dexScrollOffset -= scrollDecay

    if click[0] == 0 and scrollDecay <= 0:
        scrollDecayEngaged = False
        scrDecFirstValue = (0,0)
        scrDecSecondValue = (0,0)
        scrDecCounter = 0

    clock.tick(60)
    pygame.display.update()