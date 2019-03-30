import pygame
from pygame import gfxdraw
from CText import Text

class UI(object):
    """description of class"""

    def ProgressBar(surface,pos,width,height,color,text,minValue,maxValue,value):
        white = (255,255,255)
        displayWidth = int(width/((maxValue-minValue+1)/(value-minValue+1)))-1

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],int(height/2),white)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],int(height/2),white)
        pygame.gfxdraw.aacircle(surface,pos[0]+width,pos[1],int(height/2),white)
        pygame.gfxdraw.filled_circle(surface,pos[0]+width,pos[1],int(height/2),white)
        pygame.gfxdraw.box(surface,(pos[0],pos[1]-int(height/2),width,height),white)

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],int(height/2)-2,color)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],int(height/2)-2,color)
        pygame.gfxdraw.aacircle(surface,pos[0]+displayWidth,pos[1],int(height/2)-2,color)
        pygame.gfxdraw.filled_circle(surface,pos[0]+displayWidth,pos[1],int(height/2)-2,color)
        pygame.gfxdraw.box(surface,(pos[0],pos[1]-int(height/2)+2,displayWidth,height-4),color)

        Text.Write(surface,(pos[0],pos[1]-25),text,18,"joy.otf",white)
        Text.Write(surface,(pos[0]+width+30,pos[1]),str(value),18,"joy.otf",white,True)

