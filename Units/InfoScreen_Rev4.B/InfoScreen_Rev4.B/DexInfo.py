# Importing Modules
import pygame
from pygame import gfxdraw
from threading import Thread
from multiprocessing.pool import ThreadPool
import time
import random
import sys
import sqlite3
import os

from Buttons import Button
from SpriteManager import Sprite
from CDrawing import Draw
from CText import Text




class DexInfo:

#########################################################################################
#   PROTECTED VARIABLES                                                                 #
#########################################################################################

    pokeData = None
    currentPokemon = 1
    running = True
    loadNewPokemon = False

    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    thread = Thread()

#########################################################################################
#   TOGGLE FUNCTION                                                                     #
#########################################################################################

    def ToggleNextDex():
        DexInfo.loadNewPokemon = True
        DexInfo.currentPokemon += 1
        if DexInfo.currentPokemon >= 803: DexInfo.currentPokemon = 1

    def TogglePrevDex():
        DexInfo.loadNewPokemon = True
        DexInfo.currentPokemon -= 1
        if DexInfo.currentPokemon <=  0: DexInfo.currentPokemon = 802

    def ToggleNextEvo():
        DexInfo.loadNewPokemon = True
        if DexInfo.pokeData["nextEvolution"] != None:
            DexInfo.currentPokemon = DexInfo.pokeData["nextEvolution"]

    def TogglePrevEvo():
        DexInfo.loadNewPokemon = True
        if DexInfo.pokeData["prevEvolution"] != None:
            DexInfo.currentPokemon = DexInfo.pokeData["prevEvolution"]

    def LoadSpritesheet():
        mouse = pygame.mouse.get_pos()
        if 320 < mouse[0] < 780 and 430 < mouse[1] < 460 :
            DexInfo.thread = Thread(target = Sprite.Create, args = ("spritesheets/Simplified/" + str(DexInfo.currentPokemon) + "FN.gif",DexInfo.currentPokemon,)) 
            DexInfo.thread.start()

    def EvoChain():
        evoChain = [DexInfo.currentPokemon]

        # get previous evolutions
        currentSelector = DexInfo.currentPokemon
        while True:
            parameters = (currentSelector,)
            DexInfo.c.execute("""SELECT * FROM evolutions WHERE evoNextDex = ?""",parameters)
            evoResult = DexInfo.c.fetchone()     
            if evoResult != None:
                evoChain.insert(0,evoResult["evoDex"])
                currentSelector = evoResult["evoDex"]
            else: break

        # get next evolutions
        currentSelector = DexInfo.currentPokemon
        while True:
            parameters = (currentSelector,)
            DexInfo.c.execute("""SELECT * FROM evolutions WHERE evoDex = ?""",parameters)
            evoResult = DexInfo.c.fetchone()     
            if evoResult != None:
                evoChain.append(evoResult["evoNextDex"])
                currentSelector = evoResult["evoNextDex"]
            else: break

        return evoChain 

#########################################################################################
#########################################################################################
#   MAIN START                                                                          #
#########################################################################################
#########################################################################################

    def Show(selectedPokemon):
   
#########################################################################################
#   INITIALISATION AND SETUP                                                            #
#########################################################################################

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

#########################################################################################
#   SURFACE DEFINITIONS                                                                 #
#########################################################################################

        spriteSurface = pygame.Surface((300,300)).convert_alpha()

#########################################################################################
#   VARIABLE DEFINITIONS                                                                #
#########################################################################################

        runtimeCtr = 0

        loadActiveCounter = 0
        spriteReloadTrigger = 30
        spriteReloaded = False


        thread = None

#########################################################################################
#   LOADING LOOP                                                                        #
#########################################################################################
 
        # Required for loading spritesheet the first time
        DexInfo.thread = Thread(target = Sprite.Create, args = ("spritesheets/Simplified/" + str(DexInfo.currentPokemon) + "FN.gif",DexInfo.currentPokemon,)) 
        DexInfo.thread.start()        


        while DexInfo.running:

            # Loading data
            parameters = (DexInfo.currentPokemon,)
            DexInfo.c.execute("""SELECT *,
                        evoNext.evoNextDex AS nextEvolution,
                        evoPrev.evoDex AS prevEvolution,
                        typeA.typeNameEN AS type1NameEN,
                        typeA.typeNameDE AS type1NameDE,
                        typeA.typeIconImage AS type1IconImage,
                        typeB.typeNameEN AS type2NameEN,
                        typeB.typeNameDE AS type2NameDE,
                        typeB.typeIconImage AS type2IconImage
                        FROM pokemon 
                        LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                        LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id 
                        LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id 
                        LEFT JOIN regions ON pokemon.regionID = regions.id 
                        LEFT JOIN evYieldTypes ON pokemon.evYieldTypeID = evYieldTypes.id
                        LEFT JOIN growthRates ON pokemon.growthRateID = growthRates.id
                        LEFT JOIN eggGroups ON pokemon.eggGroupID = eggGroups.id
                        LEFT JOIN evolutions AS evoNext ON pokemon.nationalDex = evoNext.evoDex
                        LEFT JOIN evolutions AS evoPrev ON pokemon.nationalDex = evoPrev.evoNextDex
                        WHERE pokemon.nationalDex = ?""",parameters)
            DexInfo.pokeData = DexInfo.c.fetchone()


            dexTypeColor = (int(DexInfo.pokeData["typeBGColor"].split(',')[0]), int(DexInfo.pokeData["typeBGColor"].split(',')[1]), int(DexInfo.pokeData["typeBGColor"].split(',')[2]))
            dexTypeColorDark = (int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[0]), int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[1]), int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[2]))


            # One-Time Drawing routines

            mainSurface.fill((30,30,30))

            Draw.RoundRect(mainSurface,(40,40,40),(520,10,270,130),15,2,dexTypeColor,"Stats")
            Draw.RoundRect(mainSurface,(40,40,40),(520,200,270,100),15,2,dexTypeColor,"Evolution Chain")
            Draw.RoundRect(mainSurface,(40,40,40),(520,310,270,60),15,2,dexTypeColor,"Gender Ratio")
            Draw.RoundRect(mainSurface,(40,40,40),(10,360,300,110),15,2,dexTypeColor)
            Draw.RoundRect(mainSurface,dexTypeColor,(10,300,400,115),15,2,dexTypeColor)
            Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)

            # Sprites
            Draw.RoundRect(mainSurface,(40,40,40),(412,18,90,90),21,2,dexTypeColor)
            spriteImg = pygame.image.load("sprites/" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) +"/sprite-small-FN-" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) + ".png")
            spriteImg = pygame.transform.scale(spriteImg,(96,96))
            mainSurface.blit(spriteImg,(412-3,18-3))
            Text.Write(mainSurface,(456,118),"Show Sprites",12,"joy.otf",(255,255,255),True)

            # Evo Chain
            evoImg = pygame.image.load("sprites/" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) +"/sprite-small-FN-" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) + ".png")
            evoImg = pygame.transform.scale(spriteImg,(96,96))
            mainSurface.blit(evoImg,(610,218))

            # Gender Ratio
            totalBarWidth = 255
            widthMale = DexInfo.pokeData["genderMale"]*(totalBarWidth/100)
            widthFemale = (100-DexInfo.pokeData["genderFemale"])*(totalBarWidth/100)

            #pygame.draw.rect(mainSurface,(255,0,0),(5+520,340,widthMale-5,20))
            #pygame.draw.rect(mainSurface,(0,255,0),(5+5+5+widthMale+520,340,widthFemale-5,20))

            if DexInfo.pokeData["genderMale"] < 100 and DexInfo.pokeData["genderMale"] > 0:
                pygame.draw.rect(mainSurface,dexTypeColor,(5+widthMale+520,335,5,35))
                Text.Write(mainSurface,(5+520+(widthMale/2),352),"M",25,"joy.otf",(255,255,255),True)
                Text.Write(mainSurface,(5+5+5+widthMale+520+(widthFemale/2),352),"F",25,"joy.otf",(255,255,255),True)
            elif DexInfo.pokeData["genderMale"] >= 100:
                Text.Write(mainSurface,(520+5+(255/2),352),"M",25,"joy.otf",(255,255,255),True)  
            else:
                Text.Write(mainSurface,(520+5+(255/2),352),"F",25,"joy.otf",(255,255,255),True)  


            

            Draw.RoundRect(mainSurface,(40,40,40),(20,374,110,39),10)
            Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(40,40,40))

            Text.Write(mainSurface,(28,376),"#" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])),35,"joy.otf",(255,255,255))
            Text.Write(mainSurface,(138,376),DexInfo.pokeData["nameEN"],35,"joy.otf",(255,255,255))
            Text.Write(mainSurface,(20,425),"Species:",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(20,445),"Region:",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(90,425),"Evolution Pokémon",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(90,445),DexInfo.pokeData["regionName"],20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(180,445),"Generation:",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(280,445),str(DexInfo.pokeData["regionID"]),20,"calibrilight.ttf",(255,255,255))

            pygame.draw.rect(mainSurface,dexTypeColor,(420,383,12,12))
            pygame.draw.rect(mainSurface,dexTypeColor,(436,383,24,12))
            pygame.draw.rect(mainSurface,dexTypeColor,(464,383,45,12))
            Text.Write(mainSurface,(425,396),"T  Y  P  E  :",18,"joy.otf",dexTypeColor)

            if DexInfo.pokeData["type2NameEN"] == None or DexInfo.pokeData["type2NameEN"] == "":
                Draw.TypeSignSingle(mainSurface,(520,380),dexTypeColor,DexInfo.pokeData["type1NameEN"])
            else:
                Draw.TypeSign1(mainSurface,(520,380),dexTypeColor,DexInfo.pokeData["type1NameEN"])
                Draw.TypeSign2(mainSurface,(645,380),dexTypeColorDark,DexInfo.pokeData["type2NameEN"])


            # Drawing Buttons before cycle (fixes visual bug)
            # Nav Buttons
            pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(320,430,100,30),10,"Prev Dex",15,"joy.otf",2,(255,255,255)))
            pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(440,430,100,30),10,"Prev Evo",15,"joy.otf",2,(255,255,255)))
            pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(560,430,100,30),10,"Next Evo",15,"joy.otf",2,(255,255,255)))
            pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(680,430,100,30),10,"Next Dex",15,"joy.otf",2,(255,255,255)))

            # Gender Buttons
            if DexInfo.pokeData["genderDifference"] == 1:
                pygame.display.update(Button.RoundRect(mainSurface,(60,60,240),(100,100,255),(255,255,255),(18,160,40,40),10,"M",25,"joy.otf",2,(255,255,255)))
                pygame.display.update(Button.RoundRect(mainSurface,(240,60,60),(255,100,100),(255,255,255),(18,210,40,40),10,"F",25,"joy.otf",2,(255,255,255)))
                    
            # Shiny Buttons
            pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(520,155,126,30),10,"Normal",18,"joy.otf",2,(255,255,255)))
            pygame.display.update(Button.RoundRect(mainSurface,(239,191,0),(255,226,63),(255,255,255),(661,155,126,30),10,"Shiny",18,"joy.otf",2,(255,255,255)))
                     

            print(DexInfo.EvoChain())
            
            pygame.display.update()

            spriteReloaded = False
            DexInfo.loadNewPokemon = False

#########################################################################################
#   RUNNING LOOP                                                                        #
#########################################################################################

            while not DexInfo.loadNewPokemon:

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


                if not DexInfo.thread.isAlive():

                    if DexInfo.pokeData["nextEvolution"] != None: nextEvoExists = True
                    else: nextEvoExists = False

                    if DexInfo.pokeData["prevEvolution"] != None: prevEvoExists = True
                    else: prevEvoExists = False

                    # Nav Buttons
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(320,430,100,30),10,"Prev Dex",15,"joy.otf",2,(255,255,255),DexInfo.TogglePrevDex,None,DexInfo.LoadSpritesheet))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(440,430,100,30),10,"Prev Evo",15,"joy.otf",2,(255,255,255),DexInfo.TogglePrevEvo,None,DexInfo.LoadSpritesheet,prevEvoExists))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(560,430,100,30),10,"Next Evo",15,"joy.otf",2,(255,255,255),DexInfo.ToggleNextEvo,None,DexInfo.LoadSpritesheet,nextEvoExists))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(680,430,100,30),10,"Next Dex",15,"joy.otf",2,(255,255,255),DexInfo.ToggleNextDex,None,DexInfo.LoadSpritesheet))
                    
                    # Gender Buttons
                    if DexInfo.pokeData["genderDifference"] == 1:
                        pygame.display.update(Button.RoundRect(mainSurface,(60,60,240),(100,100,255),(255,255,255),(18,160,40,40),10,"M",25,"joy.otf",2,(255,255,255)))
                        pygame.display.update(Button.RoundRect(mainSurface,(240,60,60),(255,100,100),(255,255,255),(18,210,40,40),10,"F",25,"joy.otf",2,(255,255,255)))
                    
                    # Shiny Buttons
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(520,155,126,30),10,"Normal",18,"joy.otf",2,(255,255,255)))
                    pygame.display.update(Button.RoundRect(mainSurface,(239,191,0),(255,226,63),(255,255,255),(661,155,126,30),10,"Shiny",18,"joy.otf",2,(255,255,255)))
                       
                
                else:
                    # Nav Buttons
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(320,430,100,30),10,"Prev Dex",15,"joy.otf",2,(255,255,255)))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(440,430,100,30),10,"Prev Evo",15,"joy.otf",2,(255,255,255)))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(560,430,100,30),10,"Next Evo",15,"joy.otf",2,(255,255,255)))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(680,430,100,30),10,"Next Dex",15,"joy.otf",2,(255,255,255)))

                    # Gender Buttons
                    if DexInfo.pokeData["genderDifference"] == 1:
                        pygame.display.update(Button.RoundRect(mainSurface,(60,60,240),(100,100,255),(255,255,255),(18,160,40,40),10,"M",25,"joy.otf",2,(255,255,255)))
                        pygame.display.update(Button.RoundRect(mainSurface,(240,60,60),(255,100,100),(255,255,255),(18,210,40,40),10,"F",25,"joy.otf",2,(255,255,255)))
                    
                    # Shiny Buttons
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(520,155,126,30),10,"Normal",18,"joy.otf",2,(255,255,255)))
                    pygame.display.update(Button.RoundRect(mainSurface,(239,191,0),(255,226,63),(255,255,255),(661,155,126,30),10,"Shiny",18,"joy.otf",2,(255,255,255)))
                       
                

                # Animation-Cycle for the Sprite
                if not DexInfo.thread.isAlive() and Sprite.loadedSpriteNr == DexInfo.currentPokemon:
                    if runtimeCtr % 1 == 0: 
                        Sprite.Cycle(Sprite.frameIndex,Sprite.tilesAmount,Sprite.frames)    
                        spriteSurface.fill((40,40,40))
                        spriteSurface.set_colorkey((0,0,0))
                        spriteSurface.blit(Sprite.current,Sprite.sprite)
                        mainSurface.blit(spriteSurface,(100,15))
                        pygame.display.update(100,15,300,300)
                else:
                    spriteSurface.fill((40,40,40))
                    spriteSurface.set_colorkey((0,0,0))
                    if runtimeCtr % 2 == 0:
                        pygame.gfxdraw.aacircle(spriteSurface,120,150,8,dexTypeColor)
                        pygame.gfxdraw.aacircle(spriteSurface,150,150,8,dexTypeColorDark)
                        pygame.gfxdraw.aacircle(spriteSurface,180,150,8,dexTypeColor)
                        pygame.gfxdraw.filled_circle(spriteSurface,120,150,8,dexTypeColor)
                        pygame.gfxdraw.filled_circle(spriteSurface,150,150,8,dexTypeColorDark)
                        pygame.gfxdraw.filled_circle(spriteSurface,180,150,8,dexTypeColor)
                    else:
                        pygame.gfxdraw.aacircle(spriteSurface,120,150,8,dexTypeColorDark)
                        pygame.gfxdraw.aacircle(spriteSurface,150,150,8,dexTypeColor)
                        pygame.gfxdraw.aacircle(spriteSurface,180,150,8,dexTypeColorDark)
                        pygame.gfxdraw.filled_circle(spriteSurface,120,150,8,dexTypeColorDark)
                        pygame.gfxdraw.filled_circle(spriteSurface,150,150,8,dexTypeColor)
                        pygame.gfxdraw.filled_circle(spriteSurface,180,150,8,dexTypeColorDark)
                    mainSurface.blit(spriteSurface,(100,60))
                    pygame.display.update(100,60,300,300)

                clock.tick(60)

                runtimeCtr += 1
                if runtimeCtr > 10000: runtimeCtr = 1

                # Re-Triggers sprite-loading if thread failed
                if Sprite.loadedSpriteNr != DexInfo.currentPokemon: loadActiveCounter += 1
                else: loadActiveCounter = 0

                if not spriteReloaded and loadActiveCounter >= spriteReloadTrigger: 
                    print("Retriggering")
                    DexInfo.thread = Thread(target = Sprite.Create, args = ("spritesheets/Simplified/" + str(DexInfo.currentPokemon) + "FN.gif",DexInfo.currentPokemon,)) 
                    DexInfo.thread.start()     
                    spriteReloaded = True


        return  DexInfo.currentPokemon