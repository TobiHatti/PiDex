# Importing Modules
import pygame
import time
import random
import sys

# importing custom modules
#import customColors
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

btnctr = 999
ctr = 999

# Initialising PyGame
pygame.init()

# Initialising Clock
clock = pygame.time.Clock()

# Window Initialisation
displayWidth = 800
displayHeight = 480

mainSurface = pygame.display.set_mode((displayWidth,displayHeight))

# Surface declaration and initialisation
spriteSurface = pygame.Surface((300,300)).convert()
statsSurface = pygame.Surface((displayWidth-470,480)).convert()
menuSurface = pygame.Surface((150,480)).convert()


backgroundImage = pygame.image.load("backgrounds/Water.png").convert()


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

def Button(surface,pos,radius,text,idleColor,hoverColor,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if pos[0] + radius > mouse[0] > pos[0] - 50 and pos[1] + radius > mouse[1] > pos[1] - radius:
        pygame.draw.circle(surface,hoverColor,pos,radius)
        if click[0] == 1 and action != None:
            action()
          
    else:
        pygame.draw.circle(surface,idleColor,pos,radius)

    WriteText(surface,pos,text,20,"PokemonSolid.ttf",black,True)


def WriteText(surface,pos,text,fontSize,fontFamily,fontColor,centered = False):
    outputText = pygame.font.Font(fontFamily,fontSize)
    textSurf = outputText.render(text,True,fontColor)
    textRect = outputText.render(text,True,fontColor).get_rect()
    if centered:
        textRect.center = (pos[0],pos[1])
    else:
        textRect = (pos[0],pos[1])
    surface.blit(textSurf,textRect)

def TypeImages(firstType, secondType = None):
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
        mainSurface.blit(ftImage,(280-25-30,420))
        mainSurface.blit(stImage,(280-25+30,420))
    else:
        mainSurface.blit(ftImage,(280 - 25,420))
        
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



# Loading Spritesheet
spriteFrameIndex,spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate("sp30.gif")
spriteIdx = 0
toggleQueued = False
animations = ("sp30.gif","sp31.gif","sp32.gif","sp33.gif")





# One-Time Drawing Routines


mainSurface.fill(mainBG)

statsSurface.fill(mainBG)
menuSurface.fill(mainBG)

mainSurface.set_colorkey(mainBG)

statsSurface.set_colorkey(mainBG)
menuSurface.set_colorkey(mainBG)

pygame.draw.circle(menuSurface,white,(-200,int(displayHeight/2)),300)
pygame.draw.circle(menuSurface,menuBG,(-210,int(displayHeight/2)),300)

pygame.draw.circle(statsSurface,white,(950,int(displayHeight/2)),950)
pygame.draw.circle(statsSurface,menuBG,(905,int(displayHeight/2)),900)


# Stat Surface
WriteText(statsSurface,(40,5),"Region:",20,"PokemonSolid.ttf",white,False)     
WriteText(statsSurface,(40,35),"Kalos",30,"PokemonHollow.ttf",white,False)     
WriteText(statsSurface,(260,45),"#658",50,"PokemonHollow.ttf",white,True)     

ProgressBar(statsSurface,(50,120),200,18,barMaxWP,"HP",0,150,72)
ProgressBar(statsSurface,(50,170),200,18,barAttack,"Attack",0,150,95)
ProgressBar(statsSurface,(50,220),200,18,barDefense,"Defense",0,150,67)
ProgressBar(statsSurface,(50,270),200,18,barKP,"Sp. Atk",0,150,103)
ProgressBar(statsSurface,(50,320),200,18,barAttack,"Sp. Def",0,150,71)
ProgressBar(statsSurface,(50,370),200,18,barMaxWP,"Speed",0,150,122)


spriteSurface.set_colorkey(mainBG)

# Start of Game-Loop


while True:

    # New animation queue
    if toggleQueued and spriteFrameIndex == 0:
        spriteIdx += 1
        if spriteIdx > 3: spriteIdx = 0
        spriteFrameIndex,spriteTilesAmount,spriteFrames,spriteCurrent,sprite = SpriteCreate(animations[spriteIdx])
        toggleQueued = False


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


    # Image Processing
    spriteFrameIndex,spriteCurrent = SpriteCycle(spriteFrameIndex,spriteTilesAmount,spriteFrames)


    # Re-Drawing screen
    
    spriteSurface.fill(mainBG)
    mainSurface.blit(backgroundImage,(0,0))
    
    spriteSurface.blit(spriteCurrent,sprite)


    if btnctr > 10:
        Button(menuSurface,(45,int(displayHeight/2)-170),25,"animation",buttonIdleColor,buttonHoverColor,QueueAnimationSwitch)
        Button(menuSurface,(80,int(displayHeight/2)-90),28,"next Evo",buttonIdleColor,buttonHoverColor)
        Button(menuSurface,(95,int(displayHeight/2)),30,"<",buttonIdleColor,buttonHoverColor)
        Button(menuSurface,(80,int(displayHeight/2)+90),28,"prev Evo",buttonIdleColor,buttonHoverColor)
        Button(menuSurface,(45,int(displayHeight/2)+170),25,"EN / DE",buttonIdleColor,buttonHoverColor)
        btnctr = 0
    

    
    # Main Surface Infos
    WriteText(mainSurface,(280,15),"Greninja",30,"unown.ttf",white,True)
    WriteText(mainSurface,(280,70),"Greninja",50,"PokemonSolid.ttf",red,True)
    WriteText(mainSurface,(280,400),"Water / Dark",25,"calibrilight.ttf",white,True)
   
    
    TypeImages("Water","Dark")

    mainSurface.blit(statsSurface,(470,0))

    mainSurface.blit(spriteSurface,(160,(displayHeight/2)-150))
    
    mainSurface.blit(menuSurface,(0,0))



    # Updating
    if ctr > 200:
        pygame.display.update()
        ctr = 0


    pygame.display.update((160,(displayHeight/2)-150,300,300))

    # Tick
    clock.tick(60)
    ctr += 1
    btnctr += 1


