import random, os, pygame, sys
from pygame.locals import *
from GameCharacter import GameCharacter

LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT

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
        self.rect.bottom = self.game.height
        self.rect.centerx = self.game.width/2

        self.hspeed = 10
        self.bobbingAmplitude = 2
        self.bobbingSpeed = self.bobbingAmplitude*2

    def move(self, joyStick, keys):
        if keys and (self.isGoingLeft() and keys[RIGHT_KEY] or self.isGoingRight() and keys[LEFT_KEY]):
            self.turnAround()
        
        if (self.isGoingLeft() and self.joyStick_isRight(joyStick) or self.isGoingRight() and self.joyStick_isLeft(joyStick)):
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
