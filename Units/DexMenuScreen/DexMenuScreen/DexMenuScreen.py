# Importing Modules
import pygame
from pygame import gfxdraw
import time
import random
import sys
import sqlite3

# PyGame Initialisation
pygame.init()
clock = pygame.time.Clock()
#pygame.mouse.set_visible(False)

# Window and Surface Initialisation
displayWidth = 800
displayHeight = 480
mainSurface = pygame.display.set_mode((displayWidth,displayHeight))

menuSurface = pygame.Surface((800,480)).convert()

# DB-Initialisation and Setup
conn = sqlite3.connect('pokemon.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

running = True



backgroundImage = pygame.image.load("background.jpg").convert()
frameImage = pygame.image.load("frame.png").convert()


menuSurface.fill((0,0,0))
menuSurface.set_colorkey((0,0,0))
mainSurface.blit(backgroundImage,(0,0))
menuSurface.blit(frameImage,(0,0))
mainSurface.blit(menuSurface,(0,0))

while running:

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

    clock.tick(60)
    pygame.display.update()