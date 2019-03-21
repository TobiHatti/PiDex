import pygame
from pygame import gfxdraw
from CDrawing import Draw
from CText import Text

class Button(object):

    def RoundRect(surface,idleColor,hoverColor,textColor,rect,radius,text,fontsize,fontfamily,borderWidth=None,borderColor=(0,0,0),action = None,parameters = None):
        
        if borderWidth != None:  Draw.RoundRect(surface,borderColor,(rect[0]-borderWidth,rect[1]-borderWidth,rect[2]+2*borderWidth,rect[3]+2*borderWidth),radius+borderWidth)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if rect[0] < mouse[0] < rect[0]+rect[2] and rect[1] < mouse[1] < rect[1]+rect[3]:
            activeColor = hoverColor 
            if click[0] == 1 and action != None:
                if parameters == None: action() 
                else: action(parameters)
        else: activeColor = idleColor

        pygame.draw.circle(surface,activeColor,(rect[0]+radius,rect[1]+radius),radius)    
        pygame.draw.circle(surface,activeColor,(rect[0]-radius + rect[2],rect[1]+radius),radius)
        pygame.draw.circle(surface,activeColor,(rect[0]+radius,rect[1]-radius + rect[3]),radius)
        pygame.draw.circle(surface,activeColor,(rect[0]-radius + rect[2],rect[1]-radius + rect[3]),radius)

        pygame.draw.rect(surface,activeColor,(rect[0] + radius, rect[1], rect[2] - 2*radius, rect[3]))
        pygame.draw.rect(surface,activeColor,(rect[0], rect[1] + radius, rect[2], rect[3] - 2*radius))

        Text.Write(surface,(rect[0]+int(rect[2]/2),rect[1]+int(rect[3]/2)),text,fontsize,fontfamily,textColor,True)

        if borderWidth != None: return (rect[0]-borderWidth,rect[1]-borderWidth,rect[2]+2*borderWidth,rect[3]+2*borderWidth)
        else: return rect


class UI(object):

    def ProgressBar(surface,pos,width,height,color,text,minValue,maxValue,value):
        white = (255,255,255)
        displayWidth = int(width/((maxValue-minValue+1)/(value-minValue+1)))-1

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],int(height/2),white)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],int(height/2),white)
        pygame.gfxdraw.aacircle(surface,pos[0]+width,pos[1],int(height/2),white)
        pygame.gfxdraw.filled_circle(surface,pos[0]+width,pos[1],int(height/2),white)
        pygame.gfxdraw.box(surface,(pos[0],pos[1]-int(height/2),width,height+1),white)

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],int(height/2)-3,color)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],int(height/2)-3,color)
        pygame.gfxdraw.aacircle(surface,pos[0]+displayWidth,pos[1],int(height/2)-3,color)
        pygame.gfxdraw.filled_circle(surface,pos[0]+displayWidth,pos[1],int(height/2)-3,color)
        pygame.gfxdraw.box(surface,(pos[0],pos[1]-int(height/2)+3,displayWidth,height+1-6),color)

        Text.Write(surface,(pos[0],pos[1]-30),text,20,"calibrilight.ttf",white)
        Text.Write(surface,(pos[0]+width+30,pos[1]),str(value),20,"calibrilight.ttf",white,True)