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
		self.bobbingAmplitude = 2
		self.bobbingSpeed = self.bobbingAmplitude*2

	def move(self, keys):
		if keys and (self.isGoingLeft() and keys[RIGHT_KEY] or self.isGoingRight() and keys[LEFT_KEY]):
			self.turnAround()

		self.keepFlying()

	def isGoingLeft(self):
		return self.speed < 0

	def isGoingRight(self):
		return self.speed > 0

	def keepFlying(self):
		bob = random.randint(1,3)

		newRect = self.rect.move([self.speed, self.bobbingSpeed])
		if bob == 3:
			newRect = self.rect.move([self.speed, self.bobbingSpeed])
			self.bobbingSpeed = -self.bobbingSpeed
		else:
			newRect = self.rect.move([self.speed,0])

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
	def __init__(self, game, counter):
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
		# vspeed: vertical speed
		
		self.vspeed = counter*4
		
		# hspeed: horizontal speed
		self.hspeed = random.randint(-15,15)

	def move(self):
		
		self.rect = self.rect.move([self.hspeed, self.vspeed])

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
		self.hspeed = -self.hspeed

class Game(object):
	def run(self, width, height):
		pygame.init()
		self.screen = pygame.display.set_mode([width, height])

		# Game Title
		pygame.display.set_caption("Catch the woodstocks!")
		
		# Initialize snoopy and the woodstocks
		snoopy = Snoopy(self)
		woodstocks = self.initWoodstocks()

		# Define colors
		black = (0,0,0)
		
		runGame = True
		while runGame:
			
			self.woodstockCollide(woodstocks, snoopy)
			#if (woodstock.rect.bottom >= GAME_HEIGHT) or woodstock.rect.colliderect(snoopy.rect):
			#	woodstock = Woodstock(self)

			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == QUIT:
					runGame = False
					break

			# Move the woodstock
			self.moveWoodstocks(woodstocks)

			snoopy.keepFlying()
			snoopy.move(keys)
			self.draw(snoopy, woodstocks)
			pygame.display.update()
	
	def initWoodstocks(self):
		# The 4 speeds are 4, 8, 12, 16
		woodstocks = []
		counter = 1
		while counter <= 4:
			woodstocks += [Woodstock(self, counter)]
			counter += 1
		
		return woodstocks
	
	#	Checks if any of the woodstocks have collided with snoopy
	def woodstockCollide(self, woodstocks, snoopy):
		for i in xrange(len(woodstocks)):
			if (woodstocks[i].rect.bottom >= GAME_HEIGHT) or woodstocks[i].rect.colliderect(snoopy.rect):
				woodstocks[i] = Woodstock(self, (i+1))
	
	def moveWoodstocks(self, woodstocks):
		for i in xrange(len(woodstocks)):
			woodstocks[i].move()
		
		
	def draw(self,snoopy, woodstocks):
		self.drawSky()
		self.drawWoodstocks(woodstocks)
		self.screen.blit(snoopy.image, snoopy.rect)
		
		pygame.display.update()
	
	def drawSky(self):
		skyimage = pygame.image.load(os.path.join("assets/images/sky", "sky1.jpg"))
		skyimage = pygame.transform.scale(skyimage, (GAME_WIDTH, GAME_HEIGHT))
		skyrect = skyimage.get_rect()
		self.screen.blit(skyimage, skyrect)
		
	def drawWoodstocks(self, woodstocks):
		for i in xrange(len(woodstocks)):
			self.screen.blit(woodstocks[i].image, woodstocks[i].rect)
		
game = Game()
game.run(GAME_WIDTH,GAME_HEIGHT)