import pygame, os, json, pygame_textinput, startMenu
from map_tile import MapTile
from button import Button

# Load Images
fileDir = os.path.dirname(__file__)
assetDir = os.path.join(fileDir, 'assets')
grass = pygame.image.load(os.path.join(assetDir, "grass.png"))

# Load transparent squares
red = pygame.image.load(os.path.join(assetDir, "red_square.png"))
blue = pygame.image.load(os.path.join(assetDir, "blue_square.png"))
green = pygame.image.load(os.path.join(assetDir, "green_square.png"))
grey = pygame.image.load(os.path.join(assetDir, "grey_square.png"))

# Load Button Images
vpImg = pygame.image.load(os.path.join(assetDir, "viewProperties_button.png"))
spawnImg = pygame.image.load(os.path.join(assetDir, "setSpawn_button.png"))
changeOcImg = pygame.image.load(os.path.join(assetDir, "changeOccupied_button.png"))
jsonImg = pygame.image.load(os.path.join(assetDir, "saveAsJson_button.png"))
saveImg = pygame.image.load(os.path.join(assetDir, "saveAsImg_button.png"))
emptyImg = pygame.image.load(os.path.join(assetDir, "setEmpty_button.png"))
collImg = pygame.image.load(os.path.join(assetDir, "setCollision_button.png"))
# Create GUI Buttons
spawn_Button = Button(spawnImg, 1000, 500, 100, 40)
changeOc_Button = Button(changeOcImg, 1100, 500, 100, 40)
json_Button = Button(jsonImg, 1100, 540, 100, 40)
save_Button = Button(saveImg, 1000, 540, 100, 40)
vp_Button = Button(vpImg, 1000, 580, 100, 40)
empty_Button = Button(emptyImg, 1100, 580, 100, 40)
collision_Button = Button(collImg, 1000, 620, 100, 40)

# Toggle switches
viewToggle = True
spawnToggle = True
occupiedToggle = True
emptyToggle = True
collToggle = True

# Create run window
screen_width, screen_height = 1200, 1000
STEP = 100
WIN = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Map Editor")
info = pygame.display.Info()
width, height = info.current_w, info.current_h

# Global map variables
global mapX
global mapY
mapX = 0
mapY = 0
def createMap(name, width, height, terrain, tileImg, window):
    # Create an array of MapTiles that can be accessed anywhere in the file
    global mapArray
    global NAME
    NAME = name
    #print(NAME)
    mapArray = []
    for i in range(0, width, STEP):
        sub = []
        for j in range(0, height, STEP): 
            #if i >= 1000 or j >= 1000:
            #    sub.append(MapTile(terrain, (i, j), False, False, False, False))
            #else:
            window.blit(tileImg, (i, j))
            sub.append(MapTile(terrain, (i, j)))
        mapArray.append(sub)
    #print(len(mapArray), len(mapArray[0]))

def loadMap(name, window):
    # Declare Global Vars
    global mapArray
    global NAME
    NAME = name
    
    # Take the name of the map
    fileName = name + ".json"
    filePath = os.path.join(assetDir, fileName)

    # Load map Image
    mapImg = pygame.image.load(os.path.join(assetDir, name + ".png"))
    window.blit(mapImg, (mapX, mapY))
    
    # Open JSON file
    with open(filePath) as inFile:
        mapData = json.load(inFile)
    
    dimensions = mapData["Dimensions"]
    mapArray = []
    for i in range(0, dimensions[0]):
        sub = []
        for j in range(0, dimensions[1]):
            key = i, j
            data = mapData[str(key)]
            sub.append(MapTile(data['terrain'], data['location'], data['isOccupied'], data['isSpawn'], data['isCollision']))
        mapArray.append(sub)

def uniformSize():
    # x, y
    tup = (len(mapArray), len(mapArray[0]))
    return tup

def moveTools(button):
    size = uniformSize()
    width = size[0] * 100
    height = size[1] * 100
    button.setX(width)
    button.setY(height)

def moveSecondaryTools(buttonA, buttonB):
    # Move buttonA alongside buttonB
    dim = buttonB.getDimensions()
    loc = buttonB.getLocation()
    newX = loc[0] + dim[0]
    newY = loc[1] + dim[1]
    buttonA.setX(newX)
    buttonA.setY(newY)

def getTileLoc():
    # Gets the tile that the mouse is hovering over
    size = uniformSize()
    #width, height = pygame.display.get_surface().get_size()
    for i in range(size[0]):
        for j in range(size[1]):
            if mapArray[i][j].isMouseOver():
                return mapArray[i][j].getLocation()
 
# The Following functions are called on mouse click, Both functions are for drawing tiles(terrains)
# drawTile draws overtop of the previous tile, but does not update the MapTile
# changeTile changes the terrain of the MapTile, and then calls the MapTile draw function to replace the previous tile
def drawTile(tileImg, window):
    # Grabs the location of MapTile, then draws over top
    location = getTileLoc()
    window.blit(tileImg, (location))
    pygame.display.update()
   
def changeTile (terrain, window):
    # grab the location of MapTile, then change the terrain and the call the class draw func

    location = getTileLoc()
    # //10 will give the location of the MapTile in the 2d array
    x, y = location[0]//STEP, location[1]//STEP
    mapArray[x][y].setTerrain(terrain)
    mapArray[x][y].drawMapTile(window)

def setSpawn():
    # change the spawn property of the maptile
    pos = pygame.mouse.get_pos()
    size = uniformSize()
    if spawnToggle == False:
        if pos[0] >= 0 and pos[0] < (1000):
            if pos[1] >= 0 and pos[1] < (1000):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    loc = getTileLoc()
                    mapArray[loc[0]//STEP][loc[1]//STEP].setSpawn(True)
                
def setOccupied():
    pos = pygame.mouse.get_pos()
    size = uniformSize()
    if occupiedToggle == False:
        if pos[0] >= 0 and pos[0] < (1000):
            if pos[1] >= 0 and pos[1] < (1000):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    loc = getTileLoc()
                    mapArray[loc[0]//STEP][loc[1]//STEP].setOccupied(True)

def setCollision():
    pos = pygame.mouse.get_pos()
    size = uniformSize()
    if collToggle == False:
        if pos[0] >= 0 and pos[0] < (1000):
            if pos[1] >= 0 and pos[1] < (1000):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    loc = getTileLoc()
                    mapArray[loc[0]//STEP][loc[1]//STEP].setCollision(True)

def setEmpty():
    pos = pygame.mouse.get_pos()
    size = uniformSize()
    if emptyToggle == False:
        if pos[0] >= 0 and pos[0] < (1000):
            if pos[1] >= 0 and pos[1] < (1000):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    loc = getTileLoc()
                    mapArray[loc[0]//STEP][loc[1]//STEP].setEmpty()

def viewProperties(window):
    # If viewing is false then not viewing properties, set to true and view properties
    # If viewing is true, then viewing properties, set to false and stop viewing properties
    size = uniformSize()
    if viewToggle == False:

        #width, height = pygame.display.get_surface().get_size()
        for i in range(size[0]):
            for j in range(size[1]):
                # x, y = i//STEP, j//STEP
                if mapArray[i][j].getCollision():
                    # If the tile is a collision tile - set to grey
                    loc = mapArray[i][j].getLocation()
                    window.blit(grey, (loc))
                if mapArray[i][j].getSpawn():
                    # If the tile is a spawn tile - set to green
                    loc = mapArray[i][j].getLocation()
                    window.blit(green, (loc))
                if mapArray[i][j].getOccupied():
                    # If the tile is occupied - set to red
                    loc = mapArray[i][j].getLocation()
                    window.blit(red, (loc))
                if mapArray[i][j].getEmpty():
                    # If set to neither - set to blue
                    loc = mapArray[i][j].getLocation()
                    window.blit(blue, (loc))
    pygame.display.update()

def saveJson():
    size = uniformSize()
    fileName = NAME + ".json"
    stream = os.path.join(assetDir, fileName)
    data = {}
    data["Dimensions"] = (size[0], size[1])
    #data["Dimensions"].append((str(size[0]), str(size[1])))
    for i in range(size[0]):
        for j in range(size[1]):
            # x, y = i//STEP, j//STEP
            #info = mapArray[i][j].getLocation()
            #key = info[0]//STEP, info[1]//STEP
            #data[str(key)] = (mapArray[i][j].getInfo())
            #data[str(key)].append(str(mapArray[i][j]))
            
            tup = i, j
            data[str(tup)] = mapArray[i][j].saveDict()
        
    with open(stream, 'w') as outFile:
        json.dump(data, outFile)

def savePNG(window):
    fileName = NAME + ".png"
    stream = os.path.join(assetDir, fileName)
    size = uniformSize()
    rect = pygame.Rect(0,0,size[0] * STEP, size[1] * STEP)
    sub = window.subsurface(rect)
    pygame.image.save(sub, stream)

# Create the map
if startMenu.loadToggle:
    loadMap(startMenu.name, WIN)
else:
    createMap(startMenu.name,startMenu.width,startMenu.height,"grass",grass,WIN)  

def moveMap(direction, distance):
    # Counters for each direction Up/Down(-/+), Right/Left(-/+)
    size = uniformSize()
    # e.g. size[0] = 12, 1000//STEP = 10, therefore scroll up to 2 spaces
    #maxDist = size[0] - 10, size[1] - 10 # (x, y)
    
    if direction == "Up": # Scroll Up
        for i in range(size[0]):
            for j in range(size[1]):
                mapArray[i][j].move(100, "Up")
    if direction == "Down": # Scroll Down 
        for i in range(size[0]):
            for j in range(size[1]):
                mapArray[i][j].move(100, "Down")
    if direction == "Right": # Scroll Right
       for i in range(size[0]):
            for j in range(size[1]):
                mapArray[i][j].move(100, "Right")
    if direction == "Left": # Scroll Left
        for i in range(size[0]):
            for j in range(size[1]):
                mapArray[i][j].move(100, "Left")
    
    # Check if maptile is offscreen
    '''
    for i in range(size[0]):
        for j in range(size[1]):
            if i  * STEP >= 1000 or j  * STEP >= 1000:
                mapArray[i][j].setVisible(False)
            else:
                mapArray[i][j].setVisible(True)
    '''
def redraw():
    
    size = uniformSize()
    for i in range(size[0]):
        for j in range(size[1]):
            mapArray[i][j].drawMapTile(WIN)

    # Draw properties
    viewProperties(WIN)

    # Draw Toolbar Rectangle
    toolbar = pygame.Rect(1000, 0, 1000, 1200)
    pygame.draw.rect(WIN, (0,0,0), toolbar)

    # Draw Buttons
    
    vp_Button.drawButton(WIN)
    spawn_Button.drawButton(WIN)
    json_Button.drawButton(WIN)
    save_Button.drawButton(WIN)
    changeOc_Button.drawButton(WIN)
    empty_Button.drawButton(WIN)
    collision_Button.drawButton(WIN)

    # Update 
    pygame.display.update()


# Run Loop
running = True
size = uniformSize()
maxDist = size[0] - 10, size[1] - 10 # (x, y)
mapX, mapY = 0, 0
while running:
    redraw()
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            WIN = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        # If Buttons are clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if vp_Button.mouseOver(): # View Properties Button
                viewToggle = not viewToggle
            if spawn_Button.mouseOver(): # Spawn Button
                spawnToggle = not spawnToggle
                occupiedToggle = True
                emptyToggle = True
                collToggle = True
            if changeOc_Button.mouseOver(): # Change Occupied Button
                occupiedToggle = not occupiedToggle
                spawnToggle = True
                emptyToggle = True
                collToggle = True
            if collision_Button.mouseOver(): # Set Collision Button
                collToggle = not collToggle
                spawnToggle = True
                occupiedToggle = True
                emptyToggle = True
            if empty_Button.mouseOver(): # Set Empty Button
                emptyToggle = not emptyToggle
                spawnToggle = True
                occupiedToggle = True
                collToggle = True
            if json_Button.mouseOver():
                saveJson()
            if save_Button.mouseOver():
                savePNG(WIN)
    
        if keys[pygame.K_UP] and mapY > -maxDist[1]:
            mapY -= 1
            moveMap("Up", 100)
            
        if keys[pygame.K_DOWN] and mapY < 0:
            mapY += 1
            moveMap("Down", 100)
            
        if keys[pygame.K_RIGHT] and mapX > -maxDist[0]:
            mapX -= 1
            moveMap("Right", 100)
            
        if keys[pygame.K_LEFT] and mapX < 0:
            mapX += 1
            moveMap("Left", 100)
        

    # Run Tools
    setSpawn()
    setOccupied()
    setCollision()
    setEmpty()
    # Update Display
    pygame.display.update()




            