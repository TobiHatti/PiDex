# Importing Modules
import pygame
from pygame import gfxdraw
import time
import random
import sys
import sqlite3

# Color Definitions
white = (255,255,255)
black = (0,0,0)
red = (255,10,10)
mainBG = (186, 212, 255)
spriteBG = (173, 204, 255)
statsBG = (155, 193, 255)
menuBG = (137, 182, 255)

barMaxWP = (255, 208, 0)
barAttack = (255, 46, 0)
barDefense = (0, 246, 255)
barKP = (170, 0, 255)

buttonIdleColor = (0, 216, 255)
buttonHoverColor = (0, 140, 255)
menuBarColor = (0, 110, 255)

# PyGame Initialisation
pygame.init()
clock = pygame.time.Clock()
#pygame.mouse.set_visible(False)

# Window and Surface Initialisation
displayWidth = 800
displayHeight = 480

mainSurface = pygame.display.set_mode((displayWidth,displayHeight))
spriteSurface = pygame.Surface((300,300)).convert()
statsSurface = pygame.Surface((displayWidth-470,480)).convert()
menuSurface = pygame.Surface((150,480)).convert()

# DB-Initialisation and Setup
conn = sqlite3.connect('pokemon.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Variables
spriteFrameIndex = 0
attackIndex = 1
attackAmount = 3


returnToMenu = False
loadNewPokemon = False

statsMoveForward = False

nextStatPage = False

statsOffset = 0
currentStatPage = 0

clockCtr = 0

appearanceQueued = False
appearanceType = ""

genderDifference = False

currentPokemon = 1

# Functions

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def SpriteCreate(filePath):

    sheet = pygame.image.load(filePath).convert()
    imgWidth, imgHeight = sheet.get_size()
    spriteTiles = int(imgWidth / 200)
    cells = []
    for n in range(spriteTiles):
        width, height = (200,200)
        rect = pygame.Rect(n * width, 0,width,height)
        image = pygame.Surface(rect.size).convert()
        image.blit(sheet, (0,0),rect)
        alpha = image.get_at((0,0))
        image.set_colorkey(alpha)
        image = pygame.transform.scale(image,(300,300))
        cells.append(image)
    playerImg = cells[0]
    player = playerImg.get_rect()
    player.center = (150,150)
    spriteFrame = 0
    return (spriteTiles,cells,playerImg,player)

def SpriteCycle(frame,tilesAmt,cells):
    spriteFrame = frame + 1
    if spriteFrame >= tilesAmt: spriteFrame = 0
    spriteImage = cells[spriteFrame]
    return (spriteFrame,spriteImage)

def QueueAnimationSwitch():
    global toggleQueued
    toggleQueued = True

def Button(surface,pos,radius,text,fontSize,idleColor,hoverColor,action = None,parameter = None,surfaceOffset = (0,0)):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos[0] + radius + surfaceOffset[0] > mouse[0] > pos[0] - radius + surfaceOffset[0] and pos[1] + radius + surfaceOffset[1] > mouse[1] > pos[1] - radius + surfaceOffset[1]:

        pygame.gfxdraw.aacircle(surface,pos[0]-2,pos[1]-2,radius-4,hoverColor)
        pygame.gfxdraw.filled_circle(surface,pos[0]-2,pos[1]-2,radius-4,hoverColor)
        if click[0] == 1 and action != None:
            if parameter == None: action()
            else: action(parameter)
    else:
        pygame.gfxdraw.aacircle(surface,pos[0]-2,pos[1]-2,radius-4,idleColor)
        pygame.gfxdraw.filled_circle(surface,pos[0]-2,pos[1]-2,radius-4,idleColor)

    WriteText(surface,pos,text,fontSize,"PokemonSolid.ttf",white,True)

def WriteText(surface,pos,text,fontSize,fontFamily,fontColor,centered = False):
    outputText = pygame.font.Font(fontFamily,fontSize)
    textSurf = outputText.render(text,True,fontColor)
    textRect = outputText.render(text,True,fontColor).get_rect()
    if centered:
        textRect.center = (pos[0],pos[1])
    else:
        textRect = (pos[0],pos[1])
    surface.blit(textSurf,textRect)

def TypeImages(surface,pos,firstType, secondType = None):
    if firstType == "Bug": ftImage = pygame.image.load("typesS/Bug.png")
    elif firstType == "Dark": ftImage = pygame.image.load("typesS/Dark.png")
    elif firstType == "Dragon": ftImage = pygame.image.load("typesS/Dragon.png")
    elif firstType == "Electric": ftImage = pygame.image.load("typesS/Electric.png")
    elif firstType == "Fairy": ftImage = pygame.image.load("typesS/Fairy.png")
    elif firstType == "Fighting": ftImage = pygame.image.load("typesS/Fighting.png")
    elif firstType == "Fire": ftImage = pygame.image.load("typesS/Fire.png")
    elif firstType == "Flying": ftImage = pygame.image.load("typesS/Flying.png")
    elif firstType == "Ghost": ftImage = pygame.image.load("typesS/Ghost.png")
    elif firstType == "Grass": ftImage = pygame.image.load("typesS/Grass.png")
    elif firstType == "Ground": ftImage = pygame.image.load("typesS/Ground.png")
    elif firstType == "Ice": ftImage = pygame.image.load("typesS/Ice.png")
    elif firstType == "Normal": ftImage = pygame.image.load("typesS/Normal.png")
    elif firstType == "Poison": ftImage = pygame.image.load("typesS/Poison.png")
    elif firstType == "Psychic": ftImage = pygame.image.load("typesS/Psychic.png")
    elif firstType == "Rock": ftImage = pygame.image.load("typesS/Rock.png")
    elif firstType == "Steel": ftImage = pygame.image.load("typesS/Steel.png")
    elif firstType == "Water": ftImage = pygame.image.load("typesS/Water.png")

    if secondType != None:
        if secondType == "Bug": stImage = pygame.image.load("typesS/Bug.png")
        elif secondType == "Dark": stImage = pygame.image.load("typesS/Dark.png")
        elif secondType == "Dragon": stImage = pygame.image.load("typesS/Dragon.png")
        elif secondType == "Electric": stImage = pygame.image.load("typesS/Electric.png")
        elif secondType == "Fairy": stImage = pygame.image.load("typesS/Fairy.png")
        elif secondType == "Fighting": stImage = pygame.image.load("typesS/Fighting.png")
        elif secondType == "Fire": stImage = pygame.image.load("typesS/Fire.png")
        elif secondType == "Flying": stImage = pygame.image.load("typesS/Flying.png")
        elif secondType == "Ghost": stImage = pygame.image.load("typesS/Ghost.png")
        elif secondType == "Grass": stImage = pygame.image.load("typesS/Grass.png")
        elif secondType == "Ground": stImage = pygame.image.load("typesS/Ground.png")
        elif secondType == "Ice": stImage = pygame.image.load("typesS/Ice.png")
        elif secondType == "Normal": stImage = pygame.image.load("typesS/Normal.png")
        elif secondType == "Poison": stImage = pygame.image.load("typesS/Poison.png")
        elif secondType == "Psychic": stImage = pygame.image.load("typesS/Psychic.png")
        elif secondType == "Rock": stImage = pygame.image.load("typesS/Rock.png")
        elif secondType == "Steel": stImage = pygame.image.load("typesS/Steel.png")
        elif secondType == "Water": stImage = pygame.image.load("typesS/Water.png")
        surface.blit(pygame.image.load("typesS/Water.png"),(pos[0]-25-30,pos[1]))
        surface.blit(pygame.image.load("typesS/Water.png"),(pos[0]-25+30,pos[1]))
    else:
        surface.blit(ftImage,(pos[0] - 25,pos[1]))
        
def ProgressBar(surface,pos,width,height,color,text,minValue,maxValue,value):

    displayWidth = int(width/((maxValue-minValue+1)/(value-minValue+1)))-1

    pygame.gfxdraw.aacircle(surface,pos[0],pos[1],int(height/2),white)
    pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],int(height/2),white)
    pygame.gfxdraw.aacircle(surface,pos[0]+width,pos[1],int(height/2),white)
    pygame.gfxdraw.filled_circle(surface,pos[0]+width,pos[1],int(height/2),white)
    pygame.gfxdraw.box(surface,(pos[0],pos[1]-int(height/2),width,height+1),white)

    pygame.gfxdraw.aacircle(surface,pos[0],pos[1],int(height/2)-3,color)
    pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],int(height/2)-3,color)
    pygame.gfxdraw.aacircle(surface,pos[0]+displayWidth,pos[1],int(height/2)-3,color)
    pygame.gfxdraw.filled_circle(surface,pos[0]+displayWidth,pos[1],int(height/2)-3,color)
    pygame.gfxdraw.box(surface,(pos[0],pos[1]-int(height/2)+3,displayWidth,height+1-6),color)


    WriteText(surface,(pos[0],pos[1]-30),text,20,"calibrilight.ttf",white)
    WriteText(surface,(pos[0]+width+30,pos[1]),str(value),20,"calibrilight.ttf",white,True)

def LoadStatSet0(surface):
    global pokeData

    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",white,True)     

    WriteText(surface,(150,100),"Pokédex Data",30,"PokemonSolid.ttf",white,True)  
    
    WriteText(surface,(30,145),"National Dex:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(150,145),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,170),str(pokeData["regionName"]) + " Dex:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(150,170),"#" + str('{0:03d}'.format(pokeData["kalosDex"])),25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,220),"Species:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(110,220),pokeData["species"],25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,290),"Type:",20,"calibrilight.ttf",white,False) 

    if pokeData["type2NameEN"] == None:
        WriteText(surface,(150,275),pokeData["type1NameEN"],20,"calibrilight.ttf",white,True)
        surface.blit(pygame.image.load("typesS/Water.png"),(150-25,285))
    else:
        WriteText(surface,(150,275),pokeData["type1NameEN"] + " / " + pokeData["type2NameEN"],20,"calibrilight.ttf",white,True)
        surface.blit(pygame.image.load("typesS/Water.png"),(150-25-30,285))
        surface.blit(pygame.image.load("typesS/Water.png"),(150-25+30,285))

    WriteText(surface,(30,360),"Height:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(100,360),str(pokeData["height"]/100) + "m",25,"calibrilight.ttf",white,False)  

    WriteText(surface,(30,390),"Weight:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(100,390),str(pokeData["height"]/1000) + "kg",25,"calibrilight.ttf",white,False)  

def LoadStatSet1(surface):
    global pokeData

    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",white,True)    

    WriteText(surface,(150,100),"Pokédex entry",30,"PokemonSolid.ttf",white,True) 

    blit_text(surface, pokeData["dexInfo"], (20, 130),pygame.font.Font("calibrilight.ttf",20),(255,255,255))

def LoadStatSet2(surface):
    global pokeData

    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",white,True)     

    WriteText(surface,(150,100),"Base Stats",30,"PokemonSolid.ttf",white,True)    

    ProgressBar(surface,(50,160),200,18,barMaxWP,"HP",0,150,pokeData["statHP"])
    ProgressBar(surface,(50,210),200,18,barAttack,"Attack",0,150,pokeData["statAtk"])
    ProgressBar(surface,(50,260),200,18,barDefense,"Defense",0,150,pokeData["statDef"])
    ProgressBar(surface,(50,310),200,18,barKP,"Sp. Atk",0,150,pokeData["statSpAtk"])
    ProgressBar(surface,(50,360),200,18,barAttack,"Sp. Def",0,150,pokeData["statSpDef"])
    ProgressBar(surface,(50,410),200,18,barMaxWP,"Speed",0,150,pokeData["statSpd"])

def LoadStatSet3(surface):
    global pokeData

    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",white,True)    

    WriteText(surface,(150,100),"Training",30,"PokemonSolid.ttf",white,True)    

    WriteText(surface,(30,145),"EV Yield:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,145),str(pokeData["evYieldAmt"]) + " " +  str(pokeData["evYieldTypeEN"]),25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,185),"Catch Rate:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,185),str(pokeData["catchRate"]) + "%",25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,225),"Base Friendship:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,225),str(pokeData["baseFriendship"]),25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,265),"Base Exp.:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,265),str(pokeData["baseExp"]),25,"calibrilight.ttf",white,False)  

    WriteText(surface,(30,305),"Growth Rate:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,305),str(pokeData["growthRateEN"]),25,"calibrilight.ttf",white,False)  

def LoadStatSet4(surface):
    global pokeData

    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",white,True)    

    WriteText(surface,(150,100),"Breeding",30,"PokemonSolid.ttf",white,True)    

    WriteText(surface,(30,145),"Egg Groups:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,145),pokeData["eggGroupNameEN"],25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,185),"Gender:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,185),str(pokeData["genderMale"]) + "% male",25,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,220),str(100-pokeData["genderMale"]) + "% female",25,"calibrilight.ttf",white,False)    


    WriteText(surface,(30,260),"Egg cycles:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,260),str(pokeData["eggCycles"]),25,"calibrilight.ttf",white,False)  

def LoadStatSet5(surface):
    global pokeData

    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",white,True)   

    WriteText(surface,(150,100),"Appearance",30,"PokemonSolid.ttf",white,True)    

    global genderDifference

    # Gender / Shiny Button and update

    if genderDifference:
        WriteText(surface,(165,150),"Male:",25,"calibrilight.ttf",white,True) 
        Button(surface,(100,180),20,"Normal",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"FNM",(470,0))
        Button(surface,(230,180),20,"Shiny",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"FSM",(470,0))

        WriteText(surface,(165,220),"Female:",25,"calibrilight.ttf",white,True) 
        Button(surface,(100,250),20,"Normal",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"FNF",(470,0))
        Button(surface,(230,250),20,"Shiny",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"FSF",(470,0))

        WriteText(surface,(165,300),"Backside:",25,"calibrilight.ttf",white,True) 
        Button(surface,(100,330),20,"Normal",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"BN",(470,0))
        Button(surface,(230,330),20,"Shiny",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"BS",(470,0))
    else:
        WriteText(surface,(165,150),"Frontside:",25,"calibrilight.ttf",white,True) 
        Button(surface,(100,180),20,"Normal",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"FN",(470,0))
        Button(surface,(230,180),20,"Shiny",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"FS",(470,0))

        WriteText(surface,(165,220),"Backside:",25,"calibrilight.ttf",white,True) 
        Button(surface,(100,250),20,"Normal",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"BN",(470,0))
        Button(surface,(230,250),20,"Shiny",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"BS",(470,0))

    WriteText(surface,(165,380),"Attack Animation:",25,"calibrilight.ttf",white,True) 
    Button(surface,(165,410),20,"Toggle",20,buttonIdleColor,buttonHoverColor,QueueAppearance,"ATK",(470,0))



def ToggleNextStatPage():
    global nextStatPage
    nextStatPage = True

def ToggleReturnToMainMenu():
    global returnToMenu
    global loadNewPokemon
    loadNewPokemon = True
    returnToMenu = True

def QueueAppearance(spriteType):
    global appearanceQueued
    global appearanceType

    appearanceQueued = True
    appearanceType = spriteType

def ToggleLoadNextDex():
    global loadNewPokemon
    global currentPokemon
    currentPokemon +=1
    loadNewPokemon = True

def ToggleLoadPrevDex():
    global loadNewPokemon
    global currentPokemon
    currentPokemon -=1
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


# Parent Infoscreen Loop
while not returnToMenu:
    
    # Load Pokemon-Data here

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

    backgroundImage = pygame.image.load("backgrounds/" + pokeData["typeBGImage"]).convert()
    genderDifference = False

    #Loading Sprites
    spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_FN.gif")
    

    mainSurface.blit(backgroundImage,(0,0))
    
    # Drawin menu-screen
    menuSurface.fill((64,64,64))
    menuSurface.set_colorkey((64,64,64))
    
    pygame.gfxdraw.aacircle(menuSurface,-200,int(displayHeight/2),300,menuBarColor)
    pygame.gfxdraw.filled_circle(menuSurface,-200,int(displayHeight/2),300,menuBarColor)
    pygame.gfxdraw.aacircle(menuSurface,-210,int(displayHeight/2),300,(64,64,64))
    pygame.gfxdraw.filled_circle(menuSurface,-210,int(displayHeight/2),300,(64,64,64))

    pokeballImage = pygame.image.load("pokeball.png").convert()
    menuSurface.blit(pokeballImage,(-250,int(displayHeight/2)-150))
    mainSurface.blit(menuSurface,(0,0))

    # Drawin stats-screen
    statsSurface.fill((0,0,0))
    statsSurface.set_colorkey((0,0,0))
    pygame.gfxdraw.aacircle(statsSurface,950,int(displayHeight/2),950,white)
    pygame.gfxdraw.filled_circle(statsSurface,950,int(displayHeight/2),950,white)
    pygame.gfxdraw.aacircle(statsSurface,905,int(displayHeight/2),900,menuBG)
    pygame.gfxdraw.filled_circle(statsSurface,905,int(displayHeight/2),900,menuBG)
    LoadStatSet0(statsSurface)
    mainSurface.blit(statsSurface,(470 + statsOffset,0))


    WriteText(mainSurface,(280,15),pokeData["nameEN"],30,"unown.ttf",white,True)
    WriteText(mainSurface,(280,70),pokeData["nameEN"],50,"PokemonSolid.ttf",red,True)

    if pokeData["type2NameEN"] == None:
        WriteText(mainSurface,(280,420),pokeData["type1NameEN"],20,"calibrilight.ttf",white,True)
        mainSurface.blit(pygame.image.load("typesS/Water.png"),(280-25,430))
    else:
        WriteText(mainSurface,(280,420),pokeData["type1NameEN"] + " / " + pokeData["type2NameEN"],20,"calibrilight.ttf",white,True)
        mainSurface.blit(pygame.image.load("typesS/Water.png"),(280-25-30,430))
        mainSurface.blit(pygame.image.load("typesS/Water.png"),(280-25+30,430))

    pygame.display.update()

    loadNewPokemon = False

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

        # Animation Sprite Appearance Toggle
        if appearanceQueued:
            if genderDifference:
                if appearanceType == "FNM": spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_FNM.gif")
                elif appearanceType == "FNF": spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_FNF.gif")
                elif appearanceType == "FSM": spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_FSM.gif")
                elif appearanceType == "FSF": spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_FSF.gif")
            else:
                if appearanceType == "FN": spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_FN.gif")
                elif appearanceType == "FS": spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_FS.gif")   

            if appearanceType == "BN": spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_BN.gif")
            elif appearanceType == "BS": spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_BS.gif")
            elif appearanceType == "ATK":
                
                spriteFrameIndex = 0
                
                spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("spritesheets/658/658_ATK" + str(attackIndex) + ".gif")
                attackIndex += 1
                if attackIndex > attackAmount: attackIndex = 1
            appearanceQueued = False


        # Animation-Cycle for the Sprite
        spriteSurface.fill((0,0,0))
        spriteSurface.set_colorkey((0,0,0))
        spriteFrameIndex,spriteCurrent = SpriteCycle(spriteFrameIndex,spriteTilesAmount,spriteFrames)
        mainSurface.blit(backgroundImage,(0,0))
        spriteSurface.blit(spriteCurrent,sprite)
        mainSurface.blit(spriteSurface,(160,(displayHeight/2)-130))

        
        if clockCtr%5 == 0:
            # Menu Button and update
            Button(menuSurface,(45,int(displayHeight/2)-170),25,"DEX >",15,buttonIdleColor,buttonHoverColor,ToggleLoadNextDex)
            Button(menuSurface,(80,int(displayHeight/2)-90),28,"DEX <",15,buttonIdleColor,buttonHoverColor,ToggleLoadPrevDex)
            Button(menuSurface,(95,int(displayHeight/2)),30,"BACK",15,buttonIdleColor,buttonHoverColor,ToggleReturnToMainMenu)
            Button(menuSurface,(80,int(displayHeight/2)+90),28,"EVO >",15,buttonIdleColor,buttonHoverColor,ToggleLoadNextEvo)
            Button(menuSurface,(45,int(displayHeight/2)+170),25,"EVO <",15,buttonIdleColor,buttonHoverColor,ToggleLoadPrevEvo)
            mainSurface.blit(menuSurface,(0,0))
            pygame.display.update((45-25,int(displayHeight/2)-170-25,56,56))
            pygame.display.update((80-28,int(displayHeight/2)-90-28,56,56))
            pygame.display.update((95-30,int(displayHeight/2)-30,60,60))
            pygame.display.update((80-28,int(displayHeight/2)+90-28,56,56))
            pygame.display.update((45-25,int(displayHeight/2)+170-25,56,56))
            
            # Stats Button and update
            Button(mainSurface,(440,40),30,"Stats",15,buttonIdleColor,buttonHoverColor,ToggleNextStatPage)
            pygame.display.update((410,10,60,60))
            
            if currentStatPage == 2:
                LoadStatSet5(statsSurface)
                mainSurface.blit(statsSurface,(470 + statsOffset,0))
                pygame.display.update((470,0,displayWidth-470,480))

            clockCtr = 0

        

        # Updating Sprite-Section
        pygame.display.update((160,(displayHeight/2)-130,300,300))


        # Drawing stats-screen
        statsSurface.fill((0,0,0))
        statsSurface.set_colorkey((0,0,0))
        pygame.gfxdraw.aacircle(statsSurface,950,int(displayHeight/2),950,white)
        pygame.gfxdraw.filled_circle(statsSurface,950,int(displayHeight/2),950,white)
        pygame.gfxdraw.aacircle(statsSurface,905,int(displayHeight/2),900,menuBG)
        pygame.gfxdraw.filled_circle(statsSurface,905,int(displayHeight/2),900,menuBG)

        # Change Stat Screen

        if nextStatPage:
            # Move out
            if not statsMoveForward: statsOffset += 20
            if statsOffset > 350: 
                statsMoveForward = True
                currentStatPage += 1

            # Move in
            if statsMoveForward: statsOffset -= 20
            if statsOffset <= 0: 
                statsMoveForward = False
                nextStatPage = False

            # Selecting Stat Content
            if currentStatPage == 0: LoadStatSet0(statsSurface)
            if currentStatPage == 1: LoadStatSet1(statsSurface)
            if currentStatPage == 2: LoadStatSet5(statsSurface)
            if currentStatPage == 3: LoadStatSet2(statsSurface)
            if currentStatPage == 4: LoadStatSet3(statsSurface)
            if currentStatPage == 5: LoadStatSet4(statsSurface)

            # Reset Statpage-Counter
            if currentStatPage > 5: currentStatPage = 0

            mainSurface.blit(statsSurface,(470 + statsOffset,0))
            pygame.display.update((470,0,displayWidth-470,480))

        


        # Tick
        clock.tick(50)

        clockCtr += 1

for x in range(0,10):
    if x%3 == 0:
        mainSurface.blit(backgroundImage,(0,0))
        menuSurface.fill((64,64,64))
        menuSurface.set_colorkey((64,64,64))
        pygame.gfxdraw.aacircle(menuSurface,-200,int(displayHeight/2),300,menuBarColor)
        pygame.gfxdraw.filled_circle(menuSurface,-200,int(displayHeight/2),300,menuBarColor)
        pygame.gfxdraw.aacircle(menuSurface,-210,int(displayHeight/2),300,(64,64,64))
        pygame.gfxdraw.filled_circle(menuSurface,-210,int(displayHeight/2),300,(64,64,64))

        menuSurface.blit(pokeballImage,(-250 + x,int(displayHeight/2)-150))
        mainSurface.blit(menuSurface,(0,0))
        pygame.display.update((0,0,150,480))
        clock.tick(60)

for x in range(0,100):
    if x%6 == 0:
        mainSurface.blit(backgroundImage,(0,0))
        menuSurface.fill((64,64,64))
        menuSurface.set_colorkey((64,64,64))
        pygame.gfxdraw.aacircle(menuSurface,-200,int(displayHeight/2),300,menuBarColor)
        pygame.gfxdraw.filled_circle(menuSurface,-200,int(displayHeight/2),300,menuBarColor)
        pygame.gfxdraw.aacircle(menuSurface,-210,int(displayHeight/2),300,(64,64,64))
        pygame.gfxdraw.filled_circle(menuSurface,-210,int(displayHeight/2),300,(64,64,64))

        menuSurface.blit(pokeballImage,(-250 - x + 10,int(displayHeight/2)-150))
        mainSurface.blit(menuSurface,(0,0))
        pygame.display.update((0,0,150,480))
        clock.tick(60)

mainSurface.fill((255,255,255))

for x in range(0,displayWidth+100):
    if x%60 == 0:
        pygame.display.update((displayWidth - x,0,x,displayHeight))
        clock.tick(60)

pygame.quit()
sys.exit()