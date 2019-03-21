import pygame
import os

class Sprite(object):
    """description of class"""

    tilesAmount = None
    frames = None
    current = None
    sprite = None
    frameIndex = 0

    def Create(filePath):

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
                if r == spriteTilesVert-1:
                    if image.get_at((150,150)) != (0,0,0,255): cells.append(image)
                    else: spriteOffset += 1
                else: cells.append(image)
        playerImg = cells[0]
        player = playerImg.get_rect()
        player.center = (150,150)
        spriteFrame = 0

        Sprite.tilesAmount = spriteTiles * spriteTilesVert - spriteOffset
        Sprite.frames = cells
        Sprite.current = playerImg
        Sprite.sprite = player

        #return (spriteTiles * spriteTilesVert - spriteOffset,cells,playerImg,player)

    def Cycle(frame,tilesAmt,cells):
        spriteFrame = frame + 1
        if spriteFrame >= tilesAmt: spriteFrame = 0
        spriteImage = cells[spriteFrame]

        Sprite.frameIndex = spriteFrame
        Sprite.current = spriteImage

        #return (spriteFrame,spriteImage)


