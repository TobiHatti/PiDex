# Importing Modules
import pygame
from pygame import gfxdraw
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
    reload = True

    dexScrollOffset = 0

#########################################################################################
#   FUNCTIONS                                                                           #
#########################################################################################

    def GetPokeDataAll():
        DexInfo.c.execute("""SELECT *,
                evoNext.evoNextDex AS nextEvolution,
                evoPrev.evoDex AS prevEvolution,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon 
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND (sprites.isMegaEvolution IS NULL OR sprites.isMegaEvolution = '')
                LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id 
                LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id 
                LEFT JOIN regions ON pokemon.regionID = regions.id 
                LEFT JOIN evYields ON pokemon.nationalDex = evYields.nationalDex
                LEFT JOIN evYieldTypes ON evYields.evYieldTypeID = evYieldTypes.id
                LEFT JOIN growthRates ON pokemon.growthRateID = growthRates.id
                LEFT JOIN eggGroups ON pokemon.eggGroupID = eggGroups.id
                LEFT JOIN evolutions AS evoNext ON pokemon.nationalDex = evoNext.evoDex
                LEFT JOIN evolutions AS evoPrev ON pokemon.nationalDex = evoPrev.evoNextDex
                WHERE pokemon.nationalDex IS NOT NULL
                ORDER BY pokemon.nationalDex ASC
                """)
        return DexInfo.c.fetchall()

    def GetGenerations():
        DexInfo.c.execute("SELECT * FROM generations ORDER BY genNr ASC")
        return DexInfo.c.fetchall()

    def GetPMGen(dexNr):
        parameters = (dexNr,dexNr,)
        DexInfo.c.execute("SELECT * FROM generations WHERE genDexStart <= ? AND genDexEnd >= ?",parameters)
        return DexInfo.c.fetchone()["genNr"]

    def LoadSpriteSheet(dexSurface,generationData):

            yOffset = 0
            dexSurface.fill((40,40,40))
            dexSurface.set_colorkey((0,0,0))

            for gen in generationData:
                yOffset += 20
            
                pygame.gfxdraw.aacircle(dexSurface,300-100,yOffset,10,(255,255,255))
                pygame.gfxdraw.filled_circle(dexSurface,300-100,yOffset,10,(255,255,255))
                pygame.gfxdraw.aacircle(dexSurface,300+100,yOffset,10,(255,255,255))
                pygame.gfxdraw.filled_circle(dexSurface,300+100,yOffset,10,(255,255,255))

                pygame.draw.rect(dexSurface,(255,255,255),(0,yOffset-3,600,7))
                pygame.draw.rect(dexSurface,(255,255,255),(200,yOffset-10,200,21))

                Text.Write(dexSurface,(300,yOffset),gen["genName"],25,"joy.otf",(255,0,0),True)
                yOffset += 20

                for pm in range(int(gen["genDexStart"]),int(gen["genDexEnd"]+1),6):
                    for column in range(0,6):
                            if pm <= int(gen["genDexEnd"]):
                                filePath = "sprites/" + str('{0:03d}'.format(pm)) + "/sprite-small-FN-" + str('{0:03d}'.format(pm)) + ".png"
                                if os.path.isfile(filePath): pokeSprite = pygame.image.load(filePath).convert_alpha()
                                else: pokeSprite = pygame.image.load("notFound.gif").convert_alpha()
                                pokeSprite = pygame.transform.scale(pokeSprite,(96,96))
                                dexSurface.blit(pokeSprite,(column * 96, yOffset))
                                pm += 1    
                    yOffset += 96

#########################################################################################
#   TOGGLE FUNCTIONS                                                                    #
#########################################################################################

    def ReturnToMenu():
        DexMenu.running = False
        DexMenu.reload = True

    def ToggleGen1():
        DexMenu.dexScrollOffset = 0

    def ToggleGen2():
        DexMenu.dexScrollOffset = -(40+26*96)

    def ToggleGen3():
        DexMenu.dexScrollOffset = - (40+26*96) - (40+17*96)

    def ToggleGen4():
        DexMenu.dexScrollOffset = - (40+26*96) - (40+17*96) - (40+23*96)

    def ToggleGen5():
        DexMenu.dexScrollOffset = - (40+26*96) - (40+17*96) - (40+23*96) - (40+18*96)

    def ToggleGen6():
        DexMenu.dexScrollOffset = - (40+26*96) - (40+17*96) - (40+23*96) - (40+18*96) - (40+26*96)

    def ToggleGen7():
        DexMenu.dexScrollOffset = - (40+26*96) - (40+17*96) - (40+23*96) - (40+18*96) - (40+26*96) - (40+12*96)

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

#########################################################################################
#   SURFACE DEFINITIONS                                                                 #
#########################################################################################


        dexSurface = pygame.Surface((600,15000)).convert_alpha()

#########################################################################################
#   VARIABLE DEFINITIONS                                                                #
#########################################################################################

        selectionEngaged = False
        engagedMousePos = (0,0)

        clickCtr = 0
        scrollCooldown = 0

        scrollDecayEngaged = False
        scrDecFirstValue = (0,0)
        scrDecSecondValue = (0,0)
        scrDecCounter = 0
        scrollDecay = 0
        scrollDirectionUp = False

        selectClickEngaged = False
        passNextEngage = False

        passNextEngageCtr = 0

        mouseDexNr = 0

        idleCtr = 0

        pokeData = DexMenu.GetPokeDataAll() 
        generationData = DexMenu.GetGenerations()
 
#########################################################################################
#   LOADING LOOP                                                                        #
#########################################################################################
                          
        DexMenu.thread = Thread(target = DexMenu.LoadSpriteSheet, args = (dexSurface,generationData,)) 
        DexMenu.thread.start()

        while DexMenu.thread.isAlive():
            pygame.draw.rect(mainSurface,(40,40,40),(0,0,800,480))
            Text.Write(mainSurface,(400,140),"Loading...",30,"joy.otf",(200,200,200),True)
            pygame.display.update()
            clock.tick(10)
        
        while DexMenu.running:

            

            # Button Setup
            Button.idleColor = (255,255,255)
            Button.hoverColor = (200,200,200) 
            Button.fontColor = (255,0,0)
            Button.disabledColor = (150,150,150)
            Button.borderColor = (255,0,0)
            Button.fontFamily = "joy.otf"

             # Buttons Declarations
            btnToggleGen1 = Button.RoundRect(mainSurface,(10,130,125,40),15,"Gen. 1",18,1,DexMenu.ToggleGen1)
            btnToggleGen2 = Button.RoundRect(mainSurface,(10,180,125,40),15,"Gen. 2",18,1,DexMenu.ToggleGen2)
            btnToggleGen3 = Button.RoundRect(mainSurface,(10,230,125,40),15,"Gen. 3",18,1,DexMenu.ToggleGen3)
            btnToggleGen4 = Button.RoundRect(mainSurface,(10,280,125,40),15,"Gen. 4",18,1,DexMenu.ToggleGen4)
            btnToggleGen5 = Button.RoundRect(mainSurface,(10,330,125,40),15,"Gen. 5",18,1,DexMenu.ToggleGen5)
            btnToggleGen6 = Button.RoundRect(mainSurface,(10,380,125,40),15,"Gen. 6",18,1,DexMenu.ToggleGen6)
            btnToggleGen7 = Button.RoundRect(mainSurface,(10,430,125,40),15,"Gen. 7",18,1,DexMenu.ToggleGen7)

            btnBackButton = Button.RoundRect(mainSurface,(10,10,90,60),15,"< Back",18,1,DexMenu.ReturnToMenu)

            # One-Time Drawing routines
            mainSurface.fill((30,30,30))
            Draw.RoundRect(mainSurface,(40,40,40),(150,20,640,410),20,2,(255,0,0),"Pokedex")
            Draw.Pokeball(mainSurface,(140,35),(255,255,255),(40,40,40))

            pygame.display.update()

            DexMenu.reload = False

#########################################################################################
#   RUNNING LOOP                                                                        #
#########################################################################################

            while not DexMenu.reload:

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

                # Mouse Data
                mouse = pygame.mouse.get_pos()
                mouseRel = pygame.mouse.get_rel()
                click = pygame.mouse.get_pressed()

                # Drawing to Screen
                mainSurface.fill((30,30,30))
                mainSurface.blit(dexSurface,(170,50+DexMenu.dexScrollOffset))

                # Updating Buttons
                pygame.display.update(btnToggleGen1.Show())
                pygame.display.update(btnToggleGen2.Show())
                pygame.display.update(btnToggleGen3.Show())
                pygame.display.update(btnToggleGen4.Show())
                pygame.display.update(btnToggleGen5.Show())
                pygame.display.update(btnToggleGen6.Show())
                pygame.display.update(btnToggleGen7.Show())

                pygame.display.update(btnBackButton.Show())

                # Calculate Dex-Screen Values
                dexOffsetStep = abs(int(DexMenu.dexScrollOffset / 96))
                if mouseDexNr != None: Draw.DexCursor(mainSurface,(mouse[0],mouse[1]),"#" + str('{0:03d}'.format(mouseDexNr)))
                else: Draw.DexCursor(mainSurface,(mouse[0],mouse[1]))
                mouseDexPosRow = abs(DexMenu.dexScrollOffset) + mouse[1] - 50-40
                mouseDexPosRowOffset = 0
                mouseDexOffset = 0
                mouseDexPosRowOrig = mouseDexPosRow

                # Calculating the horizontal and vertical offset for each generation
                # Every generation 40 are added to compensate for the generation-banner
                # vertical offset is the "empty spaces" at the end of each generation added to the next one to
                # correct the dex number. 
                # Calc: DexRows*96 and (DexRows*96)+40
                if 0 < mouseDexPosRow <= 2496: 
                    mouseDexPosRowOffset -= 0
                    mouseDexOffset = 0
                elif 2496 + 40 < mouseDexPosRow <= 4168:  
                    mouseDexPosRowOffset -= 40
                    mouseDexOffset = 5
                elif 4168 + 40 < mouseDexPosRow <= 6416:  
                    mouseDexPosRowOffset -= 80
                    mouseDexOffset = 7
                elif 6416 + 40 < mouseDexPosRow <= 8184:  
                    mouseDexPosRowOffset -= 120
                    mouseDexOffset = 10
                elif 8184 + 40 < mouseDexPosRow <= 10720:  
                    mouseDexPosRowOffset -= 160
                    mouseDexOffset = 11
                elif 10720 + 40 < mouseDexPosRow <= 11912:  
                    mouseDexPosRowOffset -= 200
                    mouseDexOffset = 11
                elif 11912 + 40 < mouseDexPosRow <= 13296:  
                    mouseDexPosRowOffset -= 240
                    mouseDexOffset = 11
                elif 13296 + 40 < mouseDexPosRow <= 99999:  
                    mouseDexPosRowOffset -= 280
                    mouseDexOffset = 13
                else: 
                    mouseDexPosRowOffset = 0

                # Additional calculations for Dex-Screen
                mouseDexPosRow += mouseDexPosRowOffset
                mouseDexRow = math.ceil(mouseDexPosRow/96)-1
                mouseDexPosCol = mouse[0]-170
                mouseDexCol = math.ceil(mouseDexPosCol/96) - 1
                mouseDexNr = (mouseDexRow*6 + mouseDexCol)+1 - mouseDexOffset

                # Checking if the mouseDexNr is valid
                # Gets set to None when over an "empty field" for exsample
                if mouse[0] < 170: mouseDexNr = None
                elif 0 < mouseDexPosRow <= 2496 and generationData[0]["genDexStart"] <= mouseDexNr <= generationData[0]["genDexEnd"]: pass
                elif 2496 + 40 < mouseDexPosRowOrig <= 4168 and generationData[1]["genDexStart"] <= mouseDexNr <= generationData[1]["genDexEnd"]: pass
                elif 4168 + 40 < mouseDexPosRowOrig <= 6416 and generationData[2]["genDexStart"] <= mouseDexNr <= generationData[2]["genDexEnd"]: pass
                elif 6416 + 40 < mouseDexPosRowOrig <= 8184 and generationData[3]["genDexStart"] <= mouseDexNr <= generationData[3]["genDexEnd"]: pass
                elif 8184 + 40 < mouseDexPosRowOrig <= 10720 and generationData[4]["genDexStart"] <= mouseDexNr <= generationData[4]["genDexEnd"]: pass
                elif 10720 + 40 < mouseDexPosRowOrig <= 11912 and generationData[5]["genDexStart"] <= mouseDexNr <= generationData[5]["genDexEnd"]: pass
                elif 11912 + 40 < mouseDexPosRowOrig <= 13296 and generationData[6]["genDexStart"] <= mouseDexNr <= generationData[6]["genDexEnd"]: pass
                elif 13296 + 40 < mouseDexPosRowOrig <= 99999 and generationData[7]["genDexStart"] <= mouseDexNr <= generationData[7]["genDexEnd"]: pass   
                else:  mouseDexNr = None 


                # Click general
                if selectClickEngaged and passNextEngageCtr <= 0:
                    if click[0] == 0: 
                        if selecteEngagedPos[0]-10 < mouse[0] < selecteEngagedPos[0]+10 and selecteEngagedPos[1]-10 < mouse[1] < selecteEngagedPos[1]+10:
                            if mouseDexNr != None:
                                selectClickEngaged = False
                                DexMenu.reload = True
                                passNextEngageCtr = 10
                                selectedDex = DexInfo.Show(mouseDexNr)
                                #DexMenu.dexScrollOffset = -((DexMenu.GetPMGen(selectedDex)-1)*40 + ((selectedDex+2*DexMenu.GetPMGen(selectedDex)/6)*96) - (2*96))
                        selectClickEngaged = False

                if click[0] == 1 and not selectClickEngaged and passNextEngageCtr <= 0: 
                    selectClickEngaged = True
                    selecteEngagedPos = mouse
                passNextEngage = False
                if passNextEngageCtr > 0: passNextEngageCtr -= 1

                # Scrolling generall
                if click[0] == 1: clickCtr += 1
                else: clickCtr = 0

                if click[0] == 1 and clickCtr > 1:
                    DexMenu.dexScrollOffset += 2*mouseRel[1]
                    if DexMenu.dexScrollOffset > 0: DexMenu.dexScrollOffset = 0
                    if DexMenu.dexScrollOffset < -(802/6)*96 - 3*96: DexMenu.dexScrollOffset = -(802/6)*96 - 3*96

                # Sleep Trigger
                idleCtr += 1
                if click[0] == 1: idleCtr = 0
                if idleCtr > 1000:
                    idleCtr = 0
                    DexMenu.SleepState()
                    DexMenu.reload = True

                # Update Screen
                pygame.display.update((170,50,600,380))
                clock.tick(60)

        DexMenu.running = True
        return

    def SleepState():
        # PyGame Initialisation
        clock = pygame.time.Clock()

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

        run = True

        pygame.draw.rect(mainSurface,(40,40,40),(0,0,800,480))
        sleepSurface = pygame.Surface((600,300)).convert_alpha()
        sleepImg = pygame.image.load("sleeping.png").convert_alpha()

        runtimeCtr = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            click = pygame.mouse.get_pressed()

            if click[0] == 1:
                run = False

            sleepSurface.fill((40,40,40))
            sleepSurface.set_colorkey((0,0,0))
            if runtimeCtr % 2 == 0: sleepSurface.blit(sleepImg,(0,0))
            else: sleepSurface.blit(sleepImg,(-600,0))
            mainSurface.blit(sleepSurface,(100,180))
            Text.Write(mainSurface,(400,140),"Sleeping...",30,"joy.otf",(200,200,200),True)
            pygame.display.update()
                
            runtimeCtr += 1
            if runtimeCtr > 100: runtimeCtr = 0

            clock.tick(2)
        return