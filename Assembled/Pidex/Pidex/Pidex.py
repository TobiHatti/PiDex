# Importing Modules
import pygame
import time
import random
import sys
import math

from Unit_DexMenu import *
from Unit_DexInfo import *

# Color Definitions
white = (255,255,255)
grayA = (200,200,200)
grayB = (150,150,150)
grayC = (100,100,100)
black = (0,0,0)

# PyGame Initialisation
pygame.init()
clock = pygame.time.Clock()
#pygame.mouse.set_visible(False)

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


# Variables
menuOptionSelected = False
selectedMenuOption = 0

# Functions

# Defining Segment-Polygons
# Top segments
pSegment1 = ((0,0),(displayWidth/2,0),(displayWidth/2,displayHeight/2),(0,displayHeight/6))
pSegment2 = ((displayWidth,displayHeight/6),(displayWidth,0),(displayWidth/2,0),(displayWidth/2,displayHeight/2))
# Middle segments
pSegment3 = ((0,displayHeight/6),(displayWidth/2,displayHeight/2),(0,displayHeight-(displayHeight/6)))
pSegment4 = ((displayWidth,displayHeight/6),(displayWidth/2,displayHeight/2),(displayWidth,displayHeight-(displayHeight/6)))
# Botton Section
pSegment5 = ((0,displayHeight),(0,displayHeight-(displayHeight/6)),(displayWidth/2,displayHeight/2),(displayWidth/3,displayHeight))
pSegment6 = ((displayWidth/3,displayHeight),(displayWidth/2,displayHeight/2),(displayWidth-(displayWidth/3),displayHeight))
pSegment7 = ((displayWidth,displayHeight),(displayWidth,displayHeight-(displayHeight/6)),(displayWidth/2,displayHeight/2),(displayWidth-(displayWidth/3),displayHeight))


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

    # Checking Mouse Positions
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Segment 1
    if 0 < mouse[0] < displayWidth/2 and 0 < mouse[1] < displayHeight/3:
        pygame.draw.polygon(mainSurface,black,pSegment1)
        if click[0] == 1: 
            menuOptionSelected = True
            selectedMenuOption = 1
    else: pygame.draw.polygon(mainSurface,grayA,pSegment1)

    # Segment 2
    if displayWidth/2 < mouse[0] < displayWidth and 0 < mouse[1] < displayHeight/3:
        pygame.draw.polygon(mainSurface,black,pSegment2)
        if click[0] == 1: 
            menuOptionSelected = True
            selectedMenuOption = 2
    else: pygame.draw.polygon(mainSurface,grayB,pSegment2)

    # Segment 3
    if 0 < mouse[0] < displayWidth/3 and displayHeight/3 < mouse[1] < displayHeight-(displayHeight/3):
        pygame.draw.polygon(mainSurface,black,pSegment3)
        if click[0] == 1: 
            menuOptionSelected = True
            selectedMenuOption = 3
    else: pygame.draw.polygon(mainSurface,grayB,pSegment3)

    # Segment 4
    if displayWidth-(displayWidth/3) < mouse[0] < displayWidth and displayHeight/3 < mouse[1] < displayHeight-(displayHeight/3):
        pygame.draw.polygon(mainSurface,black,pSegment4)
        if click[0] == 1: 
            menuOptionSelected = True
            selectedMenuOption = 4
    else: pygame.draw.polygon(mainSurface,grayA,pSegment4)

    # Segment 5
    if 0 < mouse[0] < displayWidth/3 and displayHeight-(displayHeight/3) < mouse[1] < displayHeight:
        pygame.draw.polygon(mainSurface,black,pSegment5)
        if click[0] == 1: 
            menuOptionSelected = True
            selectedMenuOption = 5
    else: pygame.draw.polygon(mainSurface,grayA,pSegment5)

    # Segment 6
    if displayWidth/3 < mouse[0] < displayWidth-(displayWidth/3) and displayHeight-(displayHeight/3) < mouse[1] < displayHeight:
        pygame.draw.polygon(mainSurface,black,pSegment6)
        if click[0] == 1: 
            menuOptionSelected = True
            selectedMenuOption = 6
    else: pygame.draw.polygon(mainSurface,grayC,pSegment6)

    # Segment 7
    if displayWidth-(displayWidth/3) < mouse[0] < displayWidth and displayHeight-(displayHeight/3) < mouse[1] < displayHeight:
        pygame.draw.polygon(mainSurface,black,pSegment7)
        if click[0] == 1: 
            menuOptionSelected = True
            selectedMenuOption = 7
    else: pygame.draw.polygon(mainSurface,grayB,pSegment7)


    # Center
    pygame.draw.circle(mainSurface,(0,0,0),(int(displayWidth/2),int(displayHeight/2)),100)
    pygame.draw.circle(mainSurface,(255,255,255),(int(displayWidth/2),int(displayHeight/2)),85)

    if menuOptionSelected:
        menuOptionSelected = False
        for x in range(0, 500):
            if x%2 == 0:
                pygame.draw.circle(mainSurface,(255,255,255),(int(displayWidth/2),int(displayHeight/2)),100+x)
                pygame.display.update()
        if selectedMenuOption == 1:
            print("Option 1")
            DexMenu.Show()
        elif selectedMenuOption == 2:
            print("Option 2")
        elif selectedMenuOption == 3:
            print("Option 3")
        elif selectedMenuOption == 4:
            print("Option 4")
        elif selectedMenuOption == 5:
            print("Option 5")
        elif selectedMenuOption == 6:
            print("Option 6")
        elif selectedMenuOption == 7:
            print("Option 7")
    else: pygame.display.update()
    






