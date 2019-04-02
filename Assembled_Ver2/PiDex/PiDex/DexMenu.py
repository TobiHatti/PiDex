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


        

        

        # Define loaded sprites shonw on screen (rows)
        dexStartRange = 0
        dexEndRange = 6

       
        mainSurface.fill((30,30,30))

        Draw.RoundRect(mainSurface,(40,40,40),(150,20,640,410),20,2,(255,0,0),"Pokedex")
        Draw.Pokeball(mainSurface,(140,35),(255,0,0),(40,40,40))

        pokeData = DexMenu.GetPokeDataAll() 
        generationData = DexMenu.GetGenerations()


        pygame.display.update()

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


            mainSurface.fill((30,30,30))
            dexSurface.fill((40,40,40))
            dexSurface.set_colorkey((0,0,0))

            dexOffsetStep = abs(int(dexScrollOffset / 96))

            

            selectedDexNumber = 1

            startDex = selectedDexNumber - 4
            endDex = selectedDexNumber + 31


            dexGenOffset = 0          



            
            for pm in range(pm-10,pm+10):
                



            #for gen in generationData:

            #    row = 0

                

            #    # Offset after generation switch
            #    if int(gen["genNr"]) > 1 and int(gen["genNr"]) <=6: dexGenOffset += math.ceil((generationData[int(gen["genNr"])]["genDexEnd"]-generationData[int(gen["genNr"])]["genDexStart"]+1) / 6)

            #    print(dexGenOffset)

            #    # Determine if Gen is included in range
            #    if (startDex + dexOffsetStep*6 < gen["genDexStart"] and endDex + dexOffsetStep*6 < gen["genDexStart"]) or (startDex + dexOffsetStep*6 > gen["genDexEnd"] and endDex + dexOffsetStep*6 > gen["genDexEnd"]): continue
            #    else: print("GEN: " + str(gen["genName"]))

                

            #    for pm in range(int(gen["genDexStart"]),int(gen["genDexEnd"]+1),6):

            #        #print("=====" + str(row))

            #        for column in range(0,6):
            #            if startDex + dexOffsetStep*6 <= pm <= endDex + dexOffsetStep*6:
            #                if pm <= int(gen["genDexEnd"]):

            #                    pokeSprite = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(pm)) + "/sprite-small-FN-" + str('{0:03d}'.format(pm)) + ".png"),(96,96)).convert_alpha()
                                
            #                    if int(gen["genNr"] > 1): dexSurface.blit(pokeSprite,(column * 96, (dexGenOffset+row) * 96 + dexScrollOffset))
            #                    else: dexSurface.blit(pokeSprite,(column * 96, (dexGenOffset+row) * 96 + dexScrollOffset))
                               
            #                    #print(str(pm) + " in Col " + str((dexGenOffset+row)))
                                
            #                    pm += 1
                            
            #            else: break
            #        row += 1

                
                

            #mainSurface.blit(dexSurface,(170,50))        
            

            # Scrolling generall
            if click[0] == 1: clickCtr += 1
            else: clickCtr = 0

            if click[0] == 1 and clickCtr > 1:
                dexScrollOffset += mouseRel[1]
                if dexScrollOffset > 0: dexScrollOffset = 0
                if dexScrollOffset < -(802/6)*96 + 3*96: dexScrollOffset = -(802/6)*96 + 3*96
               

            pygame.display.update((170,50,600,380))
            clock.tick(60)