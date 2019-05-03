import pygame
from characters import *


#the score board for each character's values
scoreBoard = {'sorcerer': 20, 'calvary': 15, 'archer': 10, 'infantry': 5}

class Computer(pygame.sprite.Sprite):
    def __init__(self):
        self.character = None

    #change self.character
    def name(self, name):
        self.character = name

    #decide moving range and returns the coordiantes that the characte should move to and the selectedEnemy positions
    def move(self, enemyList, moveRange):
        #see what enemy is within the moving range + attack range
        canReach = []
        #character's moving range
        myRange = moveRange
        #get attack position
        attackRange = self.getAttack(myRange, self.character)
        #getting a list of enemy that the character can attack
        for enemy in enemyList:
            enemyPosition = [enemy.x, enemy.y]
            if enemyPosition in attackRange:
                canReach.append(enemy)
        #if any enemy is in range
        if len(canReach) != 0:
            highScore = 0 #select the enemy with the highest score
            selectedEnmey = None
            for enemy in canReach:
                type = self.getType(enemy)
                score = scoreBoard[type]
                if score > highScore:
                    highScore = score
                    selectedEnmey = enemy
            #decide where the character should move around the selectedEnemy
            x, y = selectedEnmey.x, selectedEnmey.y
            characterAttackRange = self.character.getAttackRange()
            for i in characterAttackRange:
                tempX = x - i[0]
                tempY = y - i[1]
                if [tempX, tempY] in myRange:
                    return tempX, tempY, x, y #move to x, move to y, attack x, attack y
        #if no enemy is in range,stay at the same place
        else:
            return self.character.x, self.character.y, "no", 'no'

    #get the enemy type to determine their score
    def getType(self, enemy):
        if isinstance(enemy, PlayerSorcerer):
            return 'sorcerer'
        elif isinstance(enemy, PlayerCalvary):
            return 'calvary'
        elif isinstance(enemy, PlayerArcher):
            return 'archer'
        elif isinstance(enemy, Player):
            return 'infantry'

    #get the possible attack coordiantes that the character can reach
    def getAttack(self, moveRange, character):
        attackRange = []
        for position in moveRange:
            x, y = position[0], position[1]
            temp = character.getAttackRange()
            for i in temp:
                tempX = i[0] + x
                tempY = i[1] + y
                attackRange.append([tempX, tempY])
        return attackRange

    #sorcerers have different moving rules
    def sorcererMove(self, enemyList, allyList, moveRange):
        # see what enemy or ally is within the moving range + attack range
        canReachEnemy = []
        canReachAlly = []
        # character's moving range
        myRange = moveRange
        # get attack or save position
        attackRange = self.getAttack(myRange, self.character)
        #save allies whose health is below 50 percent first
        for ally in allyList:
            allyPosition = [ally.x, ally.y]
            if allyPosition in attackRange:
                canReachAlly.append(ally)
        # if any ally is in range
        if len(canReachAlly) != 0:
            highScore = 0  # select the enemy with the highest score
            selectedAlly = None
            for ally in canReachAlly:
                #check if an ally has lower than 50% maxHealth
                percentage = ally.health / ally.maxHealth
                if percentage <= 0.5:
                    type = self.getType(ally)
                    score = scoreBoard[type]
                    if score > highScore:
                        highScore = score
                        selectedAlly = ally
            # decide where the character should move around the selectedAlly
            if selectedAlly != None:
                x, y = selectedAlly.x, selectedAlly.y
                characterAttackRange = self.character.getAttackRange()
                for i in characterAttackRange:
                    tempX = x - i[0]
                    tempY = y - i[1]
                    if [tempX, tempY] in myRange:
                        return tempX, tempY, x, y  # move to x, move to y, attack x, attack y
        #if no ally needs to be healed, proceed to choose enemy to attack
        # getting a list of enemy that the character can attack
        for enemy in enemyList:
            enemyPosition = [enemy.x, enemy.y]
            if enemyPosition in attackRange:
                canReachEnemy.append(enemy)
        # if any enemy is in range
        if len(canReachEnemy) != 0:
            highScore = 0  # select the enemy with the highest score
            selectedEnmey = None
            for enemy in canReachEnemy:
                type = self.getType(enemy)
                score = scoreBoard[type]
                if score > highScore:
                    highScore = score
                    selectedEnmey = enemy
            # decide where the character should move around the selectedEnemy
            x, y = selectedEnmey.x, selectedEnmey.y
            characterAttackRange = self.character.getAttackRange()
            for i in characterAttackRange:
                tempX = x - i[0]
                tempY = y - i[1]
                if [tempX, tempY] in myRange:
                    return tempX, tempY, x, y  # move to x, move to y, attack x, attack y
        # if no enemy is in range,stay at the same place
        else:
            return self.character.x, self.character.y, 'no', 'no'