#####################################################################################################################
#                                                                                                                   #
#   PIDEX POKEMON INFO-SCREEN                                                                                       #
#                                                                                                                   #
#####################################################################################################################

#####################################################################################################################
#   SETUP                                                                                                           #
#####################################################################################################################

# Importing Modules
import pygame
from pygame import gfxdraw
import time
import random
import sys
import sqlite3
import os

# Custom Classes
from statScreens import StatScreen
from basics import Basic

# DB-Initialisation and Setup
conn = sqlite3.connect('pokemon.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# PyGame Initialisation
pygame.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)

# Window and Surface Initialisation
displayWidth = 800
displayHeight = 480

mainSurface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
spriteSurface = pygame.Surface((300,300)).convert()
statsSurface = pygame.Surface((displayWidth-470,480)).convert()
menuSurface = pygame.Surface((150,480)).convert()

#####################################################################################################################
#   VARIBALES                                                                                                       #
#####################################################################################################################

# Main Colors
white = (255,255,255)
black = (0,0,0)

# Loop Conditions
returnToMenu = False
loadNewPokemon = False

# Runtime Variables
currentPokemon = 1
currentStatPage = 0

statsOffset = 0

# Counters
runtimeCounter = 0

# Sprite-specific variables
spriteFrameIndex = 0

# Stat-Page animation
statsMoveForward = False
nextStatPage = False
prevStatPage = False
flipStatPage = False

# Exit-Functions
exitActive = False
exitStep = 1
exitIteration = 0

# Swipe Support
swipeSensibility = 10
mouseRel=(0,0)
swipeLock = False


#####################################################################################################################
#   FUNCTIONS                                                                                                       #
#####################################################################################################################

def SpriteCreate(filePath):

    if os.path.isfile(filePath): sheet = pygame.image.load(filePath).convert()
    else: sheet = pygame.image.load("notFound.png").convert()
    
    imgWidth, imgHeight = sheet.get_size()
    spriteTiles = int(imgWidth / 300)
    spriteTilesVert = int(imgHeight / 300)
    cells = []
    spriteOffset = 0

    for r in range(spriteTilesVert):
        width, height = (300,300)
        for n in range(spriteTiles):
            
            rect = pygame.Rect(n * width, r * height,width,height)
            image = pygame.Surface(rect.size).convert()
            image.blit(sheet, (0,0),rect)
            alpha = image.get_at((0,0))
            image.set_colorkey(alpha)
            #image = pygame.transform.scale(image,(300,300))
            if r == spriteTilesVert-1:
                if image.get_at((150,150)) != (0,0,0,255): cells.append(image)
                else: spriteOffset += 1
            else:
                cells.append(image)
            
                

    playerImg = cells[0]
    player = playerImg.get_rect()
    player.center = (150,150)
    spriteFrame = 0
    return (spriteTiles * spriteTilesVert - spriteOffset,cells,playerImg,player)

def SpriteCycle(frame,tilesAmt,cells):
    spriteFrame = frame + 1
    if spriteFrame >= tilesAmt: spriteFrame = 0
    spriteImage = cells[spriteFrame]
    return (spriteFrame,spriteImage)


def MenuSurfaceContent(enableButton = True, pokeballOffset = 0):

    # Drawin menu-screen
    menuSurface.fill((64,64,64))
    menuSurface.set_colorkey((64,64,64))
    
    pygame.gfxdraw.aacircle(menuSurface,-200,int(displayHeight/2),300,colorMenuBarBackground)
    pygame.gfxdraw.filled_circle(menuSurface,-200,int(displayHeight/2),300,colorMenuBarBackground)
    pygame.gfxdraw.aacircle(menuSurface,-210,int(displayHeight/2),300,(64,64,64))
    pygame.gfxdraw.filled_circle(menuSurface,-210,int(displayHeight/2),300,(64,64,64))

    pokeballImage = pygame.image.load("pokeball.png").convert()
    menuSurface.blit(pokeballImage,(-250 + pokeballOffset,int(displayHeight/2)-150))

    # Menu Button and update
    Basic.Button(menuSurface,(45,int(displayHeight/2)-170),25,"DEX >",15,colorButtonIdle,colorButtonText,ToggleLoadNextDex,None,(0,0),enableButton)
    Basic.Button(menuSurface,(80,int(displayHeight/2)-90),28,"DEX <",15,colorButtonIdle,colorButtonText,ToggleLoadPrevDex,None,(0,0),enableButton)
    Basic.Button(menuSurface,(95,int(displayHeight/2)),30,"BACK",15,colorButtonIdle,colorButtonText,ToggleReturnToMainMenu,None,(0,0),enableButton)
    Basic.Button(menuSurface,(80,int(displayHeight/2)+90),28,"EVO >",15,colorButtonIdle,colorButtonText,ToggleLoadNextEvo,None,(0,0),enableButton)
    Basic.Button(menuSurface,(45,int(displayHeight/2)+170),25,"EVO <",15,colorButtonIdle,colorButtonText,ToggleLoadPrevEvo,None,(0,0),enableButton)
    mainSurface.blit(menuSurface,(0,0))
    if pokeballOffset == 0:
        pygame.display.update((45-25,int(displayHeight/2)-170-25,56,56))
        pygame.display.update((80-28,int(displayHeight/2)-90-28,56,56))
        pygame.display.update((95-30,int(displayHeight/2)-30,60,60))
        pygame.display.update((80-28,int(displayHeight/2)+90-28,56,56))
        pygame.display.update((45-25,int(displayHeight/2)+170-25,56,56))
    else:
        pygame.display.update((0,0,150,480))

def StatSurfaceContent(currentStatPage):

    # Drawin stats-screen
    statsSurface.fill((0,0,0))
    statsSurface.set_colorkey((0,0,0))
    pygame.gfxdraw.aacircle(statsSurface,950,int(displayHeight/2),950,white)
    pygame.gfxdraw.filled_circle(statsSurface,950,int(displayHeight/2),950,white)
    pygame.gfxdraw.aacircle(statsSurface,905,int(displayHeight/2),900,colorStatBackground)
    pygame.gfxdraw.filled_circle(statsSurface,905,int(displayHeight/2),900,colorStatBackground)

    # Selecting Stat Content
    StatScreen.Load(currentStatPage,statsSurface,pokeData,white,(colorAccentColor,genderDifference,colorButtonIdle,colorButtonText,QueueAppearance)) 
    

    mainSurface.blit(statsSurface,(470 + statsOffset,0))
    pygame.display.update((470,0,displayWidth-470,480))

def StatNavigationButtons(surface):
    pygame.draw.rect(mainSurface,colorStatBackground,(470+140-30,450-20,140,40))
    Basic.Button(mainSurface,(140 + 470,450),20,"<",25,colorButtonIdle,colorButtonText,TogglePrevStatPage,None,(0,0))
    Basic.Button(mainSurface,(220 + 470,450),20,">",25,colorButtonIdle,colorButtonText,ToggleNextStatPage,None,(0,0))
    pygame.display.update((470+140-30,450-20,140,40))

#####################################################################################################################
#   TOGGLE FUNCTIONS                                                                                                #
#####################################################################################################################

def ToggleLoadNextDex():
    global loadNewPokemon
    global currentPokemon
    currentPokemon +=1
    if currentPokemon == 803: currentPokemon = 1
    loadNewPokemon = True

def ToggleLoadPrevDex():
    global loadNewPokemon
    global currentPokemon
    currentPokemon -=1
    if currentPokemon == 0: currentPokemon = 802
    loadNewPokemon = True

def ToggleLoadNextEvo():
    global pokeData
    global loadNewPokemon
    global currentPokemon
    currentPokemon = pokeData["nextEvolution"]
    loadNewPokemon = True

def ToggleLoadPrevEvo():
    global pokeData
    global loadNewPokemon
    global currentPokemon
    currentPokemon = pokeData["prevEvolution"]
    loadNewPokemon = True

def ToggleNextStatPage():
    global flipStatPage
    global nextStatPage
    flipStatPage = True
    nextStatPage = True

def TogglePrevStatPage():
    global flipStatPage
    global prevStatPage
    flipStatPage = True
    prevStatPage = True

def ToggleReturnToMainMenu():
    global exitActive
    exitActive = True

def QueueAppearance(spriteType):
    global appearanceQueued
    global appearanceType

    appearanceQueued = True
    appearanceType = spriteType

#####################################################################################################################
#   LOADING LOOP                                                                                                    #
#####################################################################################################################

while not returnToMenu:

    ########################
    # Loading Pokemon-Data #
    ########################

    parameters = (currentPokemon,)
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
    pokeData = c.fetchone()

    ########################
    # Process Pokemon-Data #
    ########################

    # Load Misc Data 
    genderDifference = False

    # Load Colors
    colorStatBackground = (int(pokeData["typeBGColor"].split(',')[0]), int(pokeData["typeBGColor"].split(',')[1]), int(pokeData["typeBGColor"].split(',')[2]))
    colorMenuBarBackground = (int(pokeData["typeAccColor"].split(',')[0]), int(pokeData["typeAccColor"].split(',')[1]), int(pokeData["typeAccColor"].split(',')[2]))
    
    colorButtonIdle = (int(pokeData["typeBtnIdleColor"].split(',')[0]), int(pokeData["typeBtnIdleColor"].split(',')[1]), int(pokeData["typeBtnIdleColor"].split(',')[2]))
    colorButtonText = (int(pokeData["typeBtnHoverColor"].split(',')[0]), int(pokeData["typeBtnHoverColor"].split(',')[1]), int(pokeData["typeBtnHoverColor"].split(',')[2]))
    
    colorAccentColor = (int(pokeData["typeAccColor"].split(',')[0]), int(pokeData["typeAccColor"].split(',')[1]), int(pokeData["typeAccColor"].split(',')[2]))

    # Load Background
    backgroundImage = pygame.image.load("backgrounds/" + pokeData["typeBGImage"]).convert()
    mainSurface.blit(backgroundImage,(0,0))
    

    # Load Spritesheet
    spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/Simplified/" + str(pokeData["nationalDex"]) + "FN.gif")

    ########################
    # One-Time Drawings    #
    ########################

    # Menu and Stat Surfaces
    MenuSurfaceContent(False)
    StatSurfaceContent(currentStatPage)
    StatNavigationButtons(statsSurface)

    # General Data
    Basic.WriteText(mainSurface,(260,15),pokeData["nameEN"],30,"unown.ttf",white,True)
    Basic.WriteText(mainSurface,(260,70),pokeData["nameEN"],50,"PokemonSolid.ttf",colorAccentColor,True)

    if pokeData["hasMultipleForms"] == 1: Basic.WriteText(mainSurface,(280,420),"Forms:",20,"calibrilight.ttf",white,True)
  
    loadNewPokemon = False

    pygame.display.update()
    
#####################################################################################################################
#   DISPLAY LOOP                                                                                                    #
#####################################################################################################################
    while not loadNewPokemon:

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

        # Swipe Processing

        mouseRelLast = mouseRel
        mouseRel = pygame.mouse.get_rel()
        click = pygame.mouse.get_pressed()


        if swipeLock and  click[0] == 0: swipeLock = False

        if not swipeLock and click[0] == 1 and mouseRelLast[0] > swipeSensibility and mouseRel[0] > swipeSensibility: 
            ToggleLoadPrevDex()
            swipeLock = True

        elif not swipeLock and click[0] == 1 and mouseRelLast[0] < -swipeSensibility and mouseRel[0] < -swipeSensibility:
            ToggleLoadNextDex()
            swipeLock = True



        # Animation-Cycle for the Sprite
        if runtimeCounter%2 == 0:
            spriteSurface.fill((0,0,0))
            spriteSurface.set_colorkey((0,0,0))
            spriteFrameIndex,spriteCurrent = SpriteCycle(spriteFrameIndex,spriteTilesAmount,spriteFrames)
            mainSurface.blit(backgroundImage,(0,0))
            spriteSurface.blit(spriteCurrent,sprite)
            mainSurface.blit(spriteSurface,(160,(displayHeight/2)-130))

        # Updating Sprite-Section
        pygame.display.update((160,(displayHeight/2)-130,300,300))

        # Drawing Menu-Screen
        if not exitActive and runtimeCounter%5 == 0:
            MenuSurfaceContent()


        # Toggle Stat Pages
        if flipStatPage:
            # Move out
            if not statsMoveForward: statsOffset += 20
            if statsOffset > 350: 
                statsMoveForward = True
                if nextStatPage: currentStatPage += 1
                if prevStatPage: currentStatPage -= 1

            # Move in
            if statsMoveForward: statsOffset -= 20
            if statsOffset <= 0: 
                statsMoveForward = False
                nextStatPage = False
                prevStatPage = False
                flipStatPage = False

            if currentStatPage > 5: currentStatPage = 0
            if currentStatPage < 0: currentStatPage = 5
            StatSurfaceContent(currentStatPage)
        elif not exitActive: StatNavigationButtons(statsSurface)

        # Exit Routine
        if exitActive:
            if exitStep == 1:
                MenuSurfaceContent(None,exitIteration)
                exitIteration += 3
                if exitIteration > 10:
                    exitIteration = 0
                    exitStep += 1

            if exitStep == 2:
                MenuSurfaceContent(None,-exitIteration)
                exitIteration += 8
                if exitIteration > 100:
                    exitIteration = 0
                    exitStep += 1

            if exitStep == 3:
                pygame.draw.rect(mainSurface,(255,255,255),(displayWidth - exitIteration,0,exitIteration,displayHeight))
                pygame.display.update((displayWidth - exitIteration,0,exitIteration,displayHeight))
                exitIteration += 60
                if exitIteration > (displayWidth+100):
                    exitIteration = 0
                    exitStep += 1
            if exitStep == 4:
                pygame.quit()
                sys.exit()


        runtimeCounter += 1
        if runtimeCounter > 100: runtimeCounter = 0

        clock.tick(60)


