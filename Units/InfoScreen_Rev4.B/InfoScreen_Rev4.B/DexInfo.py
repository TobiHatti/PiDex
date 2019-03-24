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
        DexInfo.currentPokemon += 1
        if DexInfo.currentPokemon >= 803: DexInfo.currentPokemon = 1

    def TogglePrevEvo():
        DexInfo.loadNewPokemon = True
        DexInfo.currentPokemon -= 1
        if DexInfo.currentPokemon <=  0: DexInfo.currentPokemon = 802

    def LoadSpritesheet():
        DexInfo.thread = Thread(target = Sprite.Create, args = ("spritesheets/Simplified/" + str(DexInfo.currentPokemon) + "FN.gif",DexInfo.currentPokemon,)) 
        DexInfo.thread.start()
    

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

        conn = sqlite3.connect('pokemon.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()


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

       

        screenDistortOffsetHor1 = 0
        screenDistortOffsetHor2 = -200

        thread = None

#########################################################################################
#   LOADING LOOP                                                                        #
#########################################################################################
 
        DexInfo.LoadSpritesheet()

        while DexInfo.running:

            # Loading spritesheet

            #try:
            #    thread = Thread(target = Sprite.Create, args = ("spritesheets/Simplified/" + str(DexInfo.currentPokemon) + "FN.gif",)) 
       
            #    thread.start()
            #except: pass

            # Loading data
            parameters = (DexInfo.currentPokemon,)
            c.execute("""SELECT *,
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
                        LEFT JOIN evolutions AS evoPrev ON pokemon.nationalDex = evoNext.evoNextDex
                        WHERE pokemon.nationalDex = ?""",parameters)
            DexInfo.pokeData = c.fetchone()


            dexTypeColor = (int(DexInfo.pokeData["typeBGColor"].split(',')[0]), int(DexInfo.pokeData["typeBGColor"].split(',')[1]), int(DexInfo.pokeData["typeBGColor"].split(',')[2]))
            dexTypeColorDark = (int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[0]), int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[1]), int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[2]))


            # One-Time Drawing routines

            mainSurface.fill((30,30,30))

            Draw.RoundRect(mainSurface,(40,40,40),(520,10,270,130),15,2,dexTypeColor,"Stats")
            Draw.RoundRect(mainSurface,(40,40,40),(520,200,270,80),15,2,dexTypeColor,"Evolution Chain")
            Draw.RoundRect(mainSurface,(40,40,40),(520,290,270,80),15,2,dexTypeColor,"Gender Ratio")
            Draw.RoundRect(mainSurface,(40,40,40),(10,360,300,110),15,2,dexTypeColor)
            Draw.RoundRect(mainSurface,dexTypeColor,(10,300,400,115),15,2,dexTypeColor)
            Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)
            Draw.RoundRect(mainSurface,(40,40,40),(440,300,60,60),26,2,dexTypeColor)

            spriteImg = pygame.image.load("sprites/001/sprite-small-FN-001.png")
            mainSurface.blit(spriteImg,(440,300))

            Draw.RoundRect(mainSurface,(40,40,40),(20,374,110,39),10)
            Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(40,40,40))

            Text.Write(mainSurface,(28,376),"#" + str(DexInfo.currentPokemon),35,"joy.otf",(255,255,255))
            Text.Write(mainSurface,(138,376),DexInfo.pokeData["nameEN"],35,"joy.otf",(255,255,255))
            Text.Write(mainSurface,(20,425),"Species:",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(20,445),"Region:",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(90,425),"Evolution Pokémon",20,"calibrilight.ttf",(255,255,255))
            Text.Write(mainSurface,(90,445),DexInfo.pokeData["regionName"],20,"calibrilight.ttf",(255,255,255))

            pygame.draw.rect(mainSurface,dexTypeColor,(420,383,12,12))
            pygame.draw.rect(mainSurface,dexTypeColor,(436,383,24,12))
            pygame.draw.rect(mainSurface,dexTypeColor,(464,383,45,12))
            Text.Write(mainSurface,(425,396),"T  Y  P  E  :",18,"joy.otf",dexTypeColor)

            if DexInfo.pokeData["type2NameEN"] == None or DexInfo.pokeData["type2NameEN"] == "":
                Draw.TypeSignSingle(mainSurface,(520,380),dexTypeColor,DexInfo.pokeData["type1NameEN"])
            else:
                Draw.TypeSign1(mainSurface,(520,380),dexTypeColor,DexInfo.pokeData["type1NameEN"])
                Draw.TypeSign2(mainSurface,(645,380),dexTypeColorDark,DexInfo.pokeData["type2NameEN"])
            
            pygame.display.update()

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

                #pygame.draw.rect(mainSurface,(60,60,60),(0,screenDistortOffsetHor1,800,30))
                #screenDistortOffsetHor1 += 2
                #if screenDistortOffsetHor1 > 520: screenDistortOffsetHor1 = -30

                #pygame.draw.rect(mainSurface,(60,60,60),(0,screenDistortOffsetHor2,800,30))
                #screenDistortOffsetHor2 += 5
                #if screenDistortOffsetHor2 > 800: screenDistortOffsetHor2 = -60

                if not DexInfo.thread.isAlive():
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(320,430,100,30),10,"Prev Dex",15,"joy.otf",2,(255,255,255),DexInfo.TogglePrevDex,None,DexInfo.LoadSpritesheet))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(440,430,100,30),10,"Prev Evo",15,"joy.otf",2,(255,255,255),DexInfo.TogglePrevEvo,None,DexInfo.LoadSpritesheet))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(560,430,100,30),10,"Next Evo",15,"joy.otf",2,(255,255,255),DexInfo.ToggleNextEvo,None,DexInfo.LoadSpritesheet))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColor,dexTypeColorDark,(255,255,255),(680,430,100,30),10,"Next Dex",15,"joy.otf",2,(255,255,255),DexInfo.ToggleNextDex,None,DexInfo.LoadSpritesheet))
                else:
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(320,430,100,30),10,"Prev Dex",15,"joy.otf",2,(255,255,255)))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(440,430,100,30),10,"Prev Evo",15,"joy.otf",2,(255,255,255)))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(560,430,100,30),10,"Next Evo",15,"joy.otf",2,(255,255,255)))
                    pygame.display.update(Button.RoundRect(mainSurface,dexTypeColorDark,dexTypeColorDark,(255,255,255),(680,430,100,30),10,"Next Dex",15,"joy.otf",2,(255,255,255)))

                # Animation-Cycle for the Sprite
<<<<<<< HEAD
                if not thread.isAlive():
=======
                if not DexInfo.thread.isAlive() and Sprite.loadedSpriteNr == DexInfo.currentPokemon:
>>>>>>> fa60c9012f323b7a9597ea96511e849228604895
                    if runtimeCtr % 1 == 0: 
                        Sprite.Cycle(Sprite.frameIndex,Sprite.tilesAmount,Sprite.frames)    
                        spriteSurface.fill((40,40,40))
                        spriteSurface.set_colorkey((0,0,0))
                        spriteSurface.blit(Sprite.current,Sprite.sprite)
                        mainSurface.blit(spriteSurface,(100,60))
                        pygame.display.update(100,60,300,300)
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


        return  DexInfo.currentPokemon