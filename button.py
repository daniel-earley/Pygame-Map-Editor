import pygame
pygame.init()
class Button:
    def __init__(self, img, x, y, w, h, scale = False):
        self.img = img
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.scale = scale
    
    def mouseOver(self):
        pos = pygame.mouse.get_pos()
        if pos[0] >= self.x and pos[0] < self.x + self.w:
            if pos[1] >= self.y and pos[1] < self.y + self.h:
                return True

    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y

    def getLocation(self):
        loc = (self.x, self.y)
        return loc

    def getDimensions(self):
        dim = (self.w, self.h)
        return dim

    def setScale(self, scale):
        self.scale = scale
    
    def getScale(self):
        return self.scale

    def drawButton(self, window):
        if self.getScale():
            self.img = pygame.transform.smoothscale(self.img, (self.w, self.h))
        window.blit(self.img, (self.x, self.y))