import pygame

class Text(object):
    """description of class"""

    def Write(surface,pos,text,fontSize,fontFamily,fontColor,centered = False):
        outputText = pygame.font.Font(fontFamily,fontSize)
        textSurf = outputText.render(text,True,fontColor)
        textRect = outputText.render(text,True,fontColor).get_rect()
        trect = textRect
        if centered:
            textRect.center = (pos[0],pos[1])
        else:
            textRect = (pos[0],pos[1])
        surface.blit(textSurf,textRect)

        return (pos[0],pos[1],trect[2],trect[3])


    def WriteMultiline(surface, text, pos, font, color=(0,0,0)):
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

        return (pos[0],pos[1],word_width,word_height)

