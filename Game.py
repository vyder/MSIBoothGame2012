import random, os, pygame, sys
from pygame.locals import *
from Snoopy import Snoopy
from Woodstock import Woodstock

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

Q = pygame.K_q

class Game(object):
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
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
        skyimage = pygame.transform.scale(skyimage, (self.width, self.height))
        skyrect = skyimage.get_rect()
        self.screen.blit(skyimage, skyrect)

game = Game(1250, 750)
game.run()
