'''This game is created by Zixi Chen for the term project of 15-112 at CMU.'''
import pygame
from characters import *
from map_n_features import *
from AI import *
from textwrap import fill

'''The following framework is copied from the pygame manul by Lukas Peraza'''

#screen size
screenSize = 960

#collection of music
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
musGroup = path.join(path.dirname(__file__), 'sound')
pygame.mixer.music.load(path.join(musGroup, 'Background.mp3'))


class PygameGame(object):
    def init(self):
        #start page
        self.startPage = True

        #controls when the game stops
        self.gameOver = False
        self.playing = True

        #the winner
        self.winner = None

        #pause game
        self.pause = True

        #computer AI player
        self.computer = Computer()

        #map paramters
        self.map = Map()

        #moving position white box parameters
        self.gridSize = 40 # fixed grid size (also copied into the character file, under attackRange
        self.screenWidth = 600
        self.screenHeight = 400
        self.numRow = self.screenHeight // self.gridSize
        self.numCol = self.screenWidth // self.gridSize

        #moving box
        self.boxCol = 0
        self.boxRow = 0
        self.boxColor = white

        #enemy characters
        self.enemy1 = Player('guanyu still.png', 'guanyu walk.png', 12, 10)
        self.enemy2 = PlayerArcher('archer2 still.png', 'archer2 walk.png', 13, 10)
        self.enemy3 = PlayerCalvary('machao still.png', 'machao walk.png', 12, 11)
        self.enemy4 = PlayerSorcerer('zhugeliang still.png', 'zhugeliang walk.png', 15, 10)
        self.enemy5 = Player('guanyu still.png', 'guanyu walk.png', 12, 13)
        self.enemy6 = PlayerCalvary('machao still.png', 'machao walk.png', 12, 12)
        self.enemy7 = PlayerArcher('archer2 still.png', 'archer2 walk.png', 13, 11)

        #player characters
        self.player1 = Player('pangde still.png', 'pangde walk.png', 1, 12)
        self.player2 = Player('pangde still.png', 'pangde walk.png', 1, 9)
        self.player3 = PlayerArcher('archer still.png', 'archer walk.png', 0, 11)
        self.player4 = PlayerArcher('archer still.png', 'archer walk.png', 0, 10)
        self.player5 = PlayerCalvary('xiahoudun still.png', 'xiahoudun walk.png', 1, 10)
        self.player6 = PlayerCalvary('xiahoudun still.png', 'xiahoudun walk.png', 1, 11)
        self.player7 = PlayerSorcerer('simayi still.png', 'simayi walk.png', 0, 12)
        self.alternate = True

        #player and enemy list
        self.player = []
        self.player.append(self.player1)
        self.player.append(self.player2)
        self.player.append(self.player3)
        self.player.append(self.player4)
        self.player.append(self.player5)
        self.player.append(self.player6)
        self.player.append(self.player7)
        self.enemy = []
        self.enemy.append(self.enemy1)
        self.enemy.append(self.enemy2)
        self.enemy.append(self.enemy3)
        self.enemy.append(self.enemy4)
        self.enemy.append(self.enemy5)
        self.enemy.append(self.enemy6)
        self.enemy.append(self.enemy7)
        self.character = []

        #character position list
        self.position = dict()

        #attack red boxes coordinates shared by both players and enemies
        self.player1Selected = {self.player1: False, self.enemy1: False}
        self.attackReady = False
        self. attackBoxes = []

        #deciding whose turn it is
        self.turn = 'player'

        #if user has finished moving all his character
        self.playerFinished = []
        self.enemyFinished = []

        #keeps time
        self.count = 0

        #selected player
        self.characterSelected = None

        #activates helper interface
        self.help = False

    # determine character movement range
    def moveable(self, character):
        terrain = self.map.terrain()
        movement = []
        # unmovable terrain detection
        for move in character:
            row = move[0]
            col = move[1]
            if terrain[row][col]:
                movement.append(move)
        # character position overlap detection
        for move in movement:
            row = move[0]
            col = move[1]
            place = [row, col]
            if place in self.position.values():
                movement.remove(move)
            #removing positions that are off-screen
            if row < 0 or col < 0:
                movement.remove(move)
        return movement

    # if a move clicked on the map is legit
    def moveLegit(self, character, x, y):
        terrain = self.map.terrain()
        if not terrain[x][y]:
            return False
        elif character.x == x and character.y == y:
            return True
        elif [x, y] in self.position.values():
            return False
        elif [x, y] in character.moveRange():
            return True
        else:
            return False

    #determing whose turn it is
    def getTurn(self):
        status = []
        if self.turn == 'player':
            for player in self.player:
                status.append(player.finish)
            if False in status:
                self.turn = 'player'
            else:
                self.turn = 'enemy'
        elif self.turn == 'enemy':
            for enemy in self.enemy:
                status.append(enemy.finish)
            if not (False in status):
                self.turn = 'player'
                #resetting all characters to not moved
                for character in self.character:
                    character.finish = False

    # the interface for when the game is over; shows the winner
    def gameOverScreen(self, screen, winner):
        # a red box in the middle of the screen
        rect = pygame.Rect(screenSize * 0.25, screenSize * 0.25, screenSize / 2, screenSize * 0.25)
        pygame.draw.rect(screen, red, rect, 0)

        #display winner
        font = pygame.font.SysFont(None, 30)
        font2 = pygame.font.SysFont(None, 30)
        screen_text = font.render(winner, True, black)
        screen_text_2 = font2.render('Press P to start a new game', True, black)
        screen.blit(screen_text, [screenSize / 3 + 40, screenSize / 3 - 20])
        screen.blit(screen_text_2, [screenSize / 3 + 20, screenSize / 3 + 50])

    #create help interface
    def helpButton(self, screen):
        image = pygame.image.load(path.join(imgGroup, "helpButton.png")).convert()
        image_edited = pygame.transform.scale(image, (self.gridSize * 2, self.gridSize))
        image_edited.set_colorkey(white)
        screen.blit(image_edited, (0, 0))

    #create help screen
    def helpScreen(self, screen):
        image = pygame.image.load(path.join(imgGroup, 'helpPageNew.jpg')).convert()
        image_edited = pygame.transform.scale(image, (screenSize, screenSize))
        screen.blit(image_edited, (0, 0))

    def mousePressed(self, x, y):
        # how many boxes the mouse is at
        xBox = x // self.gridSize
        yBox = y // self.gridSize
        #when the user clicks on the help button, display the help interface and pause the game
        if xBox == 0 or xBox == 1 or xBox == 2:
            if yBox == 1 or yBox == 0:
               self.help = True
               self.pause = True

        #avoids user accidently moves characters whent the help interface is on
        if not self.pause:
            #controls character movement, attack and updates if the character has finished moving
            if self.characterSelected == None:
                for character in self.character:
                    #first click to select any character
                    if not character.selected:
                        if character.x == xBox and character.y == yBox:
                            if self.turn == 'player' and (character in self.player): #determining whose turn it is
                                if not character.finish: # if the character has not moved yet
                                    character.selected = True
                                    break
                            elif self.turn == 'enemy' and (character in self.enemy):
                                if not character.finish:
                                    character.selected = True
                                    break
                    #second click to move character
                    else:
                        if self.moveLegit(character, xBox, yBox):
                            character.x = xBox
                            character.y = yBox
                            character.selected = False
                            character.attackReady = True
                            self.characterSelected = character
                            self.attackBoxes = character.attackRange()
                            break
            #third click to attack
            else:
                coordinates = self.characterSelected.attackRange()
                if not isinstance(self.characterSelected, PlayerSorcerer): #sorcerers have different attacks than others
                    if [xBox, yBox] in coordinates:
                        for character in self.character:
                            if character.x == xBox and character.y == yBox:
                                damage = self.characterSelected.attack - character.defense
                                character.health -= damage
                                break
                else:
                    if [xBox, yBox] in coordinates:
                        for character in self.character:
                            if character.x == xBox and character.y == yBox:
                                if self.characterSelected.canSpell: # a sorcerer can only use spell when it has magic left
                                    #returns true if selected character is in player side
                                    selectedSide = self.characterSelected in self.player
                                    if self.turn == 'player':
                                        if selectedSide: #means the selected character is in player's side
                                            if character in self.player: #means that character attacked is on the same side
                                                temp = character.health + self.characterSelected.heal
                                                if temp >= character.maxHealth: #health cannot exceed maximum health
                                                    character.health = character.maxHealth
                                                else:
                                                    character.health = temp
                                            else: #means that character attacked is an enemy
                                                #extra damage when the enemy is in forrest
                                                x, y = character.x, character.y
                                                forrest = self.map.forrest()
                                                if [x, y] in forrest:
                                                    damage = self.characterSelected.spell + 5
                                                    character.health -= damage
                                                else:
                                                    damage = self.characterSelected.spell
                                                    character.health -= damage
                                            self.characterSelected.magic -= self.characterSelected.spellCost
                                    elif self.turn == 'enemy':
                                        if not selectedSide: #means the selected character is in enemy's side
                                            if character not in self.player:
                                                temp = character.health + self.characterSelected.heal
                                                if temp >= character.maxHealth:
                                                    character.health = character.maxHealth
                                                else:
                                                    character.health = temp
                                            else:
                                                x, y = character.x, character.y
                                                forrest = self.map.forrest()
                                                if [x, y] in forrest:
                                                    damage = self.characterSelected.spell + 5
                                                    character.health -= damage
                                                else:
                                                    damage = self.characterSelected.spell
                                                    character.health -= damage
                                            self.characterSelected.magic -= self.characterSelected.spellCost
                self.attackBoxes = []
                self.characterSelected.finish = True
                self.characterSelected = None

    def mouseMotion(self, x, y):
        self.boxRow = x // self.gridSize
        self.boxCol = y // self.gridSize

    def keyPressed(self, keyCode, modifier):
        #when the game is over, reset the game
        if self.gameOver:
            if keyCode == pygame.K_p:
                self.gameOver = False
                self.init()

        #when the help interface is on, press to get rid of the help interface
        if self.help:
            if keyCode == pygame.K_RETURN:
                self.help = False
                self.pause = False

        #start the game
        if keyCode == pygame.K_SPACE:
            self.startPage = False
            self.pause = False

    def timerFired(self, dt):
        '''The order of the following code matters'''
        # remove any character whose health is below 0
        for player in self.player:
            if player.health <= 0:
                self.player.remove(player)
                self.position.pop(player, None)
        for enemy in self.enemy:
            if enemy.health <= 0:
                self.enemy.remove(enemy)
                self.position.pop(enemy, None)

        #composing real-time player positions
        self.character = self.player + self.enemy

        #determining whose turn it is
        self.getTurn()

        #tracking all characters positions
        for character in self.character:
            x, y = character.x, character.y
            self.position[character] = [x, y]

        #creating character animation
        self.count += 1
        if (self.count % 25) == 0:
            if self.alternate:
                for character in self.character:
                    if not character.finish:
                        character.imageChange()
                self.alternate = not self.alternate
            else:
                for character in self.character:
                    if not character.finish:
                        character.imageChange2()
                self.alternate = not self.alternate

        #computer moves
        if self.turn == 'enemy':
            for enemy in self.enemy:
                #select enemy for the computer to move around
                self.computer.name(enemy)
                #creates moveRange for the character
                moveRange = self.moveable(enemy.moveRange())
                #sorcerer has different moves
                if isinstance(enemy, PlayerSorcerer):
                    moveX, moveY, attackX, attackY = self.computer.sorcererMove(self.player, self.enemy, moveRange)
                else:
                    moveX, moveY, attackX, attackY = self.computer.move(self.player, moveRange)
                #when character has to stay put
                if attackX == 'no':
                    attackX = moveX
                    attackY = moveY
                characterX = self.computer.character.x * self.gridSize
                characterY = self.computer.character.y * self.gridSize
                moveX = moveX * self.gridSize
                moveY = moveY * self.gridSize
                attackX = attackX * self.gridSize
                attackY = attackY * self.gridSize
                self.mousePressed(characterX, characterY) #select the character
                self.mousePressed(moveX, moveY) #move the character
                self.mousePressed(attackX, attackY) #attack the enemy
                # updating characters positions again since this function was outside this if statement
                for character in self.character:
                    x, y = character.x, character.y
                    self.position[character] = [x, y]

        #looping through the player and enemy list. If either list is empty, end the game
        if len(self.player) == 0:
            self.gameOver = True
            self.winner = "The Computer Has Won!"
        elif len(self.enemy) == 0:
            self.gameOver = True
            self.winner = "You Have Won!"

    def redrawAll(self, screen):
        # draw character movement blue boxes
        for character in self.character:
            if character.selected:
                movement = self.moveable(character.moveRange())
                for move in movement:
                    row = move[0]
                    col = move[1]
                    rect = pygame.Rect(row * self.gridSize, col * self.gridSize, self.gridSize, self.gridSize)
                    pygame.draw.rect(screen, blue, rect, 0)

        # drawing red attack boxes
        for x, y in self.attackBoxes:
            Rect = pygame.Rect(x * self.gridSize, y * self.gridSize, self.gridSize, self.gridSize)
            pygame.draw.rect(screen, (255, 0, 0), Rect, 0)

        #creating moving white box that traces the movement of the mouse
        Rect = pygame.Rect(self.boxRow * self.gridSize, self.boxCol * self.gridSize, self.gridSize, self.gridSize)
        pygame.draw.rect(screen, self.boxColor, Rect, 1)

        #drawing characters
        for player in self.player:
            screen.blit(player.image, (player.x * self.gridSize, player.y * self.gridSize))
        for enemy in self.enemy:
            screen.blit(enemy.image, (enemy.x * self.gridSize, enemy.y * self.gridSize))

        #draw character blood level
        for playerBlood in self.player:
            playerBlood.bloodvessel(screen)
        for enemyBlood in self.enemy:
            enemyBlood.bloodvessel(screen)

        #display the ending interface when the game ends
        if self.gameOver:
            self.gameOverScreen(screen, self.winner)

        #draw the help button
        self.helpButton(screen)

        #draw the help interface
        if self.help:
            self.helpScreen(screen)

        #display start page
        if self.startPage:
            startPage = pygame.image.load(path.join(imgGroup, 'FinalStartPage.jpg')).convert()
            image_edited = pygame.transform.scale(startPage, (screenSize, screenSize))
            screen.blit(image_edited, (0, 0))


    def __init__(self, width=screenSize, height=screenSize, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (0, 0, 0)
        pygame.init()

    def run(self):
        #play background music
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()

        while self.playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    self.playing = False
            screen.fill(self.bgColor)
            #screen.blit(background_image_editied, (0, 0))
            self.map.draw(screen)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()
        exit()

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()