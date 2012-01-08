import random, os, pygame, sys
from pygame.locals import *

GAME_WIDTH = 1250
GAME_HEIGHT = 750
LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

class Snoopy(object):
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

class Woodstock(object):
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
		
		# Set the speed of the falling woodstock
		self.speed = 5



class Game(object):
	def run(self, width, height):
		pygame.init()
		self.screen = pygame.display.set_mode([width, height])

		# Game Title
		pygame.display.set_caption("Catch the woodstocks!")
		snoopy = Snoopy(self)
		woodstock = Woodstock(self)

		# Define colors
		black = (0,0,0)
		
		runGame = True
		while runGame:
			self.screen.fill(black)

			if (woodstock.rect.bottom >= GAME_HEIGHT) or woodstock.rect.colliderect(snoopy.rect):
				woodstock = Woodstock(self)

			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == QUIT:
					runGame = False
					break

			# Move the woodstock
			woodstock.rect = woodstock.rect.move([0, woodstock.speed])

			snoopy.keepFlying()
			snoopy.move(keys)
			self.draw(snoopy, woodstock)
			pygame.display.update()


	def draw(self,snoopy, woodstock):
		skyimage = pygame.image.load(os.path.join("assets/images/sky", "sky1.jpg"))
		skyimage = pygame.transform.scale(skyimage, (GAME_WIDTH, GAME_HEIGHT))
		skyrect = skyimage.get_rect()
		self.screen.blit(skyimage, skyrect)
		self.screen.blit(snoopy.image, snoopy.rect)
		self.screen.blit(woodstock.image, woodstock.rect)
		pygame.display.update()

game = Game()
game.run(GAME_WIDTH,GAME_HEIGHT)