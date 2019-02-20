# Importing Modules
import pygame
import time
import random
import sys

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
1


# Variables
returnToMenu = False
loadNewPokemon = False

statsMoveForward = False

nextStatPage = False

statsOffset = 0
currentStatPage = 0

clockCtr = 0

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
    return (spriteFrame,spriteTiles,cells,playerImg,player)

def SpriteCycle(frame,tilesAmt,cells):
    spriteFrame = frame + 1
    if spriteFrame >= tilesAmt: spriteFrame = 0
    spriteImage = cells[spriteFrame]
    return (spriteFrame,spriteImage)

def QueueAnimationSwitch():
    global toggleQueued
    toggleQueued = True

def Button(surface,pos,radius,text,fontSize,idleColor,hoverColor,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos[0] + radius > mouse[0] > pos[0] - radius and pos[1] + radius > mouse[1] > pos[1] - radius:
        pygame.draw.circle(surface,hoverColor,pos,radius)
        if click[0] == 1 and action != None:
            action()
          
    else:
        pygame.draw.circle(surface,idleColor,pos,radius)

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
        surface.blit(ftImage,(pos[0]-25-30,pos[1]))
        surface.blit(stImage,(pos[0]-25+30,pos[1]))
    else:
        surface.blit(ftImage,(pos[0] - 25,pos[1]))
        
def ProgressBar(surface,pos,width,height,color,text,minValue,maxValue,value):

    displayWidth = int(width/((maxValue-minValue+1)/(value-minValue+1)))-1

    pygame.draw.circle(surface,white,pos,int(height/2))
    pygame.draw.circle(surface,white,(pos[0]+width,pos[1]),int(height/2))
    pygame.draw.rect(surface,white,(pos[0],pos[1]-int(height/2),width,height))

    pygame.draw.circle(surface,color,pos,int(height/2)-3)
    pygame.draw.circle(surface,color,(pos[0]+displayWidth,pos[1]),int(height/2)-3)
    pygame.draw.rect(surface,color,(pos[0],pos[1]-int(height/2)+3,displayWidth,height-6))

    WriteText(surface,(pos[0],pos[1]-30),text,20,"calibrilight.ttf",white)
    WriteText(surface,(pos[0]+width+30,pos[1]),str(value),20,"calibrilight.ttf",white,True)

def LoadStatSet0(surface):
    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),"Kalos",30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#658",50,"PokemonHollow.ttf",white,True)     

    WriteText(surface,(150,100),"Pokédex Data",30,"PokemonSolid.ttf",white,True)  
    
    WriteText(surface,(30,145),"National Dex:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(150,145),"#658",25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,170),"Kalos Dex:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(150,170),"#009",25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,220),"Species:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(110,220),"Ninja Pokémon",25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,290),"Type:",20,"calibrilight.ttf",white,False) 
    WriteText(surface,(150,275),"Water / Dark",20,"calibrilight.ttf",white,True)
    TypeImages(surface,(150,285),"Water","Dark")

    WriteText(surface,(30,360),"Height:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(100,360),"1.5m",25,"calibrilight.ttf",white,False)  

    WriteText(surface,(30,390),"Weight:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(100,390),"40.00kg",25,"calibrilight.ttf",white,False)  

def LoadStatSet1(surface):
    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),"Kalos",30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#658",50,"PokemonHollow.ttf",white,True)     

    WriteText(surface,(150,100),"Pokédex entry",30,"PokemonSolid.ttf",white,True) 
    

    text = "It appears and vanishes with a ninja’s grace. It toys with its enemies using swift movements, while slicing them with throwing stars of sharpest water."
    blit_text(surface, text, (20, 130),pygame.font.Font("calibrilight.ttf",20),(255,255,255))


def LoadStatSet2(surface):
    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),"Kalos",30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#658",50,"PokemonHollow.ttf",white,True)     

    WriteText(surface,(150,100),"Base Stats",30,"PokemonSolid.ttf",white,True)    

    ProgressBar(surface,(50,160),200,18,barMaxWP,"HP",0,150,72)
    ProgressBar(surface,(50,210),200,18,barAttack,"Attack",0,150,95)
    ProgressBar(surface,(50,260),200,18,barDefense,"Defense",0,150,67)
    ProgressBar(surface,(50,310),200,18,barKP,"Sp. Atk",0,150,103)
    ProgressBar(surface,(50,360),200,18,barAttack,"Sp. Def",0,150,71)
    ProgressBar(surface,(50,410),200,18,barMaxWP,"Speed",0,150,122)

def LoadStatSet3(surface):
    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),"Kalos",30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#658",50,"PokemonHollow.ttf",white,True)     

    WriteText(surface,(150,100),"Training",30,"PokemonSolid.ttf",white,True)    

    WriteText(surface,(30,145),"EV Yield:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,145),"3 Speed",25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,185),"Catch Rate:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,185),"45",25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,225),"Base Friendship:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,225),"70",25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,265),"Base Exp.:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,265),"239",25,"calibrilight.ttf",white,False)  

    WriteText(surface,(30,305),"Growth Rate:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,305),"Medium Slow",25,"calibrilight.ttf",white,False)  

def LoadStatSet4(surface):
    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),"Kalos",30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#658",50,"PokemonHollow.ttf",white,True)     

    WriteText(surface,(150,100),"Breeding",30,"PokemonSolid.ttf",white,True)    

    WriteText(surface,(30,145),"Egg Groups:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,145),"Water 1",25,"calibrilight.ttf",white,False)    

    WriteText(surface,(30,185),"Gender:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,185),"87.5% male",25,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,220),"12.5% female",25,"calibrilight.ttf",white,False)    


    WriteText(surface,(30,260),"Egg cycles:",20,"calibrilight.ttf",white,False)    
    WriteText(surface,(170,260),"20",25,"calibrilight.ttf",white,False)  

def LoadStatSet5(surface):
    WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
    WriteText(surface,(40,35),"Kalos",30,"PokemonHollow.ttf",white,False)     
    WriteText(surface,(260,45),"#658",50,"PokemonHollow.ttf",white,True)     

    WriteText(surface,(150,100),"Appearance",30,"PokemonSolid.ttf",white,True)    

    # Gender / Shiny Button and update
    Button(mainSurface,(380,400),20,"M",20,buttonIdleColor,buttonHoverColor)
    Button(mainSurface,(430,400),20,"F",20,buttonIdleColor,buttonHoverColor)

    Button(mainSurface,(380,450),20,"M",20,buttonIdleColor,buttonHoverColor)
    Button(mainSurface,(430,450),20,"F",20,buttonIdleColor,buttonHoverColor)

    pygame.display.update((360,380,40,40))
    pygame.display.update((410,380,40,40))

    pygame.display.update((360,430,40,40))
    pygame.display.update((410,430,40,40))





def ToggleNextStatPage():
    global nextStatPage
    nextStatPage = True

def ToggleReturnToMainMenu():
    global returnToMenu
    global loadNewPokemon
    loadNewPokemon = True
    returnToMenu = True

# Parent Infoscreen Loop
while not returnToMenu:
    
    # Load Pokemon-Data here
    backgroundImage = pygame.image.load("backgrounds/Water.png").convert()

    #Loading Sprites
    spriteFrameIndex,spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("sp30.gif")
    

    mainSurface.blit(backgroundImage,(0,0))
    
    # Drawin menu-screen
    menuSurface.fill((64,64,64))
    menuSurface.set_colorkey((64,64,64))
    
    pygame.draw.circle(menuSurface,menuBarColor,(-200,int(displayHeight/2)),300)
    pygame.draw.circle(menuSurface,(64,64,64),(-210,int(displayHeight/2)),300)
    pokeballImage = pygame.image.load("pokeball.png").convert()
    menuSurface.blit(pokeballImage,(-250,int(displayHeight/2)-150))
    mainSurface.blit(menuSurface,(0,0))

    # Drawin stats-screen
    statsSurface.fill((0,0,0))
    statsSurface.set_colorkey((0,0,0))
    pygame.draw.circle(statsSurface,white,(950,int(displayHeight/2)),950)
    pygame.draw.circle(statsSurface,menuBG,(905,int(displayHeight/2)),900)
    LoadStatSet0(statsSurface)
    mainSurface.blit(statsSurface,(470 + statsOffset,0))


    WriteText(mainSurface,(280,15),"Greninja",30,"unown.ttf",white,True)
    WriteText(mainSurface,(280,70),"Greninja",50,"PokemonSolid.ttf",red,True)

    WriteText(mainSurface,(280,420),"Water / Dark",20,"calibrilight.ttf",white,True)
    TypeImages(mainSurface,(280,430),"Water","Dark")

    pygame.display.update()

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


        # Animation-Cycle for the Sprite
        spriteSurface.fill((0,0,0))
        spriteSurface.set_colorkey((0,0,0))
        spriteFrameIndex,spriteCurrent = SpriteCycle(spriteFrameIndex,spriteTilesAmount,spriteFrames)
        mainSurface.blit(backgroundImage,(0,0))
        spriteSurface.blit(spriteCurrent,sprite)
        mainSurface.blit(spriteSurface,(160,(displayHeight/2)-130))

        
        if clockCtr%5 == 0:
            # Menu Button and update
            Button(menuSurface,(45,int(displayHeight/2)-170),25,"animation",15,buttonIdleColor,buttonHoverColor,QueueAnimationSwitch)
            Button(menuSurface,(80,int(displayHeight/2)-90),28,"next Evo",15,buttonIdleColor,buttonHoverColor)
            Button(menuSurface,(95,int(displayHeight/2)),30,"<",15,buttonIdleColor,buttonHoverColor,ToggleReturnToMainMenu)
            Button(menuSurface,(80,int(displayHeight/2)+90),28,"prev Evo",15,buttonIdleColor,buttonHoverColor)
            Button(menuSurface,(45,int(displayHeight/2)+170),25,"EN / DE",15,buttonIdleColor,buttonHoverColor)
            mainSurface.blit(menuSurface,(0,0))
            pygame.display.update((45-25,int(displayHeight/2)-170-25,56,56))
            pygame.display.update((80-28,int(displayHeight/2)-90-28,56,56))
            pygame.display.update((95-30,int(displayHeight/2)-30,60,60))
            pygame.display.update((80-28,int(displayHeight/2)+90-28,56,56))
            pygame.display.update((45-25,int(displayHeight/2)+170-25,56,56))
            
            
            # Stats Button and update
            Button(mainSurface,(440,40),30,"Stats",15,buttonIdleColor,buttonHoverColor,ToggleNextStatPage)
            pygame.display.update((410,10,60,60))

            
            clockCtr = 0

        

        # Updating Sprite-Section
        pygame.display.update((160,(displayHeight/2)-130,300,300))


        # Drawing stats-screen
        statsSurface.fill((0,0,0))
        statsSurface.set_colorkey((0,0,0))
        pygame.draw.circle(statsSurface,white,(950,int(displayHeight/2)),950)
        pygame.draw.circle(statsSurface,menuBG,(905,int(displayHeight/2)),900)

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
            if currentStatPage > 4: currentStatPage = 0

            mainSurface.blit(statsSurface,(470 + statsOffset,0))
            pygame.display.update((470,0,displayWidth-470,480))

        # Tick
        clock.tick(60)

        clockCtr += 1

for x in range(0,10):
    if x%3 == 0:
        print(x)
        mainSurface.blit(backgroundImage,(0,0))
        menuSurface.fill((64,64,64))
        menuSurface.set_colorkey((64,64,64))
        pygame.draw.circle(menuSurface,menuBarColor,(-200,int(displayHeight/2)),300)
        pygame.draw.circle(menuSurface,(64,64,64),(-210,int(displayHeight/2)),300)

        menuSurface.blit(pokeballImage,(-250 + x,int(displayHeight/2)-150))
        mainSurface.blit(menuSurface,(0,0))
        pygame.display.update((0,0,150,480))
        clock.tick(60)

for x in range(0,100):
    if x%6 == 0:
        mainSurface.blit(backgroundImage,(0,0))
        print(-x + 10)
        menuSurface.fill((64,64,64))
        menuSurface.set_colorkey((64,64,64))
        pygame.draw.circle(menuSurface,menuBarColor,(-200,int(displayHeight/2)),300)
        pygame.draw.circle(menuSurface,(64,64,64),(-210,int(displayHeight/2)),300)

        menuSurface.blit(pokeballImage,(-250 - x + 10,int(displayHeight/2)-150))
        mainSurface.blit(menuSurface,(0,0))
        pygame.display.update((0,0,150,480))
        clock.tick(60)

mainSurface.fill((255,255,255))

for x in range(0,displayWidth):
    if x%60 == 0:
        pygame.display.update((displayWidth - x,0,x,displayHeight))
        clock.tick(60)

pygame.quit()
sys.exit()