import pygame
from pygame import gfxdraw
from CText import Text

class Draw(object):
    """description of class"""

    def RoundRect(surface,color,rect,radius,borderWidth=None,borderColor=(0,0,0),titlebar = None):

        if borderWidth != None:  Draw.RoundRect(surface,borderColor,(rect[0]-borderWidth,rect[1]-borderWidth,rect[2]+2*borderWidth,rect[3]+2*borderWidth),radius+borderWidth)

        pygame.draw.circle(surface,color,(rect[0]+radius,rect[1]+radius),radius)    
        pygame.draw.circle(surface,color,(rect[0]-radius + rect[2],rect[1]+radius),radius)
        pygame.draw.circle(surface,color,(rect[0]+radius,rect[1]-radius + rect[3]),radius)
        pygame.draw.circle(surface,color,(rect[0]-radius + rect[2],rect[1]-radius + rect[3]),radius)

        pygame.draw.rect(surface,color,(rect[0] + radius, rect[1], rect[2] - 2*radius, rect[3]))
        pygame.draw.rect(surface,color,(rect[0], rect[1] + radius, rect[2], rect[3] - 2*radius))

        if titlebar != None:
            pygame.draw.circle(surface,borderColor,(rect[0]+radius,rect[1]+radius),radius)
            pygame.draw.circle(surface,borderColor,(rect[0]+rect[2]-radius,rect[1]+radius),radius)
            pygame.draw.rect(surface,borderColor,(rect[0]+radius,rect[1],rect[2]-2*radius,radius))
            pygame.draw.rect(surface,color,(rect[0],rect[1]+radius,rect[2],radius))
            pygame.draw.rect(surface,borderColor,(rect[0],rect[1]+radius,rect[2],10))
            Text.Write(surface,(rect[0]+(rect[2]/2),rect[1]+14),titlebar,20,"joy.otf",(255,255,255),True)

        if borderWidth != None: return (rect[0]-borderWidth,rect[1]-borderWidth,rect[2]+2*borderWidth,rect[3]+2*borderWidth)
        else: return rect


    def Pokeball(surface,pos,color,backcolor):
        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],32,color)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],32,color)

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],29,backcolor)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],29,backcolor)

        pygame.draw.rect(surface,color,(pos[0]-30,pos[1]-1,31*2,3))

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],12,color)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],12,color)

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],10,backcolor)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],10,backcolor)

        pygame.gfxdraw.aacircle(surface,pos[0],pos[1],5,color)
        pygame.gfxdraw.filled_circle(surface,pos[0],pos[1],5,color)

        return pos

    def TypeSign1(surface,pos,color,text):
        pygame.draw.polygon(surface,color,((pos[0],pos[1]),(pos[0]+145,pos[1]),(pos[0]+115,pos[1]+35),(pos[0],pos[1]+35)))
        Text.Write(surface,(pos[0]+70,pos[1]+18),text,20,"joy.otf",(255,255,255),True)
        return (pos[0],pos[1],145,35)

    def TypeSign2(surface,pos,color,text):
        pygame.draw.polygon(surface,color,((pos[0]+30,pos[1]),(pos[0]+145,pos[1]),(pos[0]+145,pos[1]+35),(pos[0],pos[1]+35)))
        Text.Write(surface,(pos[0]+75,pos[1]+18),text,20,"joy.otf",(255,255,255),True)
        return (pos[0],pos[1],145,35)

    def TypeSignSingle(surface,pos,color,text):
        pygame.draw.polygon(surface,color,((pos[0],pos[1]),(pos[0]+220,pos[1]),(pos[0]+190,pos[1]+35),(pos[0],pos[1]+35)))
        pygame.draw.polygon(surface,color,((pos[0]+30+200,pos[1]),(pos[0]+200+70,pos[1]),(pos[0]+200+70,pos[1]+35),(pos[0]+200,pos[1]+35)))
        Text.Write(surface,(pos[0]+75,pos[1]+18),text,20,"joy.otf",(255,255,255),True)
        return (pos[0],pos[1],220,35)