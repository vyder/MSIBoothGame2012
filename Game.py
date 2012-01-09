import random, os, pygame, sys
from pygame.locals import *
from Snoopy import Snoopy
from Woodstock import Woodstock

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

Q = pygame.K_q
COLOR_BLACK = (0,0,0)
TIME_UP = pygame.USEREVENT + 1

class Game(object):
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        
        self.score = 0

        pygame.event.post(pygame.event.Event(TIME_UP,{}))

        # Start a timer to figure out when the game ends (60 seconds)
        pygame.time.set_timer(TIME_UP,60000)

        # Game Title
        pygame.display.set_caption("Catch the woodstocks!")

        # font = pygame.font.Font(os.path.join("assets/fonts", "peanuts.tff"), 28)
        self.font = pygame.font.Font(os.path.join("assets/fonts", "cella.otf"), 28)
        
        # Render the text with Anti-aliasing
        self.scoreText = self.font.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.scorepos = self.scoreText.get_rect(left = 40, top = 20)
        
        # Initialize snoopy and the woodstocks
        self.snoopy = Snoopy(self)
        self.woodstocks = self.createWoodstocks()
        

    def run(self):
        # Define colors
        black = (0,0,0)

        self.gameOver = False
        while not self.gameOver:

            self.resetDeadWoodstocks()

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == QUIT or keys and keys[Q]:
                    self.gameOver = True
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
                if(w.hasCollidedWith(self.snoopy)):
                    self.score += 1
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
        
        self.scoreText = self.font.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.screen.blit(self.scoreText, self.scorepos)

        pygame.display.update()

    def drawSky(self):
        skyimage = pygame.image.load(os.path.join("assets/images/sky", "sky1.jpg"))
        skyimage = pygame.transform.scale(skyimage, (self.width, self.height))
        skyrect = skyimage.get_rect()
        self.screen.blit(skyimage, skyrect)

game = Game(1250, 750)
game.run()