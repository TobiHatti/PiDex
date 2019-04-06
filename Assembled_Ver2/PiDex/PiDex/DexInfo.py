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
    formData = None
    megaData = None
    megaDataSingle = None
    formDataAll = None

    evoChain = None
    currentPokemon = 1
    running = True
    loadNewPokemon = False
    evoScreenActive = False
    evoSelectActive = False
    statsScreenActive = False

    formNumberSelected = None

    megaEvolutionSelected = False
    megaEvolutionNumber = 0

    alolaFormSelected = False

    genderFemaleSelected = False

    shinySelected = False


    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    thread = Thread()
    sleepThread = Thread()

#########################################################################################
#   TOGGLE FUNCTION                                                                     #
#########################################################################################
    
    def ReturnToMenu():
        DexInfo.loadNewPokemon = True
        DexInfo.running = False

    def ToggleNextForm():
        DexInfo.formNumberSelected += 1
        if DexInfo.formNumberSelected > len(DexInfo.formDataAll): DexInfo.formNumberSelected = 1 

        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def TogglePrevForm():
        DexInfo.formNumberSelected -= 1
        if DexInfo.formNumberSelected < 1: DexInfo.formNumberSelected = len(DexInfo.formDataAll) 

        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleAlolaForm():
        if DexInfo.alolaFormSelected: DexInfo.alolaFormSelected = False
        else: DexInfo.alolaFormSelected = True
        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleShinyOn():
        DexInfo.shinySelected = True
        DexInfo.oneTimeCycleLoad = True
        DexInfo.LoadSpritesheet()

    def ToggleShinyOff():
        DexInfo.shinySelected = False
        DexInfo.oneTimeCycleLoad = True
        DexInfo.LoadSpritesheet()

    def ToggleMegaEvolution1():
        if DexInfo.megaEvolutionNumber == 1 and DexInfo.megaEvolutionSelected == True: DexInfo.megaEvolutionSelected = False
        else: DexInfo.megaEvolutionSelected = True
        DexInfo.megaEvolutionNumber = 1
        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleMegaEvolution2():
        if DexInfo.megaEvolutionNumber == 2 and DexInfo.megaEvolutionSelected == True: DexInfo.megaEvolutionSelected = False
        else: DexInfo.megaEvolutionSelected = True
        DexInfo.megaEvolutionNumber = 2
        DexInfo.loadNewPokemon = True

        DexInfo.LoadSpritesheet()

    def ToggleNormalMale():
        DexInfo.shinySelected = False
        DexInfo.genderFemaleSelected = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.LoadSpritesheet()

    def ToggleNormalFemale():
        DexInfo.shinySelected = False
        DexInfo.genderFemaleSelected = True
        DexInfo.megaEvolutionSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.LoadSpritesheet()

    def ToggleShinyMale():
        DexInfo.shinySelected = True
        DexInfo.genderFemaleSelected = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.LoadSpritesheet()

    def ToggleShinyFemale():
        DexInfo.shinySelected = True
        DexInfo.genderFemaleSelected = True
        DexInfo.megaEvolutionSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.oneTimeCycleLoad = True

        DexInfo.LoadSpritesheet()

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
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.currentPokemon += 1
        if DexInfo.currentPokemon >= 803: DexInfo.currentPokemon = 1

        DexInfo.LoadSpritesheet()

    def TogglePrevDex():
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.currentPokemon -= 1
        if DexInfo.currentPokemon <=  0: DexInfo.currentPokemon = 802

        DexInfo.LoadSpritesheet()

    def ToggleNextEvo():
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        if DexInfo.pokeData["nextEvolution"] != None:
            DexInfo.currentPokemon = DexInfo.pokeData["nextEvolution"]

        DexInfo.LoadSpritesheet()

    def TogglePrevEvo():
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        if DexInfo.pokeData["prevEvolution"] != None:
            DexInfo.currentPokemon = DexInfo.pokeData["prevEvolution"]

        DexInfo.LoadSpritesheet()

    def ToggleDexNumber(dexNumber):
        DexInfo.formNumberSelected = None
        DexInfo.alolaFormSelected = False
        DexInfo.loadNewPokemon = True
        DexInfo.evoSelectActive = False
        DexInfo.megaEvolutionSelected = False
        DexInfo.currentPokemon = dexNumber

        DexInfo.LoadSpritesheet()

    def GetPokeData(nationalDex):
        parameters = (nationalDex,)
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
                WHERE pokemon.nationalDex = ? 
                """,parameters)
        return DexInfo.c.fetchone()

    def GetMegaData(nationalDex):
        parameters = (nationalDex,)
        DexInfo.c.execute("""SELECT *,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon
                LEFT JOIN pokemonMega ON pokemon.nationalDex = pokemonMega.nationalDex
                LEFT JOIN megaStones ON pokemonMega.megaStoneID = megaStones.id
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND sprites.isMegaEvolution = 1
                LEFT JOIN types AS typeA ON pokemonMega.megaTypeID1 = typeA.id 
                LEFT JOIN types AS typeB ON pokemonMega.megaTypeID2 = typeB.id 
                WHERE pokemon.nationalDex = ?
                ORDER BY megaName ASC
                """,parameters)
        # Duplicate entries because of left join
        result = DexInfo.c.fetchall()
        if len(result) > 1: return [result[0],result[3]]
        else: return result

    def GetAlolaData(nationalDex):
        parameters = (nationalDex,)
        DexInfo.c.execute("""SELECT *,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon 
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND sprites.isAlolaForm = 1
                LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id 
                LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id 
                WHERE pokemon.nationalDex = ?
                """,parameters)
        return DexInfo.c.fetchone()


    def GetFormData(nationalDex,formNumber):
        parameters = (formNumber,formNumber,nationalDex,)
        DexInfo.c.execute("""SELECT *,
                typeA.typeName AS type1Name,
                typeB.typeName AS type2Name
                FROM pokemon 
                LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
                AND sprites.formNumber = ?
                LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id 
                LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id   
                LEFT JOIN pokemonForms ON pokemon.nationalDex = pokemonForms.nationalDex
                AND pokemonForms.formNumber = ?
                WHERE pokemon.nationalDex = ? 
                """,parameters)
        return DexInfo.c.fetchone()

    def GetFormDataAll(nationalDex):
        parameters = (nationalDex,)
        DexInfo.c.execute("""SELECT *
                FROM pokemonForms 
                WHERE nationalDex = ? 
                """,parameters)
        return DexInfo.c.fetchall()

    def LoadSpritesheet():

        pokeTmp = DexInfo.GetPokeData(DexInfo.currentPokemon)
        megaTmp = DexInfo.GetMegaData(DexInfo.currentPokemon)
        alolaTmp = DexInfo.GetAlolaData(DexInfo.currentPokemon)

        if pokeTmp["hasMultipleForms"] == 1 and DexInfo.formNumberSelected == None: DexInfo.formNumberSelected = pokeTmp["defaultForm"]
        formTmp = DexInfo.GetFormData(DexInfo.currentPokemon,DexInfo.formNumberSelected)

        

        if DexInfo.shinySelected:
        # SHINY
            # Spritesheets for Multiple Forms
            if pokeTmp["hasMultipleForms"] == 1:
                spriteFile = formTmp["spriteSheetHDFrontShiny"]

            # Spritesheets for Mega-Evolutions
            elif pokeTmp["hasMegaEvolution"] == 1 and DexInfo.megaEvolutionSelected:
                if len(megaTmp) > 1:
                    if DexInfo.megaEvolutionNumber == 1: spriteFile = megaTmp[0]["spriteSheetHDFrontShiny"]
                    else: spriteFile = megaTmp[1]["spriteSheetHDFrontShiny"]
                else: spriteFile = megaTmp[0]["spriteSheetHDFrontShiny"]

            # Spritesheets for Alola-Form
            elif pokeTmp["hasAlolaForm"] == 1 and DexInfo.alolaFormSelected:
                spriteFile = alolaTmp["spriteSheetHDFrontShiny"]

            # Spritesheets for Gender-Difference
            elif pokeTmp["genderDifference"] == 1:
                if DexInfo.genderFemaleSelected: spriteFile = pokeTmp["spriteSheetHDFrontFemaleShiny"]
                else: spriteFile = pokeTmp["spriteSheetHDFrontShiny"]

            # Default Spritesheet
            else:
                spriteFile = pokeTmp["spriteSheetHDFrontShiny"]
        else:
        # NORMAL
            # Spritesheets for Multiple Forms
            if pokeTmp["hasMultipleForms"] == 1:
                spriteFile = formTmp["spriteSheetHDFront"]

            # Spritesheets for Mega-Evolutions
            elif pokeTmp["hasMegaEvolution"] == 1 and DexInfo.megaEvolutionSelected:
                if len(megaTmp) > 1:
                    if DexInfo.megaEvolutionNumber == 1: spriteFile = megaTmp[0]["spriteSheetHDFront"]
                    else: spriteFile = megaTmp[1]["spriteSheetHDFront"]
                else: spriteFile = megaTmp[0]["spriteSheetHDFront"]

            # Spritesheets for Alola-Form
            elif pokeTmp["hasAlolaForm"] == 1 and DexInfo.alolaFormSelected:
                spriteFile = alolaTmp["spriteSheetHDFront"]

            # Spritesheets for Gender-Difference
            elif pokeTmp["genderDifference"] == 1:
                if DexInfo.genderFemaleSelected: spriteFile = pokeTmp["spriteSheetHDFrontFemale"]
                else: spriteFile = pokeTmp["spriteSheetHDFront"]

            # Default Spritesheet
            else:
                spriteFile = pokeTmp["spriteSheetHDFront"]

        DexInfo.thread = Thread(target = Sprite.Create, args = ("spriteSheets/" + str(spriteFile),DexInfo.currentPokemon,)) 
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

        colorA = (int(pmResult["typeColor"].split(',')[0]), int(pmResult["typeColor"].split(',')[1]), int(pmResult["typeColor"].split(',')[2]))
        colorB = (int(pmResult["typeColorBright"].split(',')[0]), int(pmResult["typeColorBright"].split(',')[1]), int(pmResult["typeColorBright"].split(',')[2]))

        return (colorA,colorB)

    def MegaEvolutionCount():
        parameters = (DexInfo.currentPokemon,)
        # CHANGE TO pokemonMega-Database
        DexInfo.c.execute("SELECT * FROM sprites WHERE nationalDex = ? AND isMegaEvolution = 1",parameters)
        pmResult = DexInfo.c.fetchall()

        if pmResult != None: return len(pmResult)
        else: return 0 

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

        spriteSurface = pygame.Surface((300,300)).convert_alpha()

        evoChainSurface = pygame.Surface((500-26,360-26)).convert_alpha()

#########################################################################################
#   VARIABLE DEFINITIONS                                                                #
#########################################################################################

        runtimeCtr = 0

        loadActiveCounter = 0
        spriteReloadTrigger = 10
        spriteReloaded = False

        thread = None

#########################################################################################
#   LOADING LOOP                                                                        #
#########################################################################################

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

        DexInfo.currentPokemon = selectedPokemon

        DexInfo.LoadSpritesheet()

        while DexInfo.running:

            # Loading data
            DexInfo.pokeData = DexInfo.GetPokeData(DexInfo.currentPokemon)

            if DexInfo.pokeData["hasMultipleForms"] == 1 and DexInfo.formNumberSelected == None: DexInfo.formNumberSelected = DexInfo.pokeData["defaultForm"]

            DexInfo.formData = DexInfo.GetFormData(DexInfo.currentPokemon,DexInfo.formNumberSelected)

            DexInfo.formDataAll = DexInfo.GetFormDataAll(DexInfo.currentPokemon)

            DexInfo.megaData = DexInfo.GetMegaData(DexInfo.currentPokemon)

            DexInfo.alolaData = DexInfo.GetAlolaData(DexInfo.currentPokemon)

            # Set default Form
            
            if DexInfo.megaEvolutionSelected:
                if len(DexInfo.megaData) > 1:
                    if DexInfo.megaEvolutionNumber == 1: DexInfo.megaDataSingle = DexInfo.megaData[0] 
                    else: DexInfo.megaDataSingle = DexInfo.megaData[1]
                else: DexInfo.megaDataSingle = DexInfo.megaData[0]

            dexTypeColor = (int(DexInfo.pokeData["typeColor"].split(',')[0]), int(DexInfo.pokeData["typeColor"].split(',')[1]), int(DexInfo.pokeData["typeColor"].split(',')[2]))
            dexTypeColorDark = (int(DexInfo.pokeData["typeColorBright"].split(',')[0]), int(DexInfo.pokeData["typeColorBright"].split(',')[1]), int(DexInfo.pokeData["typeColorBright"].split(',')[2]))

            # Button Setup
            Button.idleColor = dexTypeColor
            Button.hoverColor = dexTypeColorDark 
            Button.fontColor = (255,255,255)
            Button.disabledColor = (150,150,150)
            Button.borderColor = (255,255,255)
            Button.fontFamily = "joy.otf"

            # Nav Buttons
            btnPrevDex = Button.RoundRect(mainSurface,(320,425,110,40),15,"Prev Dex",18,1,DexInfo.TogglePrevDex,None,None,None,60,5)
            btnPrevEvo = Button.RoundRect(mainSurface,(440,425,110,40),15,"Prev Evo",18,1,DexInfo.TogglePrevEvo,None,None,None,60,5)
            btnNextEvo = Button.RoundRect(mainSurface,(560,425,110,40),15,"Next Evo",18,1,DexInfo.ToggleNextEvo,None,None,None,60,5)
            btnNextEvoSelect = Button.RoundRect(mainSurface,(560,425,110,40),15,"Next Evo",18,1,DexInfo.ToggleEvoSelector,None,None,None,60,5)
            btnReturn = Button.RoundRect(mainSurface,(15,80,80,40),18,"< Back",18,1,DexInfo.ReturnToMenu,None,None,None,60,5)

            btnNextDex = Button.RoundRect(mainSurface,(680,425,110,40),15,"Next Dex",18,1,DexInfo.ToggleNextDex,None,None,None,60,5)

            # Gender Buttons
            btnFormNormal = Button.RoundRect(mainSurface,(520,150,126,40),15,"Normal",20,1,DexInfo.ToggleShinyOff,None,None,None,10)
            btnFormShiny = Button.RoundRect(mainSurface,(661,150,126,40),15,"Shiny",20,1,DexInfo.ToggleShinyOn,None,None,None,10)

            btnFormNormalMale = Button.RoundRect(mainSurface,(520,150,60,40),15,"M",25,1,DexInfo.ToggleNormalMale,None,None,None,10)
            btnFormNormalFemale = Button.RoundRect(mainSurface,(520 + 66,150,60,40),15,"F",25,1,DexInfo.ToggleNormalFemale,None,None,None,10)
            btnFormShinyMale = Button.RoundRect(mainSurface,(661,150,60,40),15,"SM",25,1,DexInfo.ToggleShinyMale,None,None,None,10)
            btnFormShinyFemale = Button.RoundRect(mainSurface,(661 + 66,150,60,40),15,"SF",25,1,DexInfo.ToggleShinyFemale,None,None,None,10)

            # Alola Button
            btnAlolaToggle = Button.RoundRect(mainSurface,(16,325,70,40),18,"Alola",18,1,DexInfo.ToggleAlolaForm,None,None,None,40,30)

            # Form Selectors
            btnNextForm = Button.RoundRect(mainSurface,(465,160,40,80),18,">",18,1,DexInfo.ToggleNextForm,None,None,None,40,50)
            btnPrevForm = Button.RoundRect(mainSurface,(15,160,40,80),18,"<",18,1,DexInfo.TogglePrevForm,None,None,None,40,50)

            # MegaEvolution Buttons
            btnMegaEvo1 = Button.RoundRect(mainSurface,(18,280,40,40),10,"ME1",25,1,DexInfo.ToggleMegaEvolution1,None,None,None,0,30)
            btnMegaEvo2 = Button.RoundRect(mainSurface,(18,340,40,40),10,"ME2",25,1,DexInfo.ToggleMegaEvolution2,None,None,None,0,30)

            # ScreenToggle Buttons
            btnEvoChainScreen = Button.RoundRect(mainSurface,(745,230,40,65),15,"E-C",20,1,DexInfo.ToggleEvoChainScreen,None,None,None,10,10)
            btnStatsScreen = Button.RoundRect(mainSurface,(525+115,90,146,45),15,"More Stats",17,None,DexInfo.ToggleStatsScreen,None,None,None,10)

            

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
            Text.Write(mainSurface,(525+115+73,73),DexInfo.pokeData["eggGroupName"],17,"joy.otf",(255,255,255),True)
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
            
            if DexInfo.megaEvolutionSelected: Text.Write(mainSurface,(138,382),DexInfo.megaDataSingle["megaName"],25,"joy.otf",(255,255,255))
            else: Text.Write(mainSurface,(138,376),DexInfo.pokeData["name"],35,"joy.otf",(255,255,255))

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

            if DexInfo.megaEvolutionSelected:
                if DexInfo.megaDataSingle["type2Name"] == None or DexInfo.megaDataSingle["type2Name"] == "":
                    Draw.TypeSignSingle(mainSurface,(520,380),dexTypeColor,DexInfo.megaDataSingle["type1Name"])
                else:
                    Draw.TypeSign1(mainSurface,(520,380),dexTypeColor,DexInfo.megaDataSingle["type1Name"])
                    Draw.TypeSign2(mainSurface,(645,380),dexTypeColorDark,DexInfo.megaDataSingle["type2Name"])
            else:
                if DexInfo.pokeData["type2Name"] == None or DexInfo.pokeData["type2Name"] == "":
                    Draw.TypeSignSingle(mainSurface,(520,380),dexTypeColor,DexInfo.pokeData["type1Name"])
                else:
                    Draw.TypeSign1(mainSurface,(520,380),dexTypeColor,DexInfo.pokeData["type1Name"])
                    Draw.TypeSign2(mainSurface,(645,380),dexTypeColorDark,DexInfo.pokeData["type2Name"])


            

            # Drawing Buttons before cycle (fixes visual bug)
            # Nav Buttons
            pygame.display.update(btnPrevDex.Show(False))
            pygame.display.update(btnPrevEvo.Show(False))
            pygame.display.update(btnNextEvo.Show(False))
            pygame.display.update(btnNextDex.Show(False))

            if not DexInfo.statsScreenActive and not DexInfo.evoSelectActive:
                pygame.display.update(btnReturn.Show(False))


                    
            # Gender & Form Buttons
            if DexInfo.pokeData["genderDifference"] == 1 and not DexInfo.alolaFormSelected:    
                pygame.display.update(btnFormNormalMale.Show(False))
                pygame.display.update(btnFormNormalFemale.Show(False))
                pygame.display.update(btnFormShinyMale.Show(False))
                pygame.display.update(btnFormShinyFemale.Show(False))
            else:
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

                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()


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
                    
                    if not DexInfo.statsScreenActive and not DexInfo.evoSelectActive:
                        pygame.display.update(btnReturn.Show())


                    # Gender & Form Buttons
                    if DexInfo.pokeData["genderDifference"] == 1 and not DexInfo.alolaFormSelected:    
                        pygame.display.update(btnFormNormalMale.Show())
                        pygame.display.update(btnFormNormalFemale.Show())
                        pygame.display.update(btnFormShinyMale.Show())
                        pygame.display.update(btnFormShinyFemale.Show())
                    else:
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
                    
                    if not DexInfo.statsScreenActive and not DexInfo.evoSelectActive:
                        pygame.display.update(btnReturn.Show(False))
    
                    # Gender & Form Buttons
                    if DexInfo.pokeData["genderDifference"] == 1 and not DexInfo.alolaFormSelected:    
                        pygame.display.update(btnFormNormalMale.Show(False))
                        pygame.display.update(btnFormNormalFemale.Show(False))
                        pygame.display.update(btnFormShinyMale.Show(False))
                        pygame.display.update(btnFormShinyFemale.Show(False))
                    else:
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
                        Text.Write(evoChainSurface,(355,90),str(DexInfo.pokeData["growthRate"]),15,"joy.otf",(255,255,255))

                        Text.Write(evoChainSurface,(275,110),"EV-Yield:",15,"joy.otf",(180,180,180))
                        # Fetch EV-Yield data
                        parameters = (DexInfo.currentPokemon,)
                        DexInfo.c.execute("SELECT * FROM evYields LEFT JOIN evYieldTypes ON evYields.evYieldTypeID = evYieldTypes.id WHERE evYields.nationalDex = ?",parameters)
                        pmResult = DexInfo.c.fetchall()
                        evYieldTextOffset = 0
                        for evYield in pmResult:
                            Text.Write(evoChainSurface,(360,110 + evYieldTextOffset),str(evYield["evYieldPoints"]) + " " + evYield["evYieldType"],15,"joy.otf",(255,255,255))
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

                    # Form Buttons
                    if DexInfo.pokeData["hasMultipleForms"] == 1:
                        
                        pygame.display.update(btnNextForm.Show())
                        pygame.display.update(btnPrevForm.Show())

                    # Alola Form Button
                    if DexInfo.pokeData["hasAlolaForm"] == 1:
                        pygame.display.update(btnAlolaToggle.Show())

                    # Mega Evolution Buttons
                    if DexInfo.pokeData["hasMegaEvolution"] != None:
                        megaStoneImg = pygame.transform.scale(pygame.image.load("megaStones/" + DexInfo.megaData[0]["megaStoneImage"]),(80,80))
                        mainSurface.blit(megaStoneImg,(10,290))
                        if 10 < mouse[0] < 90 and 290 < mouse[1] < 370:
                            Text.Write(mainSurface,(50,330),"Mega",18,"joy.otf",dexTypeColor,True)
                            if not DexInfo.sleepThread.isAlive() and click[0] == 1: 
                                DexInfo.ToggleMegaEvolution1()
                                DexInfo.sleepThread = Thread(target = time.sleep, args = (0.3,)) 
                                DexInfo.sleepThread.start()    
                        else: Text.Write(mainSurface,(50,330),"Mega",18,"joy.otf",(0,0,0),True)
                        pygame.display.update((14,274,92,92))

                        if len(DexInfo.megaData) > 1: 
                            megaStoneImg = pygame.transform.scale(pygame.image.load("megaStones/" + DexInfo.megaData[1]["megaStoneImage"]),(80,80))
                            mainSurface.blit(megaStoneImg,(10,220))
                            if 10 < mouse[0] < 90 and 220 < mouse[1] < 300:
                                Text.Write(mainSurface,(50,260),"Mega",18,"joy.otf",dexTypeColor,True)
                                if not DexInfo.sleepThread.isAlive() and click[0] == 1: 
                                    DexInfo.ToggleMegaEvolution2()
                                    DexInfo.sleepThread = Thread(target = time.sleep, args = (0.3,)) 
                                    DexInfo.sleepThread.start()    
                            else: Text.Write(mainSurface,(50,260),"Mega",18,"joy.otf",(0,0,0),True)
                            pygame.display.update((14,204,92,92))

                        

                    if DexInfo.oneTimeCycleLoad: 
                        # Sprite-Box
                        Draw.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,dexTypeColor)
                        Draw.Pokeball(mainSurface,(35,35),dexTypeColor,(40,40,40))
                        Draw.RoundRect(mainSurface,(40,40,40),(412,18,90,90),21,2,dexTypeColor)
                        spriteImg = pygame.image.load("sprites/" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) +"/sprite-small-FN-" + str('{0:03d}'.format(DexInfo.pokeData["nationalDex"])) + ".png")
                        spriteImg = pygame.transform.scale(spriteImg,(96,96))
                        mainSurface.blit(spriteImg,(412-3,18-3))
                        Text.Write(mainSurface,(456,118),"Show Sprites",12,"joy.otf",(255,255,255),True)

                        if DexInfo.pokeData["hasMultipleForms"] == 1: Text.Write(mainSurface,(250,350),"Form: " + DexInfo.formData["formName"],25,"joy.otf",(255,255,255),True)
                        if DexInfo.shinySelected: Text.Write(mainSurface,(470,350),"S",30,"joy.otf",(255,255,255),True)
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
                    DexInfo.LoadSpritesheet()  
                    spriteReloaded = True

                idleCtr += 1
                if click[0] == 1: idleCtr = 0
                if idleCtr > 1000:
                    idleCtr = 0
                    DexInfo.SleepState()
                    DexInfo.oneTimeCycleLoad = True
                    DexInfo.loadNewPokemon = True
        
        DexInfo.running = True
        return  DexInfo.currentPokemon

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

