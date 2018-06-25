import pygame, sys
from pygame.locals import *

pygame.init()

labelFont = pygame.font.SysFont("Arial",20,True)

class colourSlider(object):
    def __init__(self,x,y,width=100,height=30,label = ""):
        self.bgshape = pygame.Rect(x,y,width,height)
        self.fgshape = pygame.Rect(x,y,width/20,height)
        self.min = 0
        self.max = 255
        self.value = 255
        self.label = label


    def findSliderPos(self,value):
        usableW = self.bgshape.width - self.fgshape.width
        offsetX = value*(usableW/self.max)
        pos = (self.bgshape.left+offsetX+self.fgshape.width/2,self.fgshape.center[1])
        return pos

    def draw(self,surf,hovered):
        if hovered:
            pygame.draw.rect(surf, (0,0,0), self.bgshape, 5)
            pygame.draw.rect(surf,(200,200,200),self.bgshape,0)
        else:
            pygame.draw.rect(surf, (0, 0, 0), self.bgshape, 5)
            pygame.draw.rect(surf, (150, 150, 150), self.bgshape, 0)

        self.fgshape.center = self.findSliderPos(self.value)
        pygame.draw.rect(surf, (0, 0, 0), self.fgshape, 5)
        pygame.draw.rect(surf, (100, 100, 100), self.fgshape, 0)

        label = labelFont.render(self.label+": "+str(self.value),True,(0,0,0))
        labelRect = label.get_rect()
        labelRect.left = self.bgshape.left
        labelRect.center = (labelRect.center[0],self.bgshape.center[1])
        surf.blit(label,labelRect)

    def update(self,surf):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.bgshape.left <= mouse[0] <= self.bgshape.right and self.bgshape.top <= mouse[1] <= self.bgshape.bottom:
            self.draw(surf,True)
            if click[0] == 1:
                rel = mouse[0] - self.bgshape.left - self.fgshape.width/2
                usableW = self.bgshape.width - self.fgshape.width
                self.value = int((rel/usableW)*255)
                if self.value<0:
                    self.value = 0
                elif self.value>255:
                    self.value = 255
        else:
            self.draw(surf,False)


def findCloseColour(colour):

    bestScore = 1000
    bestName = ""

    for key in pygame.color.THECOLORS:
        score = 0
        for i in range(3):
            score += abs(pygame.color.THECOLORS[key][i] - colour[i])
        if score < bestScore:
            bestScore = score
            bestName = key

    return(bestName)


DISPLAYSURF = pygame.display.set_mode((800, 600),pygame.DOUBLEBUF)
pygame.display.set_caption('Colour Picker')

rSlider = colourSlider(100,400,600,30,"R")
gSlider = colourSlider(100,450,600,30,"G")
bSlider = colourSlider(100,500,600,30,"B")



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.fill((255,255,255))
    rSlider.update(DISPLAYSURF)
    gSlider.update(DISPLAYSURF)
    bSlider.update(DISPLAYSURF)

    colour = (rSlider.value,gSlider.value,bSlider.value)
    closeColour = findCloseColour(colour)
    pygame.draw.rect(DISPLAYSURF,(0,0,0),(100,100,600,200),5)

    pygame.draw.rect(DISPLAYSURF,colour,(100,100,300,200))
    pygame.draw.rect(DISPLAYSURF, pygame.Color(closeColour), (400, 100, 300, 200))

    colourName = labelFont.render("Closest Colour: "+closeColour,True,(0,0,0))
    colourNameRect = colourName.get_rect()
    colourNameRect.center = (400,350)
    DISPLAYSURF.blit(colourName,colourNameRect)
    pygame.display.flip()
