class Basic:

    def WriteText(surface,pos,text,fontSize,fontFamily,fontColor,centered = False):
        
        import pygame

        outputText = pygame.font.Font(fontFamily,fontSize)
        textSurf = outputText.render(text,True,fontColor)
        textRect = outputText.render(text,True,fontColor).get_rect()
        if centered:
            textRect.center = (pos[0],pos[1])
        else:
            textRect = (pos[0],pos[1])
        surface.blit(textSurf,textRect)

    def BlitText(surface, text, pos, font, color=(0,0,0)):
        words = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0] 
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0] 
                    y += word_height 
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0] 
            y += word_height 

    def Button(surface,pos,radius,text,fontSize,idleColor,textColor,action = None,parameter = None,surfaceOffset = (0,0), buttonEnabled = True):
        
        import pygame

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        hoverColor = (idleColor[0]/2,idleColor[1]/2,idleColor[2]/2)

        if pos[0] + radius + surfaceOffset[0] > mouse[0] > pos[0] - radius + surfaceOffset[0] and pos[1] + radius + surfaceOffset[1] > mouse[1] > pos[1] - radius + surfaceOffset[1]:

            pygame.gfxdraw.aacircle(surface,pos[0]-2,pos[1]-2,radius-4,hoverColor)
            pygame.gfxdraw.filled_circle(surface,pos[0]-2,pos[1]-2,radius-4,hoverColor)
            if click[0] == 1 and action != None and buttonEnabled:
                if parameter == None: action()
                else: action(parameter)
        else:
            pygame.gfxdraw.aacircle(surface,pos[0]-2,pos[1]-2,radius-4,idleColor)
            pygame.gfxdraw.filled_circle(surface,pos[0]-2,pos[1]-2,radius-4,idleColor)

        Basic.WriteText(surface,pos,text,fontSize,"PokemonSolid.ttf",textColor,True)


    def ProgressBar(surface,pos,width,height,color,text,minValue,maxValue,value):

        import pygame

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

        Basic.WriteText(surface,(pos[0],pos[1]-30),text,20,"calibrilight.ttf",white)
        Basic.WriteText(surface,(pos[0]+width+30,pos[1]),str(value),20,"calibrilight.ttf",white,True)
