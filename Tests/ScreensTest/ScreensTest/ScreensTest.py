import pygame
from pygame import movie,display
import time
import sys

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
hoverGreen = (0,150,0)
yellow = (255,255,0)
blue = (0,0,255)

displayWidth = 800
displayHeight = 480

mainScreen = pygame.display.set_mode((800,480))
mainScreen.fill((255,0,0))

#taskSurface = pygame.Surface((200,200))
#taskSurface.fill((255,255,0))
#mainScreen.blit(taskSurface,(20,20))

#infoSurface = pygame.Surface((300,100))
#infoSurface.fill((0,255,255))
#mainScreen.blit(infoSurface,(80,80))

clock = pygame.time.Clock()


def TextObjects(text,font):
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()

def WriteMessage(message):
    style = pygame.font.Font('freesansbold.ttf',100)
    TextSurf, TextRect = TextObjects(message,style)
    TextRect.center = ((displayWidth/2),(displayHeight/2))
    mainScreen.blit(TextSurf,TextRect)

    pygame.display.update()





# Loading Spritesheet

sheet = pygame.image.load("lucarioSpritesheet.png").convert()
cells = []
for n in range(59):
    width, height = (52,96)
    rect = pygame.Rect(n * width, 0,width,height)

    image = pygame.Surface(rect.size).convert()

    image.blit(sheet, (0,0),rect)
    alpha = image.get_at((0,0))
    image.set_colorkey(alpha)

    image = pygame.transform.scale2x(image)

    cells.append(image)

playerImg = cells[0]
player = playerImg.get_rect()
player.center = (80,100)

spriteStep = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #print(event)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] != 0: player.y -= 4
    if keys[pygame.K_DOWN] != 0: player.y += 4
    if keys[pygame.K_LEFT] != 0: player.x -= 4
    if keys[pygame.K_RIGHT] != 0: player.x += 4

    if keys[pygame.K_q] != 0: 
        pygame.quit()
        sys.exit()


    mainScreen.fill((255,255,255))
    mainScreen.blit(playerImg,player)

    spriteStep += 1
    if spriteStep >= 59: spriteStep = 0
    playerImg = cells[spriteStep]
    

    #buttons

  
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)

    
    if 400 +50 > mouse[0] > 400 - 50 and 200 + 50 > mouse[1] > 200 - 50: 
        pygame.draw.circle(mainScreen,hoverGreen,(400,200),50)
        if click[0] == 1:
            print("Lalalalala")
            time.sleep(0.1)
    else:
        pygame.draw.circle(mainScreen,green,(400,200),50)    

    

    
    if 150+100 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
        pygame.draw.rect(mainScreen,hoverGreen,(150,450,100,50))
    else:
        pygame.draw.rect(mainScreen,green,(150,450,100,50))

    buttonText = pygame.font.Font("freesansbold.ttf",20)
    textSurf,textRect = TextObjects("GO!",buttonText)
    textRect.center = ((150 + (100/2)),(450+(50/2)))
    mainScreen.blit(textSurf,textRect)

    pygame.display.update()

    clock.tick(60)