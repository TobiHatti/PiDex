# Importing Modules
import pygame
from pygame import gfxdraw
from threading import Thread
import time
import random
import sys
import sqlite3
import os

from CButton import Button
from SpriteManager import Sprite
from CDrawing import Draw
from CText import Text
from CUserInterface import UI

from DexInfo import DexInfo 




class DexMenu:

#########################################################################################
#   PROTECTED VARIABLES                                                                 #
#########################################################################################

    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    thread = Thread()
    sleepThread = Thread()

    running = True

#########################################################################################
#########################################################################################
#   MAIN START                                                                          #
#########################################################################################
#########################################################################################

    def Show():
   
#########################################################################################
#   INITIALISATION AND SETUP                                                            #
#########################################################################################

        # PyGame Initialisation
        clock = pygame.time.Clock()

        # Window and Surface Initialisation
        displayWidth = 800
        displayHeight = 480

        idleCtr = 0

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

        dexSurface = pygame.Surface((600,380)).convert_alpha()

        selectionEngaged = False
        engagedMousePos = (0,0)

        clickCtr = 0
        scrollCooldown = 0

        dexScrollOffset = 0

        scrollDecayEngaged = False
        scrDecFirstValue = (0,0)
        scrDecSecondValue = (0,0)
        scrDecCounter = 0
        scrollDecay = 0
        scrollDirectionUp = False


        while DexMenu.running:

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

            mouse = pygame.mouse.get_pos()
            mouseRel = pygame.mouse.get_rel()
            click = pygame.mouse.get_pressed()

            dexStartRange = 0
            dexEndRange = 6

            dexOffsetStep = abs(int(dexScrollOffset / 96))

         
            mainSurface.fill((30,30,30))
            dexSurface.fill((40,40,40))
            dexSurface.set_colorkey((0,0,0))

            Draw.RoundRect(mainSurface,(40,40,40),(150,20,640,410),20,2,(255,0,0),"Hallo")
            Draw.Pokeball(mainSurface,(140,35),(255,0,0),(40,40,40))

            for x in range(dexStartRange + dexOffsetStep,dexEndRange + dexOffsetStep):

                rowCount = x

                for m in range(0,6):
                    dexNumber = (x * 6 + m) + 1
                    if dexNumber < 803:
                        img = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(dexNumber)) + "/sprite-small-FN-" + str('{0:03d}'.format(dexNumber)) + ".png"),(96,96)).convert_alpha()

                        if (m*96+170) < mouse[0]  < (m*96+96+170) and (x*96+dexScrollOffset+50) < mouse[1]  < (x*96+dexScrollOffset+96+50): 
                            pygame.draw.rect(dexSurface,(0,255,0),((m*96),(x*96+dexScrollOffset),96,96))
                    
                            # Additional condition for scroll support
                            if click[0] == 1 and engagedMousePos == (0,0):
                                selectionEngaged = True
                                engagedMousePos = mouse
                            if selectionEngaged and click[0] == 0:
                                selectionEngaged = False
                                if engagedMousePos[0] - 10 < mouse[0] < engagedMousePos[0] + 10 and engagedMousePos[1] - 10 < mouse[1] < engagedMousePos[1] + 10:
                                    dexScrollOffset = -int(((DexInfo.Show(dexNumber) * 96)/6) - 2 * 96) 
                                engagedMousePos = (0,0)


                        dexSurface.blit(img,(m * 96, x * 96 + dexScrollOffset)) 


            mainSurface.blit(dexSurface,(170,50))

            # Scrolling generall
            if click[0] == 1: clickCtr += 1
            else: clickCtr = 0

            if click[0] == 1 and clickCtr > 1:
                dexScrollOffset += mouseRel[1]
                if dexScrollOffset > 0: dexScrollOffset = 0
                if dexScrollOffset < -(802/6)*96 + 3*96: dexScrollOffset = -(802/6)*96 + 3*96
               

            pygame.display.update()
            clock.tick(60)