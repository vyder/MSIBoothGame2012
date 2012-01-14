import random, os, pygame, sys
from pygame.locals import *
from GameCharacter import GameCharacter

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
        self.mainimage = self.image

        # Get the woodstock rect
        self.rect = self.image.get_rect()

        # Get a random x axis location
        width = self.rect.width
        xcoordinate = random.randint(width/2, self.game.width - width/2)

        # Set the woodstock to the top of the game at the x location
        self.rect.top = 0
        self.rect.centerx = xcoordinate

        # Set default vertical speed (arbitrarily decided)
        self.vspeed = 5

        # hspeed: horizontal speed
        self.hspeed = random.randint(-15,15)
        
        # The current rotated degrees
        self.currentRotation = 0

    
    def move(self):
        oldcenter = self.rect.center
        self.currentRotation = (self.currentRotation + self.rspeed) % 360
        self.image = pygame.transform.rotate(self.mainimage, self.currentRotation)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        
        self.rect = self.rect.move([self.hspeed, self.vspeed])
        
        if(self.isAtRightEdge() and self.isGoingRight() or self.isAtLeftEdge() and self.isGoingLeft()):
            self.turnAround()