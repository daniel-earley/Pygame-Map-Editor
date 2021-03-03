import pygame, os
pygame.init()
class MapTile:
    def __init__(self, terrain, location, isOccupied = False, isSpawn = False, isCollision = False):
        # Terrain is the tile type (grass, forest, etc)
        self.terrain = terrain
        # Location is a tuple which holds the x and y position of the tile (top left corner)
        self.location = location
        # isOccupied is a boolean value based on whether the space is occupied by a character or not
        self.isOccupied = isOccupied
        # isSpawn is a boolean value based on whether the space is used for spawning entities
        self.isSpawn = isSpawn
        # isCollision is a boolean value based on whether the space is passable or not
        self.isCollision = isCollision
        # isVisible is a boolean value that determines whether a tile is visible in the map editor (off screen tiles are not visible)
        #self.isVisible = isVisible
        
    def saveDict(self):
        #loc = self.location[0]//100, self.location[1]//100
        #newDict = {'terrain':self.terrain, 'location':self.location, 'isOccupied':self.isOccupied, 'isSpawn':self.isSpawn, 'isCollision':self.isCollision, 'isVisible':self.isVisible}
        newDict = {'terrain':self.terrain, 'location':self.location, 'isOccupied':self.isOccupied, 'isSpawn':self.isSpawn, 'isCollision':self.isCollision}
        #mapDict = {str(loc):newDict} 
        return newDict

    def move(self, distance, direction):
        # Add or subtract the distance needed to move in a certain direction (For Scrolling)
        locX = self.location[0]
        locY = self.location[1]
        if direction == "Up": # Scroll Up
            locY -= distance
        elif direction == "Down": # Scroll Down 
            locY += distance
        elif direction == "Right": # Scroll Right
            locX -= distance
        elif direction == "Left": # Scroll Left
            locX += distance

        self.location = (locX, locY)

    def setOccupied(self, isOccupied):
        #if self.isVisible:
        self.isSpawn = False
        self.isCollision = False
        self.isOccupied = isOccupied

    def getOccupied(self):
        return self.isOccupied

    def getTerrain(self):
        return self.terrain
    
    def setTerrain(self, terrain):
        self.terrain = terrain
    
    def getLocation(self):
        return self.location

    def getSpawn(self):
        return self.isSpawn
    
    def setSpawn(self, isSpawn):
        #if self.isVisible:
        self.isOccupied = False
        self.isCollision = False
        self.isSpawn = isSpawn

    def getCollision(self):
        return self.isCollision
    
    def setCollision(self, isCollision):
        #if self.isVisible:
        self.isSpawn = False
        self.isOccupied = False
        self.isCollision = isCollision

    #def getVisible(self):
    #    return self.isVisible

    #def setVisible(self, isVisible):
    #    self.isVisible = isVisible

    def getEmpty(self):
        if not self.getCollision() and not self.getOccupied() and not self.getSpawn():
            return True

    def setEmpty(self):
        #if self.isVisible:
        self.isOccupied = False
        self.isSpawn = False
        self.isCollision = False

    def isMouseOver(self):
        pos = pygame.mouse.get_pos()
        coords = self.getLocation()
        if pos[0] >= coords[0] and pos[0] < (coords[0] + 100):
            if pos[1] >= coords[1] and pos[1] < (coords[1] + 100):
                return True

    def getTileImg(self):
        # this function loads the tile image based on the terrain
        # assume that the tile img file name is terrain + .png
        name = self.getTerrain() + ".png"
        #print (name)
        fileDir = os.path.dirname(__file__)
        assetDir = os.path.join(fileDir, 'assets')
        # load image
        tile = pygame.image.load(os.path.join(assetDir, name))
        return tile

    def drawMapTile(self, window):
        #if self.isVisible:
        location = self.getLocation()
        tile = self.getTileImg()
        window.blit(tile, (location))
        
    #can be deleted -> for testing
    def __str__(self):
        return self.terrain + ' ' +str(self.location) + ' ' + str(self.isOccupied) + ' ' + str(self.isSpawn) + ' ' + str(self.isCollision) #+ ' ' + str(self.isVisible)

    