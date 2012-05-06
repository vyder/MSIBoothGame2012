import random, os, pygame, sys
from pygame.locals import *

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
        return (self.rect.right > self.game.width)
    
    def isAtBottomEdge(self):
        return (self.rect.bottom >= self.game.height)
    
    def turnAround(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.hspeed = -self.hspeed
    
    def hasCollidedWith(self, otherObject):
        return self.rect.colliderect(otherObject.rect)
    
    def setHSpeed(self, horizontalSpeed):
        self.setSpeed(horizontalSpeed, None, None)


    def setVSpeed(self, verticalSpeed):
        self.setSpeed(None, verticalSpeed, None)

    def setRSpeed(self, rspeed):
        self.setSpeed(None, None, rspeed)

    def setSpeed(self, horizontalSpeed, verticalSpeed, rspeed):
        if(horizontalSpeed):
            self.hspeed = horizontalSpeed

        if(verticalSpeed):
            self.vspeed = verticalSpeed

        if(rspeed):
            self.rspeed = rspeed
            
    def stop(self):
        self.hspeed = self.vspeed = self.rspeed = 0
        
    def joyStick_isRight(self, joyStick):
        horizontal = joyStick.get_axis(0)
        if horizontal >= 0.004:
            return True
        return False
        
    def joyStick_isLeft(self, joyStick):
        horizontal = joyStick.get_axis(0)
        if horizontal <= -0.004:
            return True
        return False
