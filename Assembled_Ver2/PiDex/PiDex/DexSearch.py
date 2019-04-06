# Importing Modules
import pygame
from pygame import gfxdraw
from pygame.locals import *
from threading import Thread
import time
import random
import sys
import sqlite3
import os
import math

from CButton import Button
from SpriteManager import Sprite
from CDrawing import Draw
from CText import Text

class DexSearch:

#########################################################################################
#   PROTECTED VARIABLES                                                                 #
#########################################################################################

    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    thread = Thread()
    sleepThread = Thread()

    running = True
    reload = True

    searchVal = ""
    engageSearch = False

#########################################################################################
#   FUNCTIONS                                                                           #
#########################################################################################

    def PasteLetter(letter):
        DexSearch.searchVal = DexSearch.searchVal + letter
        DexSearch.engageSearch = True

    def DeleteLetter():
        DexSearch.searchVal = DexSearch.searchVal[:-1]
        DexSearch.engageSearch = True

#########################################################################################
#   TOGGLE FUNCTIONS                                                                    #
#########################################################################################

    def ReturnToMenu():
        DexSearch.running = False
        DexSearch.reload = True

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

        

        flags = FULLSCREEN | DOUBLEBUF

        try:
            if os.uname()[1] == 'raspberrypi': 
                mainSurface = pygame.display.set_mode((0,0),flags)
                pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
            else: 
                mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
                pygame.mouse.set_visible(True)
        except:
            mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
            pygame.mouse.set_visible(True)

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

#########################################################################################
#   SURFACE DEFINITIONS                                                                 #
#########################################################################################

        searchResSurface = pygame.Surface((760,110)).convert_alpha()

#########################################################################################
#   VARIABLE DEFINITIONS                                                                #
#########################################################################################
           
        searchResult = []

#########################################################################################
#   LOADING LOOP                                                                        #
#########################################################################################

        while DexSearch.running:

            # Button Setup
            Button.idleColor = (255,255,255)
            Button.hoverColor = (200,200,200) 
            Button.fontColor = (255,0,0)
            Button.disabledColor = (150,150,150)
            Button.borderColor = (255,0,0)
            Button.fontFamily = "joy.otf"

            fontSize = 40

            vertOffset = 160

            # First Row
            btnLetterQ = Button.RoundRect(mainSurface,(14+0*78,vertOffset,70,70),15,"Q",fontSize,1,DexSearch.PasteLetter,"Q")
            btnLetterW = Button.RoundRect(mainSurface,(14+1*78,vertOffset,70,70),15,"W",fontSize,1,DexSearch.PasteLetter,"W")
            btnLetterE = Button.RoundRect(mainSurface,(14+2*78,vertOffset,70,70),15,"E",fontSize,1,DexSearch.PasteLetter,"E")
            btnLetterR = Button.RoundRect(mainSurface,(14+3*78,vertOffset,70,70),15,"R",fontSize,1,DexSearch.PasteLetter,"R")
            btnLetterT = Button.RoundRect(mainSurface,(14+4*78,vertOffset,70,70),15,"T",fontSize,1,DexSearch.PasteLetter,"T")
            btnLetterY = Button.RoundRect(mainSurface,(14+5*78,vertOffset,70,70),15,"Y",fontSize,1,DexSearch.PasteLetter,"Y")
            btnLetterU = Button.RoundRect(mainSurface,(14+6*78,vertOffset,70,70),15,"U",fontSize,1,DexSearch.PasteLetter,"U")
            btnLetterI = Button.RoundRect(mainSurface,(14+7*78,vertOffset,70,70),15,"I",fontSize,1,DexSearch.PasteLetter,"I")
            btnLetterO = Button.RoundRect(mainSurface,(14+8*78,vertOffset,70,70),15,"O",fontSize,1,DexSearch.PasteLetter,"O")
            btnLetterP = Button.RoundRect(mainSurface,(14+9*78,vertOffset,70,70),15,"P",fontSize,1,DexSearch.PasteLetter,"P")
            # Second Row
            btnLetterA = Button.RoundRect(mainSurface,(45+0*80,vertOffset+80,70,70),15,"A",fontSize,1,DexSearch.PasteLetter,"A")
            btnLetterS = Button.RoundRect(mainSurface,(45+1*80,vertOffset+80,70,70),15,"S",fontSize,1,DexSearch.PasteLetter,"S")
            btnLetterD = Button.RoundRect(mainSurface,(45+2*80,vertOffset+80,70,70),15,"D",fontSize,1,DexSearch.PasteLetter,"D")
            btnLetterF = Button.RoundRect(mainSurface,(45+3*80,vertOffset+80,70,70),15,"F",fontSize,1,DexSearch.PasteLetter,"F")
            btnLetterG = Button.RoundRect(mainSurface,(45+4*80,vertOffset+80,70,70),15,"G",fontSize,1,DexSearch.PasteLetter,"G")
            btnLetterH = Button.RoundRect(mainSurface,(45+5*80,vertOffset+80,70,70),15,"H",fontSize,1,DexSearch.PasteLetter,"H")
            btnLetterJ = Button.RoundRect(mainSurface,(45+6*80,vertOffset+80,70,70),15,"J",fontSize,1,DexSearch.PasteLetter,"J")
            btnLetterK = Button.RoundRect(mainSurface,(45+7*80,vertOffset+80,70,70),15,"K",fontSize,1,DexSearch.PasteLetter,"K")
            btnLetterL = Button.RoundRect(mainSurface,(45+8*80,vertOffset+80,70,70),15,"L",fontSize,1,DexSearch.PasteLetter,"L")
            # Third Row
            btnLetterZ = Button.RoundRect(mainSurface,(85+0*80,vertOffset+160,70,70),15,"Z",fontSize,1,DexSearch.PasteLetter,"Z")
            btnLetterX = Button.RoundRect(mainSurface,(85+1*80,vertOffset+160,70,70),15,"X",fontSize,1,DexSearch.PasteLetter,"X")
            btnLetterC = Button.RoundRect(mainSurface,(85+2*80,vertOffset+160,70,70),15,"C",fontSize,1,DexSearch.PasteLetter,"C")
            btnLetterV = Button.RoundRect(mainSurface,(85+3*80,vertOffset+160,70,70),15,"V",fontSize,1,DexSearch.PasteLetter,"V")
            btnLetterB = Button.RoundRect(mainSurface,(85+4*80,vertOffset+160,70,70),15,"B",fontSize,1,DexSearch.PasteLetter,"B")
            btnLetterN = Button.RoundRect(mainSurface,(85+5*80,vertOffset+160,70,70),15,"N",fontSize,1,DexSearch.PasteLetter,"N")
            btnLetterM = Button.RoundRect(mainSurface,(85+6*80,vertOffset+160,70,70),15,"M",fontSize,1,DexSearch.PasteLetter,"M")
            btnSignDot = Button.RoundRect(mainSurface,(85+7*80,vertOffset+160,50,70),15,".",fontSize,1,DexSearch.PasteLetter,".")
            btnSignMin = Button.RoundRect(mainSurface,(60+85+7*80,vertOffset+160,50,70),15,"-",fontSize,1,DexSearch.PasteLetter,"-")
            # Fourth Row
            btnOpDelete = Button.RoundRect(mainSurface,(35+0*80,vertOffset+240,160,70),15,"Delete",30,1,DexSearch.DeleteLetter)
            btnSignSpa = Button.RoundRect(mainSurface,(45+2*80,vertOffset+240,390,70),15,"[Space]",30,1,DexSearch.PasteLetter," ")
            btnOpSearch = Button.RoundRect(mainSurface,(45+7*80,vertOffset+240,160,70),15,"Search...",30,1,DexSearch.PasteLetter,"")

            btnGoBack = Button.RoundRect(mainSurface,(0,0,120,30),10,"< Back",20,1,DexSearch.ReturnToMenu)

            searchResSurface.fill((40,40,40))
            searchResSurface.set_colorkey((0,0,0))

            DexSearch.reload = False

#########################################################################################
#   RUNNING LOOP                                                                        #
#########################################################################################

            while not DexSearch.reload:

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
                click = pygame.mouse.get_pressed()

                
                mainSurface.fill((30,30,30))

                
                Draw.RoundRect(mainSurface,(40,40,40),(5,150,790,325),15,2,(255,0,0))
                Draw.RoundRect(mainSurface,(40,40,40),(5,5,790,135),15,2,(255,0,0),"Searching for: " + str(DexSearch.searchVal))

                if DexSearch.engageSearch:
                    params = (DexSearch.searchVal + "%",)
                    DexSearch.c.execute("SELECT * FROM pokemon WHERE name LIKE ? ORDER BY nationalDex ASC LIMIT 0,8",params)
                    searchResult = DexSearch.c.fetchall()

                    i = 0

                    searchResSurface.fill((40,40,40))
                    searchResSurface.set_colorkey((0,0,0))

                    for pm in searchResult: 
                        filePath = "sprites/" + str('{0:03d}'.format(pm["nationalDex"])) + "/sprite-small-FN-" + str('{0:03d}'.format(pm["nationalDex"])) + ".png"
                        if os.path.isfile(filePath): pokeSprite = pygame.image.load(filePath).convert_alpha()
                        else: pokeSprite = pygame.image.load("notFound.gif").convert_alpha()
                        pokeSprite = pygame.transform.scale(pokeSprite,(96,96))
                        searchResSurface.blit(pokeSprite,(i*96,0))
                        Text.Write(searchResSurface,(i*96+48,96),pm["name"],12,"joy.otf",(255,255,255),True)
                        Text.Write(searchResSurface,(i*96,0),"#" + str('{0:03d}'.format(pm["nationalDex"])),12,"joy.otf",(255,255,255),False)
                        i+=1

                    DexSearch.engageSearch = False

                i = 0
                for pm in searchResult:

                    if 20+i*96 < mouse[0] < 20+96+i*96 and 30 < mouse[1] < 140:
                        if click[0] == 1: return pm["nationalDex"]
                    i += 1

                

                mainSurface.blit(searchResSurface,(20,30))

                pygame.display.update(btnLetterQ.Show())
                pygame.display.update(btnLetterW.Show())
                pygame.display.update(btnLetterE.Show())
                pygame.display.update(btnLetterR.Show())
                pygame.display.update(btnLetterT.Show())
                pygame.display.update(btnLetterY.Show())
                pygame.display.update(btnLetterU.Show())
                pygame.display.update(btnLetterI.Show())
                pygame.display.update(btnLetterO.Show())
                pygame.display.update(btnLetterP.Show())

                pygame.display.update(btnLetterA.Show())
                pygame.display.update(btnLetterS.Show())
                pygame.display.update(btnLetterD.Show())
                pygame.display.update(btnLetterF.Show())
                pygame.display.update(btnLetterG.Show())
                pygame.display.update(btnLetterH.Show())
                pygame.display.update(btnLetterJ.Show())
                pygame.display.update(btnLetterK.Show())
                pygame.display.update(btnLetterL.Show())

                pygame.display.update(btnLetterZ.Show())
                pygame.display.update(btnLetterX.Show())
                pygame.display.update(btnLetterC.Show())
                pygame.display.update(btnLetterV.Show())
                pygame.display.update(btnLetterB.Show())
                pygame.display.update(btnLetterN.Show())
                pygame.display.update(btnLetterM.Show())
                pygame.display.update(btnSignDot.Show())
                pygame.display.update(btnSignMin.Show())

                pygame.display.update(btnOpDelete.Show())
                pygame.display.update(btnSignSpa.Show())
                pygame.display.update(btnOpSearch.Show())

                pygame.display.update(btnGoBack.Show())

                if 10 < mouse[0] < 790 and 10 < mouse[1] < 140:
                    Draw.DexCursor(mainSurface,(mouse[0],mouse[1]))

                # Update Screen
                pygame.display.update()
                clock.tick(60)

        DexSearch.running = True
        return None