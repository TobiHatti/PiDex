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
import math

from CButton import Button
from SpriteManager import Sprite
from CDrawing import Draw
from CText import Text

import CText

from DexMenu import DexMenu 


class DexHome:

#########################################################################################
#   PROTECTED VARIABLES                                                                 #
#########################################################################################

    conn = sqlite3.connect('pokemon.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    thread = Thread()
    sleepThread = Thread()

    running = True
    reload = True
    selectionMade = False
    selectedOption = None

    selectedScreen = 1

#########################################################################################
#   FUNCTIONS                                                                           #
#########################################################################################


#########################################################################################
#   TOGGLE FUNCTIONS                                                                    #
#########################################################################################



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


#########################################################################################
#   VARIABLE DEFINITIONS                                                                #
#########################################################################################
           
        fadeOutCtr = 0


        borderWidth = 3

        borderColor = (255,0,0)
        infillColor = (40,40,40)
        fontColor = (255,255,255)

        backColor = (30,30,30)

        radius = 15

        sectionPadding = 10

        borderCorrection = 1

        fontSize = 35

        centerRadius = 130
 
        repressCooldown = 0

#########################################################################################
#   LOADING LOOP                                                                        #
#########################################################################################

        while DexHome.running:

            DexHome.reload = False

#########################################################################################
#   RUNNING LOOP                                                                        #
#########################################################################################

            while not DexHome.reload:

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

                
                
                mainSurface.fill((30,30,30))

#########################################################################################
#   HOME SCREEN 1                                                                       #
#########################################################################################               
                
                if DexHome.selectedScreen == 1:

                    boxOffset1 = 300
                    boxOffset2 = 360
                    boxOffset3 = 420
                    boxOffset4 = -420
                    boxOffset5 = -360
                    boxOffset6 = -300

                    boxWidth = int(266.66 - 2*10)
                    boxHeight = 240-2*10

                    btnColorCenter = infillColor
                    btnColorTopLeft = infillColor
                    btnColorTopRight = infillColor
                    btnColorBottomLeft = infillColor
                    btnColorBottomRight = infillColor

                    btnFontCenter = fontColor
                    btnFontTopLeft = fontColor
                    btnFontTopRight = fontColor
                    btnFontBottomLeft = fontColor
                    btnFontBottomRight = fontColor


                    if repressCooldown <= 0 and not DexHome.selectionMade:

                        # Button functionality
                        if 400-centerRadius < mouse[0] < 400+centerRadius and 240-centerRadius < mouse[1] < 240+centerRadius: 
                            btnColorCenter = (255,255,255)
                            btnFontCenter = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 1
                
                        if (0 < mouse[0] < 400 and 0 < mouse[1] < 240-centerRadius) or (0 < mouse[0] < 400-centerRadius and 0 < mouse[1] < 240): 
                            btnColorTopLeft = (255,255,255)
                            btnFontTopLeft = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 2

                        if (400 < mouse[0] < 800 and 0 < mouse[1] < 240-centerRadius) or (400+centerRadius < mouse[0] < 800 and 0 < mouse[1] < 240): 
                            btnColorTopRight = (255,255,255)
                            btnFontTopRight = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 3

                        if (0 < mouse[0] < 400 and 240+centerRadius < mouse[1] < 480) or (0 < mouse[0] < 400-centerRadius and 240 < mouse[1] < 480): 
                            btnColorBottomLeft = (255,255,255)
                            btnFontBottomLeft = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 4

                        if (400 < mouse[0] < 800 and 240+centerRadius < mouse[1] < 480) or (400+centerRadius < mouse[0] < 800 and 240 < mouse[1] < 480): 
                            btnColorBottomRight = (255,255,255)
                            btnFontBottomRight = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 5





                    # Top Left Segment
                    # Edge Circles
                    Draw.AAFilledCircle(mainSurface,sectionPadding+radius,sectionPadding+radius,radius,btnColorTopLeft,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,400-sectionPadding-radius,sectionPadding+radius,radius,btnColorTopLeft,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,sectionPadding+radius,240-sectionPadding-radius,radius,btnColorTopLeft,borderColor,borderWidth)

                    # Outer Connections
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+radius,sectionPadding+borderCorrection),(400-sectionPadding-radius,sectionPadding+borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+borderCorrection,sectionPadding+radius),(sectionPadding+borderCorrection,240-sectionPadding-radius),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+radius,240-sectionPadding-borderCorrection),(800-sectionPadding-radius,240-sectionPadding-borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(400-sectionPadding-borderCorrection,sectionPadding+radius+borderCorrection),(400-sectionPadding-borderCorrection,480-sectionPadding-radius),borderWidth)
                
                    # Infills
                    pygame.draw.rect(mainSurface,btnColorTopLeft,(sectionPadding+borderWidth,sectionPadding+radius,400-2*sectionPadding-2*borderWidth+borderCorrection,240-4*sectionPadding-2*borderWidth))
                    pygame.draw.rect(mainSurface,btnColorTopLeft,(sectionPadding+radius,sectionPadding+borderWidth,400-radius-2*sectionPadding-4*borderWidth+borderCorrection,240-2*sectionPadding-2*borderWidth+borderCorrection))

                    # Top Right Segment
                    # Edge Circles
                    Draw.AAFilledCircle(mainSurface,400+sectionPadding+radius,sectionPadding+radius,radius,btnColorTopRight,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,800-sectionPadding-radius,sectionPadding+radius,radius,btnColorTopRight,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,800-sectionPadding-radius,240-sectionPadding-radius,radius,btnColorTopRight,borderColor,borderWidth)
                
                    # Outer Connections
                    pygame.draw.line(mainSurface,borderColor,(400+sectionPadding+radius,sectionPadding+borderCorrection),(800-sectionPadding-radius,sectionPadding+borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+borderCorrection,240+sectionPadding+radius),(sectionPadding+borderCorrection,480-sectionPadding-radius),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(400+sectionPadding+borderCorrection,sectionPadding+radius+borderCorrection),(400+sectionPadding+borderCorrection,480-sectionPadding-radius),borderWidth)

                    # Infills
                    pygame.draw.rect(mainSurface,btnColorTopRight,(400+sectionPadding+borderWidth,sectionPadding+radius,400-2*sectionPadding-2*borderWidth+borderCorrection,240-4*sectionPadding-2*borderWidth))
                    pygame.draw.rect(mainSurface,btnColorTopRight,(400+sectionPadding+radius,sectionPadding+borderWidth,400-radius-2*sectionPadding-4*borderWidth+borderCorrection,240-2*sectionPadding-2*borderWidth+borderCorrection))


                    # Bottom Left Segment
                    # Edge Circles
                    Draw.AAFilledCircle(mainSurface,sectionPadding+radius,240+sectionPadding+radius,radius,btnColorBottomLeft,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,400-sectionPadding-radius,480-sectionPadding-radius,radius,btnColorBottomLeft,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,sectionPadding+radius,480-sectionPadding-radius,radius,btnColorBottomLeft,borderColor,borderWidth)
                
                    # Outer Connections
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+radius,480-sectionPadding-borderCorrection),(400-sectionPadding-radius,480-sectionPadding-borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(800-sectionPadding-borderCorrection,sectionPadding+radius),(800-sectionPadding-borderCorrection,240-sectionPadding-radius),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(sectionPadding+radius,240+sectionPadding+borderCorrection),(800-sectionPadding-radius,240+sectionPadding+borderCorrection),borderWidth)

                    # Infills
                    pygame.draw.rect(mainSurface,btnColorBottomLeft,(sectionPadding+borderWidth,240+sectionPadding+radius,400-2*sectionPadding-2*borderWidth+borderCorrection,240-4*sectionPadding-2*borderWidth))
                    pygame.draw.rect(mainSurface,btnColorBottomLeft,(sectionPadding+radius,240+sectionPadding+borderWidth,400-radius-2*sectionPadding-4*borderWidth+borderCorrection,240-2*sectionPadding-2*borderWidth+borderCorrection))

                    # Bottom Right Segment
                    # Edge Circles
                    Draw.AAFilledCircle(mainSurface,400+sectionPadding+radius,480-sectionPadding-radius,radius,btnColorBottomRight,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,800-sectionPadding-radius,480-sectionPadding-radius,radius,btnColorBottomRight,borderColor,borderWidth)
                    Draw.AAFilledCircle(mainSurface,800-sectionPadding-radius,240+sectionPadding+radius,radius,btnColorBottomRight,borderColor,borderWidth)

                    # Outer Connections
                    pygame.draw.line(mainSurface,borderColor,(400+sectionPadding+radius,480-sectionPadding-borderCorrection),(800-sectionPadding-radius,480-sectionPadding-borderCorrection),borderWidth)
                    pygame.draw.line(mainSurface,borderColor,(800-sectionPadding-borderCorrection,240+sectionPadding+radius),(800-sectionPadding-borderCorrection,480-sectionPadding-radius),borderWidth)

                    # Infills
                    pygame.draw.rect(mainSurface,btnColorBottomRight,(400+sectionPadding+borderWidth,240+sectionPadding+radius,400-2*sectionPadding-2*borderWidth+borderCorrection,240-4*sectionPadding-2*borderWidth))
                    pygame.draw.rect(mainSurface,btnColorBottomRight,(400+sectionPadding+radius,240+sectionPadding+borderWidth,400-radius-2*sectionPadding-4*borderWidth+borderCorrection,240-2*sectionPadding-2*borderWidth+borderCorrection))

                    # Outer Segments Large Radius
                    Draw.AAFilledCircle(mainSurface,400,240,centerRadius+2*sectionPadding,backColor,borderColor,borderWidth)
                    pygame.draw.rect(mainSurface,backColor,(400-sectionPadding+borderCorrection,0,2*sectionPadding-borderCorrection,480))
                    pygame.draw.rect(mainSurface,backColor,(0,240-sectionPadding+borderCorrection,800,2*sectionPadding-borderCorrection))

                    # Center segment
                    Draw.AAFilledCircle(mainSurface,400,240,centerRadius,btnColorCenter,borderColor,borderWidth)


                    # Text Segments

                    # (Main) Pokedex
                    # (Main) Fight Simulation
                    # (Main) Type Calculator
                    # (Main) Move Sets
                    # (Main) More
                    # (More) Candy Calculator
                    # (More) Trainercard
                    # (More) Settings
                    # (More) Update
                

                    Text.Write(mainSurface,(400,240),"Pokedex",fontSize,"joy.otf",btnFontCenter,True)

                    Text.Write(mainSurface,(170,80),"Type",fontSize,"joy.otf",btnFontTopLeft,True)
                    Text.Write(mainSurface,(170,120),"Calculator",fontSize,"joy.otf",btnFontTopLeft,True)

                    Text.Write(mainSurface,(630,80),"Move",fontSize,"joy.otf",btnFontTopRight,True)
                    Text.Write(mainSurface,(630,120),"Sets",fontSize,"joy.otf",btnFontTopRight,True)

                    Text.Write(mainSurface,(170,350),"Fight",fontSize,"joy.otf",btnFontBottomLeft,True)
                    Text.Write(mainSurface,(170,390),"Simulation",fontSize,"joy.otf",btnFontBottomLeft,True)

                    Text.Write(mainSurface,(630,370),"More",fontSize,"joy.otf",btnFontBottomRight,True)

                    # Fade-Out and Selection-Trigger
                    if DexHome.selectionMade:
                        if fadeOutCtr <= 3:
                            sectionPadding -= 1
                            centerRadius += 1
                        if fadeOutCtr > 3:
                            sectionPadding += 1
                            if centerRadius >= 2: centerRadius -= 3
                            if fontSize > 0: fontSize -= 1
                        if fadeOutCtr > 10:
                            fadeOutColor = (30,30,30)
                            Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 25: 

                            sectionPadding = 10
                            fontSize = 35
                            centerRadius = 130
                            fadeOutCtr = 0
                            DexHome.selectionMade=False

                            if DexHome.selectedOption == 1: DexMenu.Show()
                            if DexHome.selectedOption == 2: pass
                            if DexHome.selectedOption == 3: pass
                            if DexHome.selectedOption == 4: pass
                            if DexHome.selectedOption == 5: DexHome.selectedScreen = 2

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

#########################################################################################
#   HOME SCREEN 2                                                                       #
#########################################################################################

                

                if DexHome.selectedScreen == 2:

                    btnColorMore1 = infillColor
                    btnColorMore2 = infillColor
                    btnColorMore3 = infillColor
                    btnColorMore4 = infillColor
                    btnColorMore5 = infillColor
                    btnColorMore6 = infillColor

                    btnFontMore1 = fontColor
                    btnFontMore2 = fontColor
                    btnFontMore3 = fontColor
                    btnFontMore4 = fontColor
                    btnFontMore5 = fontColor
                    btnFontMore6 = fontColor
                    

                    while boxOffset1 > 0 or boxOffset2 > 0 or boxOffset3 > 0 or boxOffset4 > 0 or boxOffset5 > 0 or boxOffset6 > 0:

                        mainSurface.fill((30,30,30))

                        Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10-boxOffset1,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10-boxOffset2,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10-boxOffset3,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight-boxOffset4,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight-boxOffset5,boxWidth,boxHeight),radius,borderWidth,borderColor)
                        Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight-boxOffset6,boxWidth,boxHeight),radius,borderWidth,borderColor)

                        if boxOffset1 > 0: boxOffset1 -= 20
                        if boxOffset2 > 0: boxOffset2 -= 20
                        if boxOffset3 > 0: boxOffset3 -= 20
                        if boxOffset4 < 0: boxOffset4 += 20
                        if boxOffset5 < 0: boxOffset5 += 20
                        if boxOffset6 < 0: boxOffset6 += 20

                        pygame.display.update()
                        clock.tick(60)

                    if repressCooldown <= 0:
                        if 0 < mouse[0] < 266 and 0 < mouse[1] < 240: 
                            btnColorMore1 = (255,255,255)
                            btnFontMore1 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 6

                        elif 266 < mouse[0] < 533 and 0 < mouse[1] < 240: 
                            btnColorMore2 = (255,255,255)
                            btnFontMore2 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 7

                        elif 533 < mouse[0] < 800 and 0 < mouse[1] < 240: 
                            btnColorMore3 = (255,255,255)
                            btnFontMore3 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 8

                        elif 0 < mouse[0] < 266 and 240 < mouse[1] < 480: 
                            btnColorMore4 = (255,255,255)
                            btnFontMore4 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 9

                        elif 266 < mouse[0] < 533 and 240 < mouse[1] < 480: 
                            btnColorMore5 = (255,255,255)
                            btnFontMore5 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 10

                        elif 533 < mouse[0] < 800 and 240 < mouse[1] < 480: 
                            btnColorMore6 = (255,255,255)
                            btnFontMore6 = (255,0,0)
                            if click[0] == 1:
                                DexHome.selectionMade = True
                                DexHome.selectedOption = 11


                    Draw.RoundRect(mainSurface,btnColorMore1,(1*10+0*boxWidth,10,boxWidth,boxHeight),radius,borderWidth,borderColor)
                    Draw.RoundRect(mainSurface,btnColorMore2,(3*10+1*boxWidth,10,boxWidth,boxHeight),radius,borderWidth,borderColor)
                    Draw.RoundRect(mainSurface,btnColorMore3,(5*10+2*boxWidth,10,boxWidth,boxHeight),radius,borderWidth,borderColor)

                    Draw.RoundRect(mainSurface,btnColorMore4,(1*10+0*boxWidth,3*10+boxHeight,boxWidth,boxHeight),radius,borderWidth,borderColor)
                    Draw.RoundRect(mainSurface,btnColorMore5,(3*10+1*boxWidth,3*10+boxHeight,boxWidth,boxHeight),radius,borderWidth,borderColor)
                    Draw.RoundRect(mainSurface,btnColorMore6,(5*10+2*boxWidth,3*10+boxHeight,boxWidth,boxHeight),radius,borderWidth,borderColor)

                    Text.Write(mainSurface,(1*10+0*boxWidth+boxWidth/2,10+boxHeight/2),"< Back",fontSize,"joy.otf",btnFontMore1,True)

                    Text.Write(mainSurface,(3*10+1*boxWidth+boxWidth/2,10+boxHeight/2-20),"Candy",fontSize,"joy.otf",btnFontMore2,True)
                    Text.Write(mainSurface,(3*10+1*boxWidth+boxWidth/2,10+boxHeight/2+20),"Calculator",fontSize,"joy.otf",btnFontMore2,True)

                    Text.Write(mainSurface,(5*10+2*boxWidth+boxWidth/2,10+boxHeight/2-20),"Trainer",fontSize,"joy.otf",btnFontMore3,True)
                    Text.Write(mainSurface,(5*10+2*boxWidth+boxWidth/2,10+boxHeight/2+20),"Card",fontSize,"joy.otf",btnFontMore3,True)

                    Text.Write(mainSurface,(1*10+0*boxWidth+boxWidth/2,3*10+boxHeight+boxHeight/2),"---",fontSize,"joy.otf",btnFontMore4,True)
                    Text.Write(mainSurface,(3*10+1*boxWidth+boxWidth/2,3*10+boxHeight+boxHeight/2),"---",fontSize,"joy.otf",btnFontMore5,True)

                    Text.Write(mainSurface,(5*10+2*boxWidth+boxWidth/2,3*10+boxHeight+boxHeight/2-20),"Settings /",fontSize,"joy.otf",btnFontMore6,True)
                    Text.Write(mainSurface,(5*10+2*boxWidth+boxWidth/2,3*10+boxHeight+boxHeight/2+20)," Update",fontSize,"joy.otf",btnFontMore6,True)


                    if DexHome.selectionMade:
                        if fadeOutCtr <= 3:
                            boxWidth +=1
                            boxHeight +=1
                        if fadeOutCtr > 3:
                            boxWidth -=5
                            boxHeight -=5
                            if fontSize > 0: fontSize -= 2
                        if fadeOutCtr > 10:
                            fadeOutColor = (30,30,30)
                            Draw.AAFilledCircle(mainSurface,400,240,(fadeOutCtr-10)*40,fadeOutColor,fadeOutColor,3)
                        if fadeOutCtr > 25: 

                            boxWidth = int(266.66 - 2*10)
                            boxHeight = 240-2*10
                            fontSize = 35
                            fadeOutCtr = 0
   
                            DexHome.selectionMade=False

                            if DexHome.selectedOption == 6: DexHome.selectedScreen = 1
                            if DexHome.selectedOption == 7: pass
                            if DexHome.selectedOption == 8: pass
                            if DexHome.selectedOption == 9: pass
                            if DexHome.selectedOption == 10: pass
                            if DexHome.selectedOption == 11: pass

                            repressCooldown = 10

                        fadeOutCtr += 1
    
                    if repressCooldown > 0: repressCooldown -= 1

                # Update Screen
                pygame.display.update()
                clock.tick(60)

        DexHome.running = True
        return