import pygame
import time
from pygame import gfxdraw
from CDrawing import Draw
from CText import Text

class Button(object):
    
    lastClickState = 0

    def RoundRect(surface,idleColor,hoverColor,textColor,rect,radius,text,fontsize,fontfamily,borderWidth=None,borderColor=(0,0,0),action = None,parameters = None, onReleaseAction = None, enabled = True):
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if borderWidth != None:  Draw.RoundRect(surface,borderColor,(rect[0]-borderWidth,rect[1]-borderWidth,rect[2]+2*borderWidth,rect[3]+2*borderWidth),radius+borderWidth)

        if Button.lastClickState == 1 and click[0] == 0 and onReleaseAction != None:
            onReleaseAction()

        if enabled:

            if rect[0] < mouse[0] < rect[0]+rect[2] and rect[1] < mouse[1] < rect[1]+rect[3]:
                activeColor = hoverColor 
                if click[0] == 1 and action != None:
                    if parameters == None: action() 
                    else: action(parameters)
                    time.sleep(0.2)
                
            else: activeColor = idleColor

        else:
            activeColor = (100,100,100)

        pygame.draw.circle(surface,activeColor,(rect[0]+radius,rect[1]+radius),radius)    
        pygame.draw.circle(surface,activeColor,(rect[0]-radius + rect[2],rect[1]+radius),radius)
        pygame.draw.circle(surface,activeColor,(rect[0]+radius,rect[1]-radius + rect[3]),radius)
        pygame.draw.circle(surface,activeColor,(rect[0]-radius + rect[2],rect[1]-radius + rect[3]),radius)

        pygame.draw.rect(surface,activeColor,(rect[0] + radius, rect[1], rect[2] - 2*radius, rect[3]))
        pygame.draw.rect(surface,activeColor,(rect[0], rect[1] + radius, rect[2], rect[3] - 2*radius))

        Text.Write(surface,(rect[0]+int(rect[2]/2),rect[1]+int(rect[3]/2)),text,fontsize,fontfamily,textColor,True)

        Button.lastClickState = click[0]        

        

        if borderWidth != None: return (rect[0]-borderWidth,rect[1]-borderWidth,rect[2]+2*borderWidth,rect[3]+2*borderWidth)
        else: return rect

    def Circle(surface,idleColor,hoverColor,textColor,pos,radius,text,fontsize,fontfamily,borderWidth=None,borderColor=(0,0,0),action = None,parameters = None, onReleaseAction = None, enabled = True):
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if borderWidth != None:  Draw.Circle(surface,borderColor,pos,radius+borderWidth)

        if Button.lastClickState == 1 and click[0] == 0 and onReleaseAction != None:
            onReleaseAction()

        if enabled:

            if pos[0]-radius < mouse[0] < pos[0]+radius and pos[1]-radius < mouse[1] < pos[1]+radius:
                activeColor = hoverColor 
                if click[0] == 1 and action != None:
                    if parameters == None: action() 
                    else: action(parameters)
                    time.sleep(0.2)
                
            else: activeColor = idleColor

        else:
            activeColor = (100,100,100)

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],radius,activeColor)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],radius,activeColor)

        Text.Write(surface,pos,text,fontsize,fontfamily,textColor,True)

        Button.lastClickState = click[0]        

        

        if borderWidth == None: return (pos[0]-radius,pos[1]-radius,2*radius+2,2*radius+2)
        else: return (pos[0]-radius-borderWidth,pos[1]-radius-borderWidth,2*radius+2*borderWidth+2,2*radius+2*borderWidth+2)


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