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
                """)
        return DexInfo.c.fetchall()

    def GetGenerations():
        DexInfo.c.execute("SELECT * FROM generations")
        return DexInfo.c.fetchall()

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




            # Define loaded sprites shonw on screen (rows)
            dexStartRange = 0
            dexEndRange = 6

            dexOffsetStep = abs(int(dexScrollOffset / 96))

         
            mainSurface.fill((30,30,30))
            dexSurface.fill((40,40,40))
            dexSurface.set_colorkey((0,0,0))

            Draw.RoundRect(mainSurface,(40,40,40),(150,20,640,410),20,2,(255,0,0),"Pokedex")
            Draw.Pokeball(mainSurface,(140,35),(255,0,0),(40,40,40))

            pokeData = DexMenu.GetPokeDataAll() 
            generationData = DexMenu.GetGenerations()

            row = 0

            selectedDexNumber = 1

            startDex = selectedDexNumber - 18
            endDex = selectedDexNumber + 18

           

            for gen in generationData:

                #print("==========="+ gen["genName"] + "===========")

                # Determine if Gen is included in range
                if (startDex < gen["genDexStart"] and endDex < gen["genDexStart"]) or (startDex > gen["genDexEnd"] and endDex > gen["genDexEnd"]): continue

                for pm in range(int(gen["genDexStart"]),int(gen["genDexEnd"]+1),6):

                    #if gen["genDexStart"] <= selectedDexNumber <= gen["genDexEnd"]:
                    #    colPos = (selectedDexNumber - gen["genDexStart"]) % 6


                    
                    for column in range(0,6):
                        if startDex <= pm <= endDex:
                            if pm <= int(gen["genDexEnd"]):
                                #print("Col " + str(column) + " Row " + str(row) + ": " + str(pm))
                                
                                pokeSprite = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(pm)) + "/sprite-small-FN-" + str('{0:03d}'.format(pm)) + ".png"),(96,96)).convert_alpha()
                                dexSurface.blit(pokeSprite,(column * 96, row * 96 + dexScrollOffset))
                                print(row)
                                
                                pm += 1
                            
                        else: break
                    row += 1

            mainSurface.blit(dexSurface,(170,50))        
                    



            #for row in range(dexStartRange + dexOffsetStep,dexEndRange + dexOffsetStep):
                
            #    rowCount = row

            #    for column in range(0,6):

            #        dexNumber = (row * 6 + column) + 1

            #        if 0 <= dexNumber <= 151: dexGen =1

            #        if dexNumber <= 151:
            #            pokeSprite = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(dexNumber)) + "/sprite-small-FN-" + str('{0:03d}'.format(dexNumber)) + ".png"),(96,96)).convert_alpha()
            #            dexSurface.blit(pokeSprite,(column * 96, row * 96 + dexScrollOffset)) 

            #mainSurface.blit(dexSurface,(170,50))


            #for x in range(dexStartRange + dexOffsetStep,dexEndRange + dexOffsetStep):

            #    print(dexOffsetStep*6)

            #    rowCount = x

            #    for m in range(0,6):
                    
            #        dexNumber = (x * 6 + m) + 1



            #        if dexNumber < 803:
            #            img = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(dexNumber)) + "/sprite-small-FN-" + str('{0:03d}'.format(dexNumber)) + ".png"),(96,96)).convert_alpha()

            #            if (m*96+170) < mouse[0]  < (m*96+96+170) and (x*96+dexScrollOffset+50) < mouse[1]  < (x*96+dexScrollOffset+96+50): 
            #                Draw.RRCursor(dexSurface,(40,40,40),((m*96)+2,(x*96+dexScrollOffset)+2,96-2,96-2),20,2,(255,255,255))

            #                # Additional condition for scroll support
            #                if click[0] == 1 and engagedMousePos == (0,0):
            #                    selectionEngaged = True
            #                    engagedMousePos = mouse
            #                if selectionEngaged and click[0] == 0:
            #                    selectionEngaged = False
            #                    if engagedMousePos[0] - 10 < mouse[0] < engagedMousePos[0] + 10 and engagedMousePos[1] - 10 < mouse[1] < engagedMousePos[1] + 10:
            #                        dexScrollOffset = -int(((DexInfo.Show(dexNumber) * 96)/6) - 2 * 96) 
            #                    engagedMousePos = (0,0)


            #            dexSurface.blit(img,(m * 96, x * 96 + dexScrollOffset)) 


            #mainSurface.blit(dexSurface,(170,50))





            # Scrolling generall
            if click[0] == 1: clickCtr += 1
            else: clickCtr = 0

            if click[0] == 1 and clickCtr > 1:
                dexScrollOffset += mouseRel[1]
                if dexScrollOffset > 0: dexScrollOffset = 0
                if dexScrollOffset < -(802/6)*96 + 3*96: dexScrollOffset = -(802/6)*96 + 3*96
               

            pygame.display.update()
            clock.tick(60)