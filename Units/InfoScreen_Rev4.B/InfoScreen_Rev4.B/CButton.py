import pygame
import time
from pygame import gfxdraw
from CText import Text
from CDrawing import Draw
from threading import Thread

class Button:

    sleepThread = Thread()
    idleColor = (0,0,0)
    hoverColor = (40,40,40)
    disabledColor = (60,60,60)
    fontColor = (255,255,255)
    borderColor = (255,255,255)
    clickCooldown = 0.2

    fontFamily = "default"

    class RoundRect:

        def __init__(self, surface, rect, radius, text, fontSize, borderWidth = None, clickAction = None, clickParameters = None, releaseAction = None, releaseParameters = None):
            self.surface = surface
            self.rect = rect
            self.radius = radius
            self.text = text
            self.fontSize = fontSize
            self.borderWidth = borderWidth

            self.idleColor = Button.idleColor
            self.hoverColor = Button.hoverColor
            self.disabledColor = Button.disabledColor
            self.fontColor = Button.fontColor
            self.borderColor = Button.borderColor

            self.fontFamily = Button.fontFamily

            self.clickAction = clickAction
            self.clickParameters = clickParameters
            self.releaseAction = releaseAction
            self.releaseParameters = releaseParameters

            self.lastClickState = 0

        def Show(self, enabled = True, disabled = False):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if not disabled:
                if enabled:
                    if self.rect[0] < mouse[0] < self.rect[0] + self.rect[2] and self.rect[1] < mouse[1] < self.rect[1] + self.rect[3]:
 
                        Draw.RoundRect(self.surface,self.hoverColor,self.rect,self.radius,self.borderWidth,self.borderColor)

                        if not Button.sleepThread.isAlive():
                            if click[0] == 1:
                                if self.clickAction != None:
                                    if self.clickParameters != None: self.clickAction(self.clickParameters)
                                    else: self.clickAction()

                                Button.sleepThread = Thread(target = time.sleep, args = (Button.clickCooldown,)) 
                                Button.sleepThread.start()    

                            if click[0] == 0 and self.lastClickState == 1:
                                if self.releaseAction != None:
                                    if self.releaseParameters != None: self.releaseAction(self.releaseParameters)
                                    else: self.releaseAction()
                    else: Draw.RoundRect(self.surface,self.idleColor,self.rect,self.radius,self.borderWidth,self.borderColor)
                else: Draw.RoundRect(self.surface,self.idleColor,self.rect,self.radius,self.borderWidth,self.borderColor)
            else: Draw.RoundRect(self.surface,self.disabledColor,self.rect,self.radius,self.borderWidth,self.borderColor)

            Text.Write(self.surface,(self.rect[0]+self.rect[2]/2,self.rect[1]+self.rect[3]/2),self.text,self.fontSize,self.fontFamily,self.fontColor,True)

            self.lastClickState = click[0]

            if self.borderWidth != None: return (self.rect[0]-self.borderWidth,self.rect[1]-self.borderWidth,self.rect[2]+2*self.borderWidth,self.rect[3]+2*self.borderWidth)
            else: return self.rect

        


