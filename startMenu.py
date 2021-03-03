import pygame, os, pygame_textinput
from button import Button

pygame.init()

# Setup screen
w, h = 500, 500
WIN = pygame.display.set_mode((w, h))

# Load images
fileDir = os.path.dirname(__file__)
assetDir = os.path.join(fileDir, 'assets')
menuImg = pygame.image.load(os.path.join(assetDir, "start_menu.png"))
startImg = pygame.image.load(os.path.join(assetDir, "play_button.png"))
loadImg = pygame.image.load(os.path.join(assetDir, "load_button.png"))

# Set clock and buttons
clock = pygame.time.Clock()
startButton = Button(startImg, 164, 318, 171, 68)
loadButton = Button(loadImg, 164, 406, 171, 68)

# setup text inputs
mapName = pygame_textinput.TextInput()
widthText = pygame_textinput.TextInput()
heightText = pygame_textinput.TextInput()

# Toggles
mapTextToggle = False
widthTextToggle = False
heightTextToggle = False
buttonToggle = False
loadToggle = False
# Run Loop
startMenu = True

while startMenu:
    # Would be redraw function (taken out bc it made the input text flicker)
    # Blit the prompts
    WIN.blit(menuImg, (0, 0))
    # Blit the button to start the map editor
    startButton.drawButton(WIN)
    loadButton.drawButton(WIN)
    # Mouse Position
    pos = pygame.mouse.get_pos()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            startMenu = False
            pygame.quit()
            quit()

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Map Text
        if pos[0] > 50 and pos[0] < 455:
            if pos[1] > 198 and pos[1] < 222:    
                mapTextToggle = True
                widthTextToggle = False
                heightTextToggle = False
        
        # Width Text
        if pos[0] > 123 and pos[0] < 213:
            if pos[1] > 270 and pos[1] < 292:    
                widthTextToggle = True
                mapTextToggle = False
                heightTextToggle = False

        # Height Text
        if pos[0] > 277 and pos[0] < 385:
            if pos[1] > 270 and pos[1] < 292:    
                heightTextToggle = True
                mapTextToggle = False
                widthTextToggle = False
        
        # If Button Press
        if startButton.mouseOver():
            buttonToggle = True
        if loadButton.mouseOver():
            loadToggle = True

    # Update input_text
    if mapTextToggle:   
        mapName.update(events)
        
    if widthTextToggle:
        widthText.update(events)
    
    if heightTextToggle:
        heightText.update(events)

    if buttonToggle:
        name = mapName.get_text()
        width = int(widthText.get_text())
        height = int(heightText.get_text())
        #print(name, width, height)
        startMenu = False   

    if loadToggle:
        name = mapName.get_text()
        startMenu = False  
    # Blit its surface onto the screen
    WIN.blit(mapName.get_surface(), (52, 198))
    WIN.blit(widthText.get_surface(), (124, 272))
    WIN.blit(heightText.get_surface(), (279, 272))
    pygame.display.update()
    clock.tick(30)
        