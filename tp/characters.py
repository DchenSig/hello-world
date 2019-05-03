import pygame
from os import path
import random
import copy

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

class Player(pygame.sprite.Sprite):
    def __init__(self, image1, image2, x = 0, y = 0): #image1 is still image and image2 is moving image
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.image1 = image1
        self.image2 = image2

        #health and attack parameters
        self.maxHealth = 130
        self.health = 130
        self.attack = 25
        self.defense = 20

        #selected for attack
        self.selected = False
        self.attackReady = False

        #loading image
        image = pygame.image.load(path.join(imgGroup, self.image1)).convert()
        image_edited = pygame.transform.scale(image, (40, 40))
        self.image = image_edited
        self.image.set_colorkey((255, 255, 255))

        #if a player has finished its move
        self.finish = False

    #drawing a blood rectangle underneath the player
    def bloodvessel(self, screen):
        percentage = self.health / self.maxHealth
        rect = pygame.Rect(self.x * gridSize, (self.y + 1) * gridSize - 5, gridSize * percentage, 5)
        pygame.draw.rect(screen, green, rect, 0)

    #change image of the character to create movement
    def imageChange(self):
        image = pygame.image.load(path.join(imgGroup, self.image2)).convert()
        image_edited = pygame.transform.scale(image, (40, 40))
        self.image = image_edited
        self.image.set_colorkey((255, 255, 255))
    def imageChange2(self):
        image = pygame.image.load(path.join(imgGroup, self.image1)).convert()
        image_edited = pygame.transform.scale(image, (40, 40))
        self.image = image_edited
        self.image.set_colorkey((255, 255, 255))

    #draw attack range
    def attackRange(self):
        range = [[self.x, self.y - 1], [self.x, self.y + 1], [self.x + 1, self.y],
                 [self.x - 1, self.y]]
        return range

    #return attack range for computer moves
    def getAttackRange(self):
        range = [[0, - 1], [0, 1], [1, 0], [- 1, 0]]
        return range


    # change animation when attack
    def attack(self):
        image = pygame.image.load(path.join(imgGroup, 'pangde attackpose')).convert()
        image_edited = pygame.transform.scale(image, (40, 40))
        self.image = image_edited
        self.image.set_colorkey((255, 255, 255))

    #draw move range boxes
    def moveRange(self):
        getMoveRange = [ [self.x + 4, self.y-4], [self.x + 3, self.y-4], [self.x + 2, self.y-4], [self.x + 1, self.y-4],
                         [self.x, self.y-4], [self.x - 1, self.y-4], [self.x - 2, self.y-4], [self.x -3, self.y-4],
                         [self.x - 4, self.y-4], [self.x + 4, self.y-3], [self.x + 3, self.y-3], [self.x + 2, self.y-3],
                         [self.x + 1, self.y-3], [self.x, self.y-3], [self.x - 1, self.y-3], [self.x - 2, self.y-3],
                         [self.x -3, self.y-3], [self.x - 4, self.y-3], [self.x + 4, self.y -2], [self.x + 3, self.y-2],
                         [self.x + 2, self.y-2], [self.x + 1, self.y-2], [self.x, self.y-2], [self.x - 1, self.y-2],
                         [self.x - 2, self.y-2], [self.x -3, self.y-2], [self.x - 4, self.y-2],[self.x + 4, self.y-1],
                         [self.x + 3, self.y-1], [self.x + 2, self.y-1], [self.x + 1, self.y-1], [self.x, self.y-1],
                         [self.x - 1, self.y-1], [self.x - 2, self.y-1], [self.x -3, self.y-1], [self.x - 4, self.y-1],
                         [self.x + 4, self.y], [self.x + 3, self.y], [self.x + 2, self.y], [self.x + 1, self.y],
                         [self.x - 1, self.y], [self.x - 2, self.y], [self.x -3, self.y], [self.x - 4, self.y],
                         [self.x + 4, self.y+1], [self.x + 3, self.y+1], [self.x + 2, self.y+1], [self.x + 1, self.y+1],
                         [self.x, self.y+1], [self.x - 1, self.y+1], [self.x - 2, self.y+1], [self.x -3, self.y+1],
                         [self.x - 4, self.y+1], [self.x + 4, self.y+2], [self.x + 3, self.y+2], [self.x + 2, self.y+2],
                         [self.x + 1, self.y+2], [self.x, self.y+2], [self.x - 1, self.y+2], [self.x - 2, self.y+2],
                         [self.x -3, self.y+2], [self.x - 4, self.y+2], [self.x + 4, self.y+3], [self.x + 3, self.y+3],
                         [self.x + 2, self.y+3], [self.x + 1, self.y+3], [self.x, self.y+3], [self.x - 1, self.y+3],
                         [self.x - 2, self.y+3], [self.x -3, self.y+3], [self.x - 4, self.y+3], [self.x + 4, self.y+ 4],
                         [self.x + 3, self.y+ 4], [self.x + 2, self.y+ 4], [self.x + 1, self.y+ 4], [self.x, self.y+ 4],
                         [self.x - 1, self.y+ 4], [self.x - 2, self.y+ 4], [self.x -3, self.y+ 4],
                         [self.x - 4, self.y+ 4]]
        return getMoveRange

class PlayerArcher(Player):
    def __init__(self, image1, image2, x = 0, y = 0):
        self.x = x
        self.y = y
        self.image1 = image1
        self.image2 = image2

        # health and attack parameters
        self.maxHealth = 80
        self.health = 80
        self.attack = 35
        self.defense = 15

        # selected for attack
        self.selected = False
        self.attackReady = False

        # loading image
        image = pygame.image.load(path.join(imgGroup, self.image1)).convert()
        image_edited = pygame.transform.scale(image, (40, 40))
        self.image = image_edited
        self.image.set_colorkey(white)

        # if a player has finished its move
        self.finish = False

    # draw attack range
    def attackRange(self):
        range = [[self.x, self.y - 6], [self.x, self.y + 6], [self.x + 6, self.y],
                 [self.x - 6, self.y]]
        return range

    def getAttackRange(self):
        range = [[0, - 6], [0, 6], [6, 0], [- 6, 0]]
        return range

class PlayerCalvary(Player):
    def __init__(self, image1, image2, x = 0, y = 0):
        self.x = x
        self.y = y
        self.image1 = image1
        self.image2 = image2

        # health and attack parameters
        self.maxHealth = 100
        self.health = 100
        self.attack = 50
        self.defense = 15

        # selected for attack
        self.selected = False
        self.attackReady = False

        # loading image
        image = pygame.image.load(path.join(imgGroup, self.image1)).convert()
        image_edited = pygame.transform.scale(image, (40, 40))
        self.image = image_edited
        self.image.set_colorkey(white)

        # if a player has finished its move
        self.finish = False

    # draw attack range
    def attackRange(self):
        range = [[self.x, self.y - 1], [self.x + 1, self.y + 1], [self.x, self.y + 1], [self.x + 1, self.y - 1],
                 [self.x + 1, self.y], [self.x -1 , self.y - 1], [self.x - 1, self.y + 1],[self.x - 1, self.y]]
        return range
    def getAttackRange(self):
        range = [[0, - 1], [0, 1], [1, 0], [- 1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        return range

    #draw move range boxes
    def moveRange(self):
        getMoveRange = [[self.x + 5, self.y-5], [self.x + 4, self.y-5], [self.x + 3, self.y - 5],
                        [self.x + 2, self.y- 5], [self.x + 1, self.y-5], [self.x, self.y-5], [self.x - 1, self.y-5],
                        [self.x - 2, self.y-5], [self.x - 3, self.y-5], [self.x - 4, self.y-5], [self.x - 5, self.y-5],
                         [self.x + 3, self.y-4], [self.x + 2, self.y-4], [self.x + 1, self.y-4], [self.x, self.y-4],
                        [self.x - 1, self.y-4], [self.x - 2, self.y-4], [self.x -3, self.y-4], [self.x - 4, self.y-4],
                        [self.x + 5, self.y-4], [self.x - 5, self.y-4], [self.x + 4, self.y-3], [self.x + 3, self.y-3],
                        [self.x + 2, self.y-3], [self.x + 1, self.y-3], [self.x, self.y-3], [self.x - 1, self.y-3],
                        [self.x - 2, self.y-3], [self.x -3, self.y-3], [self.x - 4, self.y-3], [self.x + 5, self.y-3],
                        [self.x - 5, self.y-3], [self.x + 4, self.y -2], [self.x + 3, self.y-2], [self.x + 2, self.y-2],
                        [self.x + 1, self.y-2], [self.x, self.y-2], [self.x - 1, self.y-2], [self.x - 2, self.y-2],
                        [self.x -3, self.y-2], [self.x - 4, self.y-2],[self.x + 5, self.y-2], [self.x - 5, self.y-2],
                        [self.x + 4, self.y-1], [self.x + 3, self.y-1], [self.x + 2, self.y-1], [self.x + 1, self.y-1],
                        [self.x, self.y-1], [self.x - 1, self.y-1], [self.x - 2, self.y-1], [self.x -3, self.y-1],
                        [self.x - 4, self.y-1], [self.x + 5, self.y-1], [self.x - 5, self.y-1], [self.x + 4, self.y],
                        [self.x + 3, self.y], [self.x + 2, self.y], [self.x + 1, self.y], [self.x - 1, self.y],
                        [self.x - 2, self.y], [self.x -3, self.y], [self.x - 4, self.y], [self.x + 5, self.y],
                        [self.x - 5, self.y], [self.x + 4, self.y+1], [self.x + 3, self.y+1], [self.x + 2, self.y+1],
                        [self.x + 1, self.y+1], [self.x, self.y+1], [self.x - 1, self.y+1], [self.x - 2, self.y+1],
                        [self.x -3, self.y+1], [self.x - 4, self.y+1],[self.x + 5, self.y + 1],[self.x - 5, self.y + 1],
                        [self.x + 4, self.y+2], [self.x + 3, self.y+2], [self.x + 2, self.y+2], [self.x + 1, self.y+2],
                        [self.x, self.y+2], [self.x - 1, self.y+2], [self.x - 2, self.y+2], [self.x -3, self.y+2],
                        [self.x - 4, self.y+2], [self.x + 5, self.y + 2], [self.x - 5, self.y + 2],
                        [self.x + 4, self.y+3], [self.x + 3, self.y+3], [self.x + 2, self.y+3], [self.x + 1, self.y+3],
                        [self.x, self.y+3], [self.x - 1, self.y+3], [self.x - 2, self.y+3], [self.x -3, self.y+3],
                        [self.x - 4, self.y+3], [self.x + 5, self.y + 3], [self.x - 5, self.y + 3],
                        [self.x + 4, self.y+ 4], [self.x + 3, self.y+ 4], [self.x + 2, self.y+ 4],
                        [self.x + 1, self.y+ 4], [self.x, self.y+ 4], [self.x - 1, self.y+ 4], [self.x - 2, self.y+ 4],
                        [self.x -3, self.y+ 4], [self.x - 4, self.y+ 4], [self.x + 5, self.y + 4],
                        [self.x - 5, self.y + 4], [self.x + 4, self.y+ 5], [self.x + 3, self.y+ 5],
                        [self.x + 2, self.y+ 5], [self.x + 1, self.y+ 5], [self.x, self.y+ 5], [self.x - 1, self.y+ 5],
                        [self.x - 2, self.y+ 5], [self.x -3, self.y+ 5], [self.x - 4, self.y+ 5],
                        [self.x + 5, self.y + 5], [self.x - 5, self.y + 5],[self.x + 4, self.y-4]]
        return getMoveRange

class PlayerSorcerer(Player):
    def __init__(self, image1, image2, x = 0, y = 0):
        self.x = x
        self.y = y
        self.image1 = image1
        self.image2 = image2

        # health and attack parameters
        self.defense = 10
        self.maxHealth = 60
        self.health = 60
        self.maxMagic = 100
        self.magic = 100
        self.spellCost = 10

        #spell damage
        self.spell = random.randint(10, 20)
        self.heal = random.randint(10, 20)

        # selected for attack
        self.selected = False
        self.attackReady = False

        # loading image
        image = pygame.image.load(path.join(imgGroup, self.image1)).convert()
        image_edited = pygame.transform.scale(image, (40, 40))
        self.image = image_edited
        self.image.set_colorkey(white)

        # if a player has finished its move
        self.finish = False

    #determine if the sorcerer still has magic left for a spell
    def canSpell(self):
        left = self.magic - self.spellCost
        if left >= 0:
            return True
        else:
            return False

    # drawing a blood rectangle and a magic rectangle underneath the player
    def bloodvessel(self, screen):
        #blood vessel
        percentage = self.health / self.maxHealth
        rect = pygame.Rect(self.x * gridSize, (self.y + 1) * gridSize - 5, gridSize * percentage, 5)
        pygame.draw.rect(screen, green, rect, 0)

        #magic vessel
        percentage2 = self.magic / self.maxMagic
        rect = pygame.Rect(self.x * gridSize, (self.y + 1) * gridSize - 10, gridSize * percentage2, 5)
        pygame.draw.rect(screen, blue, rect, 0)

    def attackRange(self):
        range = [[self.x + 5, self.y-5], [self.x + 4, self.y-5], [self.x + 3, self.y - 5],
                        [self.x + 2, self.y- 5], [self.x + 1, self.y-5], [self.x, self.y-5], [self.x - 1, self.y-5],
                        [self.x - 2, self.y-5], [self.x - 3, self.y-5], [self.x - 4, self.y-5], [self.x - 5, self.y-5],
                         [self.x + 3, self.y-4], [self.x + 2, self.y-4], [self.x + 1, self.y-4], [self.x, self.y-4],
                        [self.x - 1, self.y-4], [self.x - 2, self.y-4], [self.x -3, self.y-4], [self.x - 4, self.y-4],
                        [self.x + 5, self.y-4], [self.x - 5, self.y-4], [self.x + 4, self.y-3], [self.x + 3, self.y-3],
                        [self.x + 2, self.y-3], [self.x + 1, self.y-3], [self.x, self.y-3], [self.x - 1, self.y-3],
                        [self.x - 2, self.y-3], [self.x -3, self.y-3], [self.x - 4, self.y-3], [self.x + 5, self.y-3],
                        [self.x - 5, self.y-3], [self.x + 4, self.y -2], [self.x + 3, self.y-2], [self.x + 2, self.y-2],
                        [self.x + 1, self.y-2], [self.x, self.y-2], [self.x - 1, self.y-2], [self.x - 2, self.y-2],
                        [self.x -3, self.y-2], [self.x - 4, self.y-2],[self.x + 5, self.y-2], [self.x - 5, self.y-2],
                        [self.x + 4, self.y-1], [self.x + 3, self.y-1], [self.x + 2, self.y-1], [self.x + 1, self.y-1],
                        [self.x, self.y-1], [self.x - 1, self.y-1], [self.x - 2, self.y-1], [self.x -3, self.y-1],
                        [self.x - 4, self.y-1], [self.x + 5, self.y-1], [self.x - 5, self.y-1], [self.x + 4, self.y],
                        [self.x + 3, self.y], [self.x + 2, self.y], [self.x + 1, self.y], [self.x - 1, self.y],
                        [self.x - 2, self.y], [self.x -3, self.y], [self.x - 4, self.y], [self.x + 5, self.y],
                        [self.x - 5, self.y], [self.x + 4, self.y+1], [self.x + 3, self.y+1], [self.x + 2, self.y+1],
                        [self.x + 1, self.y+1], [self.x, self.y+1], [self.x - 1, self.y+1], [self.x - 2, self.y+1],
                        [self.x -3, self.y+1], [self.x - 4, self.y+1],[self.x + 5, self.y + 1],[self.x - 5, self.y + 1],
                        [self.x + 4, self.y+2], [self.x + 3, self.y+2], [self.x + 2, self.y+2], [self.x + 1, self.y+2],
                        [self.x, self.y+2], [self.x - 1, self.y+2], [self.x - 2, self.y+2], [self.x -3, self.y+2],
                        [self.x - 4, self.y+2], [self.x + 5, self.y + 2], [self.x - 5, self.y + 2],
                        [self.x + 4, self.y+3], [self.x + 3, self.y+3], [self.x + 2, self.y+3], [self.x + 1, self.y+3],
                        [self.x, self.y+3], [self.x - 1, self.y+3], [self.x - 2, self.y+3], [self.x -3, self.y+3],
                        [self.x - 4, self.y+3], [self.x + 5, self.y + 3], [self.x - 5, self.y + 3],
                        [self.x + 4, self.y+ 4], [self.x + 3, self.y+ 4], [self.x + 2, self.y+ 4],
                        [self.x + 1, self.y+ 4], [self.x, self.y+ 4], [self.x - 1, self.y+ 4], [self.x - 2, self.y+ 4],
                        [self.x -3, self.y+ 4], [self.x - 4, self.y+ 4], [self.x + 5, self.y + 4],
                        [self.x - 5, self.y + 4], [self.x + 4, self.y+ 5], [self.x + 3, self.y+ 5],
                        [self.x + 2, self.y+ 5], [self.x + 1, self.y+ 5], [self.x, self.y+ 5], [self.x - 1, self.y+ 5],
                        [self.x - 2, self.y+ 5], [self.x -3, self.y+ 5], [self.x - 4, self.y+ 5],
                        [self.x + 5, self.y + 5], [self.x - 5, self.y + 5],[self.x + 4, self.y-4]]
        return range
    def getAttackRange(self):
        range = copy.deepcopy(self.attackRange())
        for i in range:
            i[0] -= self.x
            i[1] -= self.y
        return range


