import random, os, pygame, sys
from pygame.locals import *

GAME_WIDTH = 1250
GAME_HEIGHT = 750
LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT
Q = pygame.K_q

class GameCharacter(object):
    def __init(self):
        self.hspeed = 0
        self.vspeed = 0
    
    def isGoingLeft(self):
        return self.hspeed < 0
    
    def isGoingRight(self):
        return self.hspeed > 0
    
    def isAtEdge(self):
        return (self.isAtLeftEdge() or self.isAtRightEdge())
    
    def isAtLeftEdge(self):
        return (self.rect.left < 0)
    
    def isAtRightEdge(self):
        return (self.rect.right > GAME_WIDTH)
    
    def isAtBottomEdge(self):
        return (self.rect.bottom >= GAME_HEIGHT)
    
    def turnAround(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.hspeed = -self.hspeed
    
    def hasCollidedWith(self, otherObject):
        return self.rect.colliderect(otherObject.rect)
    
    def setHSpeed(self, horizontalSpeed):
        self.setSpeed(horizontalSpeed, None)


    def setVSpeed(self, verticalSpeed):
        self.setSpeed(None, verticalSpeed)


    def setSpeed(self, horizontalSpeed, verticalSpeed):
        if(horizontalSpeed):
            self.hspeed = horizontalSpeed

        if(verticalSpeed):
            self.vspeed = verticalSpeed

class Snoopy(GameCharacter):
    def __init__(self, game):
        # Game to which this snoopy belongs to
        self.game = game

        # Get snoopy's image
        self.image = pygame.image.load(os.path.join("assets/images", "snoopy.png"))

        # Resize the huge snoopy
        self.rect = self.image.get_rect()
        height = self.rect.height
        width = self.rect.width
        self.image = pygame.transform.scale(self.image, (width/2, height/2))

        # Reset the rect to the resized image's rect
        self.rect = self.image.get_rect()

        # Position him at the bottom of the game screen
        self.rect.bottom = GAME_HEIGHT

        self.hspeed = 10
        self.bobbingAmplitude = 2
        self.bobbingSpeed = self.bobbingAmplitude*2

    def move(self, keys):
        if keys and (self.isGoingLeft() and keys[RIGHT_KEY] or self.isGoingRight() and keys[LEFT_KEY]):
            self.turnAround()

        self.keepFlying()

    def keepFlying(self):
        bob = random.randint(1,3)

        newRect = self.rect.move([self.hspeed, self.bobbingSpeed])
        if bob == 3:
            newRect = self.rect.move([self.hspeed, self.bobbingSpeed])
            self.bobbingSpeed = -self.bobbingSpeed
        else:
            newRect = self.rect.move([self.hspeed,0])

        self.rect = newRect

        if(self.isAtEdge()):
            self.turnAround()

class Woodstock(GameCharacter):
    def __init__(self, game):
        # Game to which this snoopy belongs to
        self.game = game

        # The woodstock image
        self.image = pygame.image.load(os.path.join("assets/images", "woodstock.png"))

        # Resize the woodstock
        self.rect = self.image.get_rect()
        height = self.rect.height
        width = self.rect.width
        self.image = pygame.transform.scale(self.image, (width/5, height/5))

        # Get the woodstock rect
        self.rect = self.image.get_rect()

        # Get a random x axis location
        width = self.rect.width
        xcoordinate = random.randint(width/2, GAME_WIDTH - width/2)

        # Set the woodstock to the top of the game at the x location
        self.rect.top = 0
        self.rect.centerx = xcoordinate

        # Set default vertical speed (arbitrarily decided)
        self.vspeed = 5

        # hspeed: horizontal speed
        self.hspeed = random.randint(-15,15)

    
    def move(self):
        
        self.rect = self.rect.move([self.hspeed, self.vspeed])
        
        if(self.isAtEdge()):
            self.turnAround()

class Game(object):
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode([width, height])
        
        # Game Title
        pygame.display.set_caption("Catch the woodstocks!")
        
        # Initialize snoopy and the woodstocks
        self.snoopy = Snoopy(self)
        self.woodstocks = self.createWoodstocks()

    def run(self):
        # Define colors
        black = (0,0,0)

        runGame = True
        while runGame:

            self.resetDeadWoodstocks()

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT or keys and keys[Q]:
                    runGame = False
                    break

            self.moveWoodstocks()
            self.snoopy.move(keys)
            
            self.draw()
            pygame.display.update()

    def createWoodstocks(self):
        # There is one woodstock for each speed
        speeds = [4, 8, 12, 16]
        woodstocks = []
        
        for speed in speeds:
            w = Woodstock(self)
            w.setVSpeed(speed)
            woodstocks += [w]

        return woodstocks

    #	Checks if any of the woodstocks have collided with snoopy
    def resetDeadWoodstocks(self):
        for w in self.woodstocks:
            # Woodstock is dead if he hits the bottom or if Snoopy catches him
            if w.isAtBottomEdge() or w.hasCollidedWith(self.snoopy):
                vspeed = w.vspeed
                self.woodstocks.remove(w)
                w = Woodstock(self)
                w.setVSpeed = vspeed
                self.woodstocks.append(w)
                

    def moveWoodstocks(self):
        for w in self.woodstocks:
            w.move()

    def draw(self):
        self.drawSky()
        for w in self.woodstocks:
            self.screen.blit(w.image, w.rect)
        self.screen.blit(self.snoopy.image, self.snoopy.rect)

        pygame.display.update()

    def drawSky(self):
        skyimage = pygame.image.load(os.path.join("assets/images/sky", "sky1.jpg"))
        skyimage = pygame.transform.scale(skyimage, (GAME_WIDTH, GAME_HEIGHT))
        skyrect = skyimage.get_rect()
        self.screen.blit(skyimage, skyrect)

game = Game(GAME_WIDTH, GAME_HEIGHT)
game.run()