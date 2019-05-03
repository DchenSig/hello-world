import pygame
from os import path

#collection of images
imgGroup = path.join(path.dirname(__file__), 'images')

#borrowed parameter from __init__
gridSize = 40

#color
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

class Map(pygame.sprite.Sprite):
    def __init__(self):
        #map image
        map = pygame.image.load(path.join(imgGroup, 'map.jpg')).convert()
        image_edited = pygame.transform.scale(map, (960, 960))
        self.picture = image_edited

        #setting up grid parameter
        self.gridSize = 40  # fixed grid size (also copied into the character file, under attackRange
        self.screenWidth = 960
        self.screenHeight = 960
        self.numRow = self.screenHeight // self.gridSize
        self.numCol = self.screenWidth // self.gridSize

    #draw the map
    def draw(self, screen):
        screen.blit(self.picture, (0, 0))

        '''
        #uncomment the following code to draw a grid to calibrate
        for row in range(self.numRow):
            for col in range(self.numCol):
                Rect = pygame.Rect(row * self.gridSize, col * self.gridSize, self.gridSize, self.gridSize)
                pygame.draw.rect(screen, (255, 0, 0), Rect, 1)
        '''

    #set up terrain characters
    def terrain(self):
        movement = [([True] * self.numRow) for col in range(self.numCol)]
        #set up unmovable terrain by creating a 2d list and setting unmovalbe terrain's values as False
        #first num is row number and the following is col num
        fences = [[3, 13, 14, 15, 16],
                  [6, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20,21],
                  [7, 8, 21],
                  [8, 8, 21],
                  [9, 8, 21],
                  [10, 8, 21],
                  [13, 8, 21],
                  [14, 8, 21],
                  [15, 8, 21],
                  [16, 8, 21],
                  [17, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20 ,21],
                  [21, 13, 14, 15, 16]]
        #correcting counting error
        for i in range(len(fences)):
            for j in range(len(fences[i])):
                fences[i][j] -= 1

        for fence in fences:
            col = fence[0]
            for place in range(1, len(fence)):
                row = fence[place]
                movement[row][col] = False
        return movement

    #castles and tents can heal soilders
    def castle(self):
        specialTerrain = [[10, 12], [11, 12], [13, 19], [14, 19], [15, 19]] # col, row
        return specialTerrain

    #forrest coordinates
    def forrest(self):
        forrest = [[23, 2], [23, 3], [23, 4], [23, 5], [23, 6], [23, 7], [23, 8],
                   [22, 2], [22, 3], [22, 4], [22, 5], [22, 6], [22, 7],
                   [21, 3], [21, 4], [21, 5], [21, 6],
                   [20, 4],
                   [0, 18],[0, 19], [0, 20], [0, 21], [0, 22], [0,23],
                   [1, 19], [1, 20], [1, 21], [1, 22], [1,23],
                   [2, 22], [2, 23], [3, 23]]
        return forrest




