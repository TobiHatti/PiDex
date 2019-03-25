# Importing Modules
import pygame
import time
import random
import sys
import math

from CButton import Button

# PyGame Initialisation
pygame.init()
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


Button.fontFamily = "joy.otf"
Button.idleColor = (0,255,0)
Button.hoverColor = (100,255,100)

btn1 = Button.RoundRect(mainSurface,(20,20,100,50),20,"Hallo",13,2)
btn2 = Button.RoundRect(mainSurface,(20,200,100,50),20,"Tschüss",13,2)


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

   
    btn1.Show()
    btn2.Show(False)

    clock.tick(60)


    pygame.display.update()
    






