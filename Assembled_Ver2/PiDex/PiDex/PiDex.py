# Importing Modules
import pygame
import time
import random
import sys
import math

from DexInfo import DexInfo
from DexMenu import DexMenu

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

    DexMenu.Show()

    pygame.display.update()
    clock.tick(1)
    






