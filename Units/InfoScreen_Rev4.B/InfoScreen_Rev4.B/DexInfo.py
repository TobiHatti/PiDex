# Importing Modules
import pygame
from pygame import gfxdraw
import time
import random
import sys
import sqlite3
import os

from basics import Basic




class DexInfo:

    class Button:

        def RoundRect(surface,idleColor,hoverColor,textColor,rect,radius,text,fontsize,fontfamily,borderWidth=None,borderColor=(0,0,0)):
            if borderWidth != None:  DexInfo.RoundRect(surface,borderColor,(rect[0]-borderWidth,rect[1]-borderWidth,rect[2]+2*borderWidth,rect[3]+2*borderWidth),radius+borderWidth)

            mouse = pygame.mouse.get_pos()

            if rect[0] < mouse[0] < rect[0]+rect[2] and rect[1] < mouse[1] < rect[1]+rect[3]:
                pygame.draw.circle(surface,idleColor,(rect[0]+radius,rect[1]+radius),radius)    
                pygame.draw.circle(surface,idleColor,(rect[0]-radius + rect[2],rect[1]+radius),radius)
                pygame.draw.circle(surface,idleColor,(rect[0]+radius,rect[1]-radius + rect[3]),radius)
                pygame.draw.circle(surface,idleColor,(rect[0]-radius + rect[2],rect[1]-radius + rect[3]),radius)

                pygame.draw.rect(surface,idleColor,(rect[0] + radius, rect[1], rect[2] - 2*radius, rect[3]))
                pygame.draw.rect(surface,idleColor,(rect[0], rect[1] + radius, rect[2], rect[3] - 2*radius))
            else: 
                pygame.draw.circle(surface,hoverColor,(rect[0]+radius,rect[1]+radius),radius)    
                pygame.draw.circle(surface,hoverColor,(rect[0]-radius + rect[2],rect[1]+radius),radius)
                pygame.draw.circle(surface,hoverColor,(rect[0]+radius,rect[1]-radius + rect[3]),radius)
                pygame.draw.circle(surface,hoverColor,(rect[0]-radius + rect[2],rect[1]-radius + rect[3]),radius)

                pygame.draw.rect(surface,hoverColor,(rect[0] + radius, rect[1], rect[2] - 2*radius, rect[3]))
                pygame.draw.rect(surface,hoverColor,(rect[0], rect[1] + radius, rect[2], rect[3] - 2*radius))

            Basic.WriteText(surface,(rect[0]+int(rect[2]/2),rect[1]+int(rect[3]/2)),text,fontsize,fontfamily,textColor,True)

    currentPokemon = 1

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

    def RoundRect(surface,color,rect,radius,borderWidth=None,borderColor=(0,0,0),titlebar = None):

        if borderWidth != None:  DexInfo.RoundRect(surface,borderColor,(rect[0]-borderWidth,rect[1]-borderWidth,rect[2]+2*borderWidth,rect[3]+2*borderWidth),radius+borderWidth)

        pygame.draw.circle(surface,color,(rect[0]+radius,rect[1]+radius),radius)    
        pygame.draw.circle(surface,color,(rect[0]-radius + rect[2],rect[1]+radius),radius)
        pygame.draw.circle(surface,color,(rect[0]+radius,rect[1]-radius + rect[3]),radius)
        pygame.draw.circle(surface,color,(rect[0]-radius + rect[2],rect[1]-radius + rect[3]),radius)

        pygame.draw.rect(surface,color,(rect[0] + radius, rect[1], rect[2] - 2*radius, rect[3]))
        pygame.draw.rect(surface,color,(rect[0], rect[1] + radius, rect[2], rect[3] - 2*radius))

        if titlebar != None:
            pygame.draw.circle(surface,borderColor,(rect[0]+radius,rect[1]+radius),radius)
            pygame.draw.circle(surface,borderColor,(rect[0]+rect[2]-radius,rect[1]+radius),radius)
            pygame.draw.rect(surface,borderColor,(rect[0]+radius,rect[1],rect[2]-2*radius,radius))
            pygame.draw.rect(surface,color,(rect[0],rect[1]+radius,rect[2],radius))
            pygame.draw.rect(surface,borderColor,(rect[0],rect[1]+radius,rect[2],10))
            Basic.WriteText(surface,(rect[0]+(rect[2]/2),rect[1]+14),titlebar,20,"joy.otf",(255,255,255),True)
        
    def TypeSign1(surface,pos,color,text):
        pygame.draw.polygon(surface,color,((pos[0],pos[1]),(pos[0]+145,pos[1]),(pos[0]+115,pos[1]+35),(pos[0],pos[1]+35)))
        Basic.WriteText(surface,(pos[0]+70,pos[1]+18),text,20,"joy.otf",(255,255,255),True)

    def TypeSign2(surface,pos,color,text):
        pygame.draw.polygon(surface,color,((pos[0]+30,pos[1]),(pos[0]+145,pos[1]),(pos[0]+145,pos[1]+35),(pos[0],pos[1]+35)))
        Basic.WriteText(surface,(pos[0]+75,pos[1]+18),text,20,"joy.otf",(255,255,255),True)

    def TypeSignSingle(surface,pos,color,text):
        pygame.draw.polygon(surface,color,((pos[0],pos[1]),(pos[0]+220,pos[1]),(pos[0]+190,pos[1]+35),(pos[0],pos[1]+35)))
        pygame.draw.polygon(surface,color,((pos[0]+30+200,pos[1]),(pos[0]+200+70,pos[1]),(pos[0]+200+70,pos[1]+35),(pos[0]+200,pos[1]+35)))
        Basic.WriteText(surface,(pos[0]+75,pos[1]+18),text,20,"joy.otf",(255,255,255),True)

    def Pokeball(surface,pos,color,backcolor):

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],32,color)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],32,color)

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],29,backcolor)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],29,backcolor)

        #pygame.draw.circle(surface,color,pos,32)
        #pygame.draw.circle(surface,backcolor,pos,29)
        pygame.draw.rect(surface,color,(pos[0]-30,pos[1]-1,31*2,3))
        pygame.draw.circle(surface,color,pos,12)
        pygame.draw.circle(surface,backcolor,pos,10)
        pygame.draw.circle(surface,color,pos,5)


    def Show(selectedPokemon):
        # PyGame Initialisation
        pygame.init()
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


        spriteSurface = pygame.Surface((300,300)).convert()

        runtimeCtr = 0

        spriteFrameIndex = 0
        screenDistortOffsetHor1 = 0
        screenDistortOffsetHor2 = -200


        spriteTilesAmount,spriteFrames,spriteCurrent,sprite = DexInfo.SpriteCreate("spritesheets/Simplified/" + str(133) + "FN.gif")











        while True:

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


            mainSurface.fill((30,30,30))

            pygame.draw.rect(mainSurface,(60,60,60),(0,screenDistortOffsetHor1,800,30))
            screenDistortOffsetHor1 += 2
            if screenDistortOffsetHor1 > 520: screenDistortOffsetHor1 = -30

            pygame.draw.rect(mainSurface,(60,60,60),(0,screenDistortOffsetHor2,800,30))
            screenDistortOffsetHor2 += 5
            if screenDistortOffsetHor2 > 800: screenDistortOffsetHor2 = -60
            

            
            DexInfo.RoundRect(mainSurface,(40,40,40),(520,10,270,130),15,2,(255,0,255),"Stats")
            DexInfo.RoundRect(mainSurface,(40,40,40),(520,200,270,80),15,2,(255,0,255),"Evolution Chain")
            DexInfo.RoundRect(mainSurface,(40,40,40),(520,290,270,80),15,2,(255,0,255),"Gender Ratio")
            DexInfo.RoundRect(mainSurface,(40,40,40),(10,360,300,110),15,2,(255,0,255))
            DexInfo.RoundRect(mainSurface,(255,0,255),(10,300,400,115),15,2,(255,0,255))
            DexInfo.RoundRect(mainSurface,(40,40,40),(10,10,500,360),26,2,(255,0,255))
            DexInfo.RoundRect(mainSurface,(40,40,40),(20,374,110,39),10)
            DexInfo.Pokeball(mainSurface,(40,40),(255,0,255),(40,40,40))

            DexInfo.Button.RoundRect(mainSurface,(255,0,255),(150,0,150),(255,255,255),(320,430,100,30),10,"Prev Dex",15,"joy.otf",2,(255,255,255))
            DexInfo.Button.RoundRect(mainSurface,(255,0,255),(150,0,150),(255,255,255),(440,430,100,30),10,"Prev Evo",15,"joy.otf",2,(255,255,255))
            DexInfo.Button.RoundRect(mainSurface,(255,0,255),(150,0,150),(255,255,255),(560,430,100,30),10,"Next Evo",15,"joy.otf",2,(255,255,255))
            DexInfo.Button.RoundRect(mainSurface,(255,0,255),(150,0,150),(255,255,255),(680,430,100,30),10,"Next Dex",15,"joy.otf",2,(255,255,255))


            Basic.WriteText(mainSurface,(28,376),"#133",35,"joy.otf",(255,255,255))
            Basic.WriteText(mainSurface,(138,376),"Evolie",35,"joy.otf",(255,255,255))
            Basic.WriteText(mainSurface,(20,425),"Species:",20,"calibrilight.ttf",(255,255,255))
            Basic.WriteText(mainSurface,(20,445),"Region:",20,"calibrilight.ttf",(255,255,255))

            Basic.WriteText(mainSurface,(90,425),"Evolution Pokémon",20,"calibrilight.ttf",(255,255,255))
            Basic.WriteText(mainSurface,(90,445),"Kantho",20,"calibrilight.ttf",(255,255,255))

            pygame.draw.rect(mainSurface,(255,0,255),(420,383,12,12))
            pygame.draw.rect(mainSurface,(255,0,255),(436,383,24,12))
            pygame.draw.rect(mainSurface,(255,0,255),(464,383,45,12))
            Basic.WriteText(mainSurface,(425,396),"T  Y  P  E  :",18,"joy.otf",(255,0,255))


            DexInfo.TypeSign1(mainSurface,(520,380),(150,0,150),"Type 1")
            DexInfo.TypeSign2(mainSurface,(645,380),(255,0,255),"Type 2")

            #DexInfo.TypeSignSingle(mainSurface,(520,380),(150,0,150),"Normal")


            # Animation-Cycle for the Sprite
            if runtimeCtr % 1 == 0: spriteFrameIndex,spriteCurrent = DexInfo.SpriteCycle(spriteFrameIndex,spriteTilesAmount,spriteFrames)
            spriteSurface.fill((0,0,0))
            spriteSurface.set_colorkey((0,0,0))
            spriteSurface.blit(spriteCurrent,sprite)
            mainSurface.blit(spriteSurface,(100,60))

            pygame.display.update()

            clock.tick(60)
            print(clock.tick(60))

            runtimeCtr += 1
            if runtimeCtr > 10000: runtimeCtr = 1


        return  DexInfo.currentPokemon