import random, os, pygame, sys
from pygame.locals import *

GAME_WIDTH = 1250
GAME_HEIGHT = 750
LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

class Snoopy:
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
        
        self.speed = 10

    def move(self, keys):
        if keys and (self.isGoingLeft() and keys[RIGHT_KEY] or self.isGoingRight() and keys[LEFT_KEY]):
            self.turnAround()
        
        self.keepFlying()
        
    def isGoingLeft(self):
        return self.speed < 0
        
    def isGoingRight(self):
        return self.speed > 0

    def keepFlying(self):
        newRect = self.rect.move([self.speed, 0])
        self.rect = newRect
        
        if(self.isAtEdge()):
            self.turnAround()

    def isAtEdge(self):
        return (self.isAtLeftEdge() or self.isAtRightEdge())

    def isAtLeftEdge(self):
        return (self.rect.left < 0)

    def isAtRightEdge(self):
        return (self.rect.right > GAME_WIDTH)
        
    def turnAround(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.speed = -self.speed

class Game:
    def run(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode([width, height])
        
        # Game Title
        pygame.display.set_caption("Catch the woodstocks!")
        snoopy = Snoopy(self)
        
        # Define colors
        black = (0,0,0)
        
        runGame = True
        while runGame:
            self.screen.fill(black)
            
            keys = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    runGame = False
                    break
                elif event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
            
            # snoopy.keepFlying()
            snoopy.move(keys)
            self.draw(snoopy)
            pygame.display.update()

    
    def draw(self,snoopy):
		self.screen.blit(snoopy.image, snoopy.rect)
		pygame.display.update()

game = Game()
game.run(GAME_WIDTH,GAME_HEIGHT)