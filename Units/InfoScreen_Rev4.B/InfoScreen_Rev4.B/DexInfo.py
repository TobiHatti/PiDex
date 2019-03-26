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




class DexInfo:

#########################################################################################
#   PROTECTED VARIABLES                                                                 #
#########################################################################################

    pokeData = None
    evoChain = None
    currentPokemon = 1
    running = True
    loadNewPokemon = False
    evoScreenActive = False
    evoSelectActive = False
    statsScreenActive = False

    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    thread = Thread()

#########################################################################################
#   TOGGLE FUNCTION                                                                     #
#########################################################################################
    
    def ToggleStatsScreen():
        if DexInfo.statsScreenActive: DexInfo.statsScreenActive = False
        else: DexInfo.statsScreenActive = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.evoScreenActive = False
        DexInfo.evoSelectActive = False
    
    def ToggleEvoSelector():
        if DexInfo.evoSelectActive: DexInfo.evoSelectActive = False
        else: DexInfo.evoSelectActive = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.evoScreenActive = False
        DexInfo.statsScreenActive = False

    def ToggleEvoChainScreen():
        if DexInfo.evoScreenActive: DexInfo.evoScreenActive = False
        else: DexInfo.evoScreenActive = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.evoSelectActive = False
        DexInfo.statsScreenActive = False

    def ToggleNextDex():
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.currentPokemon += 1
        if DexInfo.currentPokemon >= 803: DexInfo.currentPokemon = 1

    def TogglePrevDex():
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.currentPokemon -= 1
        if DexInfo.currentPokemon <=  0: DexInfo.currentPokemon = 802

    def ToggleNextEvo():
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        if DexInfo.pokeData["nextEvolution"] != None:
            DexInfo.currentPokemon = DexInfo.pokeData["nextEvolution"]

    def TogglePrevEvo():
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        if DexInfo.pokeData["prevEvolution"] != None:
            DexInfo.currentPokemon = DexInfo.pokeData["prevEvolution"]

    def ToggleDexNumber(dexNumber):
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.currentPokemon = dexNumber

    def LoadSpritesheet():
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

    def FullChain():
        simpleChain = DexInfo.EvoChain()
        fullChain = [[simpleChain[0]]]
        fullChainSegment = []

        for sCh in simpleChain:
            currentSelector = sCh
            fullChainSegment = []

            parameters = (currentSelector,)
            DexInfo.c.execute("""SELECT * FROM evolutions WHERE evoDex = ?""",parameters)
            evoResults = DexInfo.c.fetchall()
            for evoResult in evoResults:
                if evoResult != None:
                    fullChainSegment.append(evoResult["evoNextDex"])
            if len(fullChainSegment) != 0:
                fullChain.append(fullChainSegment)

        return fullChain

    def NextEvolutions():
        nextEvos = []
        parameters = (DexInfo.currentPokemon,)
        DexInfo.c.execute("""SELECT * FROM evolutions WHERE evoDex = ?""",parameters)
        evoResults = DexInfo.c.fetchall()
        for evoResult in evoResults:
            if evoResult != None:
                nextEvos.append(evoResult["evoNextDex"])
        return nextEvos

    def HasMultipleEvos():

        parameters = (DexInfo.currentPokemon,)
        DexInfo.c.execute("SELECT * FROM evolutions WHERE evoDex = ?",parameters)
        evoResults = DexInfo.c.fetchall()
        if len(evoResults) > 1: return True
        else: return False

    def GetTypeColors(dexNumber):
        parameters = (dexNumber,)
        DexInfo.c.execute("SELECT * FROM pokemon LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id WHERE pokemon.nationalDex = ?",parameters)
        pmResult = DexInfo.c.fetchone()

        colorA = (int(pmResult["typeBGColor"].split(',')[0]), int(pmResult["typeBGColor"].split(',')[1]), int(pmResult["typeBGColor"].split(',')[2]))
        colorB = (int(pmResult["typeBtnHoverColor"].split(',')[0]), int(pmResult["typeBtnHoverColor"].split(',')[1]), int(pmResult["typeBtnHoverColor"].split(',')[2]))

        return (colorA,colorB)

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

        evoChainSurface = pygame.Surface((500-26,360-26)).convert_alpha()

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

        
        # Loading min and max values for stats
        statMinMaxVals = []
        statTypes = ("statHP","statAtk","statDef","statSpAtk","statSpDef","statSpd")
        for stat in statTypes:
            statSegment = []
            DexInfo.c.execute("SELECT * FROM pokemon WHERE " + stat + " NOT NULL ORDER BY " + stat + " ASC")
            statResMin = DexInfo.c.fetchone()
            statSegment.append(statResMin[stat])
            DexInfo.c.execute("SELECT * FROM pokemon ORDER BY " + stat + " DESC")
            statResMax= DexInfo.c.fetchone()
            statSegment.append(statResMax[stat])
            statMinMaxVals.append(statSegment)
           

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
                        LEFT JOIN evYields ON pokemon.nationalDex = evYields.nationalDex
                        LEFT JOIN evYieldTypes ON evYields.evYieldTypeID = evYieldTypes.id
                        LEFT JOIN growthRates ON pokemon.growthRateID = growthRates.id
                        LEFT JOIN eggGroups ON pokemon.eggGroupID = eggGroups.id
                        LEFT JOIN evolutions AS evoNext ON pokemon.nationalDex = evoNext.evoDex
                        LEFT JOIN evolutions AS evoPrev ON pokemon.nationalDex = evoPrev.evoNextDex
                        WHERE pokemon.nationalDex = ?""",parameters)
            DexInfo.pokeData = DexInfo.c.fetchone()


            dexTypeColor = (int(DexInfo.pokeData["typeBGColor"].split(',')[0]), int(DexInfo.pokeData["typeBGColor"].split(',')[1]), int(DexInfo.pokeData["typeBGColor"].split(',')[2]))
            dexTypeColorDark = (int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[0]), int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[1]), int(DexInfo.pokeData["typeBtnHoverColor"].split(',')[2]))

            # Button Setup
            Button.idleColor = dexTypeColor
            Button.hoverColor = dexTypeColorDark 
            Button.fontColor = (255,255,255)
            Button.disabledColor = (150,150,150)
            Button.borderColor = (255,255,255)
            Button.fontFamily = "joy.otf"

            # Nav Buttons
            btnPrevDex = Button.RoundRect(mainSurface,(320,430,100,30),10,"Prev Dex",15,2,DexInfo.TogglePrevDex,None,DexInfo.LoadSpritesheet)
            btnPrevEvo = Button.RoundRect(mainSurface,(440,430,100,30),10,"Prev Evo",15,2,DexInfo.TogglePrevEvo,None,DexInfo.LoadSpritesheet)
            btnNextEvo = Button.RoundRect(mainSurface,(560,430,100,30),10,"Next Evo",15,2,DexInfo.ToggleNextEvo,None,DexInfo.LoadSpritesheet)
            btnNextEvoSelect = Button.RoundRect(mainSurface,(560,430,100,30),10,"Next Evo",15,2,DexInfo.ToggleEvoSelector)
            btnNextDex = Button.RoundRect(mainSurface,(680,430,100,30),10,"Next Dex",15,2,DexInfo.ToggleNextDex,None,DexInfo.LoadSpritesheet)

            # Gender Buttons
            btnGenderM = Button.RoundRect(mainSurface,(18,160,40,40),10,"M",25,2)
            btnGenderF = Button.RoundRect(mainSurface,(18,210,40,40),10,"F",25,2)

            # Form Buttons
            btnFormNormal = Button.RoundRect(mainSurface,(520,155,126,30),10,"Normal",18,2)
            btnFormShiny = Button.RoundRect(mainSurface,(661,155,126,30),10,"Shiny",18,2)

            # ScreenToggle Buttons
            btnEvoChainScreen = Button.RoundRect(mainSurface,(745,230,40,65),15,"E-C",20,2,DexInfo.ToggleEvoChainScreen)
            btnStatsScreen = Button.RoundRect(mainSurface,(525+115,90,146,45),15,"More Stats",17,None,DexInfo.ToggleStatsScreen)

            

            # One-Time Drawing routines

            mainSurface.fill((30,30,30))

            
            Draw.RoundRect(mainSurface,(40,40,40),(520,10,270,130),15,2,dexTypeColor,"Stats")
            Draw.RoundRect(mainSurface,(40,40,40),(525,40,110,45),10,1,dexTypeColor,"")
            Text.Write(mainSurface,(525+55,50),"Height",17,"joy.otf",(255,255,255),True)
            Text.Write(mainSurface,(525+55,73),str('{0:.2f}'.format(DexInfo.pokeData["height"]/10)) + " m",19,"joy.otf",(255,255,255),True)
            Draw.RoundRect(mainSurface,(40,40,40),(525,90,110,45),10,1,dexTypeColor,"")
            Text.Write(mainSurface,(525+55,100),"Weight",17,"joy.otf",(255,255,255),True)
            Text.Write(mainSurface,(525+55,123),str('{0:.2f}'.format(DexInfo.pokeData["weight"]/10)) + " kg",19,"joy.otf",(255,255,255),True)
            Draw.RoundRect(mainSurface,(40,40,40),(525+115,40,146,45),10,1,dexTypeColor,"")
            Text.Write(mainSurface,(525+115+73,50),"Egg Group",17,"joy.otf",(255,255,255),True)
            Text.Write(mainSurface,(525+115+73,73),DexInfo.pokeData["eggGroupNameEN"],17,"joy.otf",(255,255,255),True)
            Draw.RoundRect(mainSurface,(40,40,40),(520,200,270,100),15,2,dexTypeColor,"Evolution Chain")
            Draw.RoundRect(mainSurface,(40,40,40),(520,310,270,60),15,2,dexTypeColor,"Gender Ratio")
            Draw.RoundRect(mainSurface,(40,40,40),(10,360,300,110),15,2,dexTypeColor)
            Draw.RoundRect(mainSurface,dexTypeColor,(10,300,400,115),15,2,dexTypeColor)
            Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)


            # Evo Chain
            evoImg = pygame.image.load("sprites/" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) +"/sprite-small-FN-" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) + ".png")
            evoImg = pygame.transform.scale(evoImg,(96,96))
            mainSurface.blit(evoImg,(610,218))

            # Gender Ratio
            totalBarWidth = 255
            widthMale = DexInfo.pokeData["genderMale"]*(totalBarWidth/100)
            widthFemale = (100-DexInfo.pokeData["genderFemale"])*(totalBarWidth/100)

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
            Text.Write(mainSurface,(90,425),DexInfo.pokeData["species"],20,"calibrilight.ttf",(255,255,255))
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
            pygame.display.update(btnPrevDex.Show(False))
            pygame.display.update(btnPrevEvo.Show(False))
            pygame.display.update(btnNextEvo.Show(False))
            pygame.display.update(btnNextDex.Show(False))


                    
            # Shiny Buttons
            pygame.display.update(btnFormNormal.Show(False))
            pygame.display.update(btnFormShiny.Show(False))

            # Screen Select Buttons
            pygame.display.update(btnEvoChainScreen.Show(False))
            pygame.display.update(btnStatsScreen.Show(False))


   
            DexInfo.evoChain = DexInfo.EvoChain()
            DexInfo.fullChain = DexInfo.FullChain()

            pygame.display.update()

            spriteReloaded = False
            DexInfo.loadNewPokemon = False

            DexInfo.oneTimeCycleLoad = True

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


                if DexInfo.pokeData["nextEvolution"] != None: nextEvoExists = True
                else: nextEvoExists = False

                if DexInfo.pokeData["prevEvolution"] != None: prevEvoExists = True
                else: prevEvoExists = False

############### RENDER ACTIVE BUTTONS ##################################################################
                if not DexInfo.thread.isAlive():
                    # Nav Buttons
                    pygame.display.update(btnPrevDex.Show())
                    pygame.display.update(btnPrevEvo.Show(disabled = not prevEvoExists))
                    if DexInfo.HasMultipleEvos(): pygame.display.update(btnNextEvoSelect.Show(disabled = not nextEvoExists))
                    else: pygame.display.update(btnNextEvo.Show(disabled = not nextEvoExists))
                    pygame.display.update(btnNextDex.Show())

                    

                    # Shiny Buttons
                    pygame.display.update(btnFormNormal.Show())
                    pygame.display.update(btnFormShiny.Show())

                    # Screen Select Buttons
                    pygame.display.update(btnEvoChainScreen.Show())
                    pygame.display.update(btnStatsScreen.Show())

############### RENDER DUMMY BUTTONS ###################################################################
                else:
                    # Nav Buttons
                    pygame.display.update(btnPrevDex.Show(False))
                    pygame.display.update(btnPrevEvo.Show(False,not prevEvoExists))
                    pygame.display.update(btnNextEvo.Show(False,not nextEvoExists))
                    pygame.display.update(btnNextDex.Show(False))

                    
                    # Shiny Buttons
                    pygame.display.update(btnFormNormal.Show(False))
                    pygame.display.update(btnFormShiny.Show(False))

                    # Screen Select Buttons
                    pygame.display.update(btnEvoChainScreen.Show(False))
                    pygame.display.update(btnStatsScreen.Show(False))

                # Animation-Cycle for the Sprite and Stat-Screens
############### STATUS SCREENS #########################################################################
                if DexInfo.statsScreenActive:
                    # Only load once 
                    if DexInfo.oneTimeCycleLoad:
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)
                        evoChainSurface.fill((40,40,40))
                        evoChainSurface.set_colorkey((0,0,0))
                        Text.Write(evoChainSurface,(70,0),"Pokemon",25,"joy.otf",(255,255,255))
                        Text.Write(evoChainSurface,(150,20),"stats",25,"joy.otf",(255,255,255))

                        Draw.RoundRect(evoChainSurface,(40,40,40),(5,50,250,282),15,2,dexTypeColor,"Base Stats")
                        UI.ProgressBar(evoChainSurface,(25,110),180,15,dexTypeColor,"HP",statMinMaxVals[0][0],statMinMaxVals[0][1],DexInfo.pokeData["statHP"])
                        UI.ProgressBar(evoChainSurface,(25,150),180,15,dexTypeColorDark,"Attack",statMinMaxVals[1][0],statMinMaxVals[1][1],DexInfo.pokeData["statAtk"])
                        UI.ProgressBar(evoChainSurface,(25,190),180,15,dexTypeColor,"Defense",statMinMaxVals[2][0],statMinMaxVals[2][1],DexInfo.pokeData["statDef"])
                        UI.ProgressBar(evoChainSurface,(25,230),180,15,dexTypeColorDark,"Special Attack",statMinMaxVals[3][0],statMinMaxVals[3][1],DexInfo.pokeData["statSpAtk"])
                        UI.ProgressBar(evoChainSurface,(25,270),180,15,dexTypeColor,"Special Defense",statMinMaxVals[4][0],statMinMaxVals[4][1],DexInfo.pokeData["statSpDef"])
                        UI.ProgressBar(evoChainSurface,(25,310),180,15,dexTypeColorDark,"Speed",statMinMaxVals[5][0],statMinMaxVals[5][1],DexInfo.pokeData["statSpd"])

                        Draw.RoundRect(evoChainSurface,(40,40,40),(265,2,205,150),15,2,dexTypeColor,"Training")
                        
                        Text.Write(evoChainSurface,(275,30),"Catch Rate:",15,"joy.otf",(180,180,180))
                        Text.Write(evoChainSurface,(380,30),str(DexInfo.pokeData["catchRate"]) + "%",15,"joy.otf",(255,255,255))
                        Text.Write(evoChainSurface,(275,50),"Base Friendship:",15,"joy.otf",(180,180,180))
                        Text.Write(evoChainSurface,(420,50),str(DexInfo.pokeData["baseFriendship"]),15,"joy.otf",(255,255,255))
                        Text.Write(evoChainSurface,(275,70),"Base Exp.:",15,"joy.otf",(180,180,180))
                        Text.Write(evoChainSurface,(365,70),str(DexInfo.pokeData["baseExp"]),15,"joy.otf",(255,255,255))
                        Text.Write(evoChainSurface,(275,90),"Growth.:",15,"joy.otf",(180,180,180))
                        Text.Write(evoChainSurface,(355,90),str(DexInfo.pokeData["growthRateEN"]),15,"joy.otf",(255,255,255))

                        Text.Write(evoChainSurface,(275,110),"EV-Yield:",15,"joy.otf",(180,180,180))
                        # Fetch EV-Yield data
                        parameters = (DexInfo.currentPokemon,)
                        DexInfo.c.execute("SELECT * FROM evYields LEFT JOIN evYieldTypes ON evYields.evYieldTypeID = evYieldTypes.id WHERE evYields.nationalDex = ?",parameters)
                        pmResult = DexInfo.c.fetchall()
                        evYieldTextOffset = 0
                        for evYield in pmResult:
                            Text.Write(evoChainSurface,(360,110 + evYieldTextOffset),str(evYield["evYieldPoints"]) + " " + evYield["evYieldTypeEN"],15,"joy.otf",(255,255,255))
                            evYieldTextOffset += 20


                        Draw.RoundRect(evoChainSurface,(40,40,40),(265,162,205,170),15,2,dexTypeColor,"Pokedex Entry")

                        Text.WriteMultiline(evoChainSurface,str(DexInfo.pokeData["dexInfo"]),(275,190),pygame.font.Font("calibrilight.ttf",18),(255,255,255))

                        mainSurface.blit(evoChainSurface,(23,23))
                        Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(40,40,40))
                    pygame.display.update(0,0,526,366)


############### EVO SELECTION SCREEN ###################################################################
                elif DexInfo.evoSelectActive:
                    # Only load once 
                    if DexInfo.oneTimeCycleLoad:
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)

                        evoChainSurface.fill((40,40,40))
                        evoChainSurface.set_colorkey((0,0,0))
                        if DexInfo.currentPokemon == 133: Text.Write(evoChainSurface,(250,30),"Select next eeveelution",25,"joy.otf",(255,255,255),True)
                        else: Text.Write(evoChainSurface,(250,30),"Select next evolution",25,"joy.otf",(255,255,255),True)
                        mainSurface.blit(evoChainSurface,(23,23))

                    horizontalOffset = 10
                    verticalOffset = 120

                    nextEvos = DexInfo.NextEvolutions()

                    if len(nextEvos) == 2: horizontalOffset = 140
                    elif len(nextEvos) == 3: horizontalOffset = 80
                    else: horizontalOffset = 10

                    if len(nextEvos) > 4: verticalOffset = 70

                    evoCount = 0

                    mouse = pygame.mouse.get_pos()
                    click = pygame.mouse.get_pressed()

                    for evo in nextEvos:

                        typeColors = DexInfo.GetTypeColors(evo)

                        if horizontalOffset+23-2 < mouse[0] < horizontalOffset+110+23+2 and verticalOffset+23-2 < mouse[1] < verticalOffset+96+23+2:
                            Draw.RoundRect(evoChainSurface,(40,40,40),(horizontalOffset,verticalOffset,96,110),15,2,typeColors[1],"#" + str('{0:03d}'.format(evo)))
                            if click[0] == 1: DexInfo.ToggleDexNumber(evo)

                        else: 
                            Draw.RoundRect(evoChainSurface,(40,40,40),(horizontalOffset,verticalOffset,96,110),15,2,typeColors[0],"#" + str('{0:03d}'.format(evo)))

                        nextEvoImg = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(evo)) +"/sprite-small-FN-" + str('{0:03d}'.format(evo)) + ".png"),(96,96))
                        evoChainSurface.blit(nextEvoImg,(horizontalOffset,verticalOffset+20))
                        horizontalOffset += 120
                        evoCount += 1
                        if evoCount >= 4:
                            horizontalOffset = 10
                            verticalOffset += 120
                            evoCount = 0
                    
                    
                    mainSurface.blit(evoChainSurface,(23,23))
                    Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(40,40,40))
                    pygame.display.update(0,0,526,366)

############### EVO CHAIN SCREEN #######################################################################
                elif DexInfo.evoScreenActive:

                    # Only load once 
                    if DexInfo.oneTimeCycleLoad:
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)

                        evoChainSurface.fill((40,40,40))
                        evoChainSurface.set_colorkey((0,0,0))
                        Text.Write(evoChainSurface,(250,30),"Evolution Chain",25,"joy.otf",(255,255,255),True)
                        Text.Write(evoChainSurface,(250,320),str(len(DexInfo.fullChain)) + " stage evolution-chain",20,"joy.otf",(255,255,255),True)

                        verticalOffset = 0
                        scaleFactor = 2
                        scaleOffsetCorrection = 48
                        scaleHorizontalCorrection = 48

                        if len(DexInfo.fullChain) == 1: horizontalOffset = 205
                        elif len(DexInfo.fullChain) == 2: horizontalOffset = 205 - 48 - 40
                        elif len(DexInfo.fullChain) == 3: horizontalOffset = 205 - 96 - 60
                        elif len(DexInfo.fullChain) == 4: horizontalOffset = 205 - 144 - 75

                        if len(DexInfo.fullChain) > 2: 
                            scaleFactor = 1
                            scaleOffsetCorrection = 0
                            scaleHorizontalCorrection = 0

                        for evoGroups in DexInfo.fullChain:
                            if len(evoGroups) > 1: 
                                scaleFactor = 1
                                scaleOffsetCorrection = 0
                                scaleHorizontalCorrection = 0

                        if len(DexInfo.fullChain) == 2 and scaleFactor == 2: horizontalOffset -= 20

                        for evoGroups in DexInfo.fullChain:

                            if len(evoGroups) == 1: verticalOffset = 131
                            elif len(evoGroups) == 2:verticalOffset = 83
                            else: verticalOffset = 35

                            evoItemCount = 0
                            for evoItem in evoGroups:
                                evoItemImg = pygame.transform.scale(pygame.image.load("sprites/" + str('{0:03d}'.format(evoItem)) +"/sprite-small-FN-" + str('{0:03d}'.format(evoItem)) + ".png"),(96*scaleFactor,96*scaleFactor))
                                evoChainSurface.blit(evoItemImg,(horizontalOffset-scaleOffsetCorrection,verticalOffset-scaleOffsetCorrection))
                                verticalOffset += 96
                                evoItemCount += 1
                                if evoItemCount >= 3: 
                                    horizontalOffset += 60
                                    verticalOffset = 35
                                    evoItemCount = 0
                            horizontalOffset += 150 + scaleHorizontalCorrection

                        mainSurface.blit(evoChainSurface,(23,23))
                        
                        Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(40,40,40))
                        pygame.display.update(0,0,526,366)

############### ANIMATED SPRITE CYCLE ##################################################################
                else:
                    # Gender Buttons
                    if DexInfo.pokeData["genderDifference"] == 1:              
                        pygame.display.update(btnGenderM.Show())
                        pygame.display.update(btnGenderF.Show())

                    if DexInfo.oneTimeCycleLoad: 
                        # Sprite-Box
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)
                        Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(40,40,40))
                        Draw.RoundRect(mainSurface,(40,40,40),(412,18,90,90),21,2,dexTypeColor)
                        spriteImg = pygame.image.load("sprites/" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) +"/sprite-small-FN-" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) + ".png")
                        spriteImg = pygame.transform.scale(spriteImg,(96,96))
                        mainSurface.blit(spriteImg,(412-3,18-3))
                        Text.Write(mainSurface,(456,118),"Show Sprites",12,"joy.otf",(255,255,255),True)
                        pygame.display.update(0,0,526,386)

                    if not DexInfo.thread.isAlive() and Sprite.loadedSpriteNr == DexInfo.currentPokemon:

                        if runtimeCtr % 1 == 0: 
                            Sprite.Cycle(Sprite.frameIndex,Sprite.tilesAmount,Sprite.frames)    
                            spriteSurface.fill((40,40,40))
                            spriteSurface.set_colorkey((0,0,0))
                            spriteSurface.blit(Sprite.current,Sprite.sprite)
                            mainSurface.blit(spriteSurface,(100,30))
                            pygame.display.update(100,30,300,300)
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
                        pygame.draw.rect(mainSurface,(40,40,40),(22,330,476,36))
                        mainSurface.blit(spriteSurface,(100,30))
                        pygame.display.update(100,30,300,300)

                clock.tick(60)

                runtimeCtr += 1
                if runtimeCtr > 10000: runtimeCtr = 1

                DexInfo.oneTimeCycleLoad = False

                # Re-Triggers sprite-loading if thread failed
                if Sprite.loadedSpriteNr != DexInfo.currentPokemon: loadActiveCounter += 1
                else: loadActiveCounter = 0

                if not spriteReloaded and loadActiveCounter >= spriteReloadTrigger: 
                    DexInfo.thread = Thread(target = Sprite.Create, args = ("spritesheets/Simplified/" + str(DexInfo.currentPokemon) + "FN.gif",DexInfo.currentPokemon,)) 
                    DexInfo.thread.start()     
                    spriteReloaded = True




        return  DexInfo.currentPokemon