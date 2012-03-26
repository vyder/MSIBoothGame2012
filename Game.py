import random, os, pygame, sys
from pygame.locals import *
from Snoopy import Snoopy
from Woodstock import Woodstock

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Pygame Keys
Q = pygame.K_q
R = pygame.K_r
ESCAPE = pygame.K_ESCAPE

# Colors
COLOR_BLACK = (0,0,0)

# Events
TIME_UP = pygame.USEREVENT + 1

class Game(object):
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode([width, height])
        
        self.score = 0
        self.totalTime = 60

        pygame.event.post(pygame.event.Event(TIME_UP,{}))

        # Start a timer to figure out when the game ends (60 seconds)
        pygame.time.set_timer(TIME_UP,60000)
        self.startTime = pygame.time.get_ticks()

        # Game Title
        pygame.display.set_caption("Catch the woodstocks!")

        # font = pygame.font.Font(os.path.join("assets/fonts", "peanuts.tff"), 28)
        self.font = pygame.font.Font(os.path.join("assets/fonts", "cella.otf"), 28)
        
        # Render the text with Anti-aliasing
        self.scoreText = self.font.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.scorepos = self.scoreText.get_rect(left = 40, top = 20)
        self.timerText = self.font.render("Time Left: " + str(self.time_left()), True, COLOR_BLACK)
        self.timerpos = self.timerText.get_rect(left = 40, top = 50)
        
        # Initialize snoopy and the woodstocks
        self.snoopy = Snoopy(self)
        self.woodstocks = self.createWoodstocks()
        
    def time_left(self):
        return self.totalTime - self.current_time()
    
    def current_time(self):
        return (pygame.time.get_ticks() - self.startTime)/1000

    def run(self):
        while True:
            # Define colors
            black = (0,0,0)

            self.gameOver = False
            timerIsRunning = False
            while not self.gameOver:

                self.resetDeadWoodstocks()

                keys = pygame.key.get_pressed()

                for event in pygame.event.get():
                    if event.type == QUIT or keys and keys[Q] or timerIsRunning and event.type == TIME_UP:
                        self.gameOver = True
                        break
                
                    # This code is to fix a wierd glitchy thing the timer does at the start
                    if event.type == TIME_UP and not timerIsRunning:
                        timerIsRunning = True

                self.moveWoodstocks()
                self.snoopy.move(keys)
            
                self.draw()
                pygame.display.update()
        
            self.snoopy.stop()
            while True:
                #print "drawing the end"
                self.drawTheEnd()
                
                keys = pygame.key.get_pressed()
                
                for event in pygame.event.get():
                    if event.type == QUIT or keys and keys[ESCAPE]:
                        return
                    if keys and keys[R]:
                        self.reset()
                        break

    def reset():
        pass
        
    def createWoodstocks(self):
        # There is one woodstock for each speed
        # The first one is vertical speed. Second one is the rotational speed
        speeds = [(4,10), (8,20), (12,30), (16, 40)]
        woodstocks = []

        for speedPair in speeds:
            speed, rspeed = speedPair
            w = Woodstock(self)
            w.setVSpeed(speed)
            w.setRSpeed(rspeed)
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
                rspeed = w.rspeed
                self.woodstocks.remove(w)
                w = Woodstock(self)
                w.setVSpeed(vspeed)
                w.setRSpeed(rspeed)
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
        self.timerText = self.font.render("Time Left: " + str(self.time_left()), True, COLOR_BLACK)
        self.screen.blit(self.timerText, self.timerpos)

        pygame.display.update()

    def drawSky(self):
        skyimage = pygame.image.load(os.path.join("assets/images/sky", "sky1.jpg"))
        skyimage = pygame.transform.scale(skyimage, (self.width, self.height))
        skyrect = skyimage.get_rect()
        self.screen.blit(skyimage, skyrect)
    
    def drawTheEnd(self):
        self.drawSky()
        self.scoreText = self.font.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.scorepos = self.scoreText.get_rect(centerx = self.width/2, centery = self.height/2 - 50)
        self.screen.blit(self.scoreText, self.scorepos)
        theEnd = self.font.render("The End", True, COLOR_BLACK)
        theEndpos = theEnd.get_rect(centerx = self.width/2, centery = self.height/2)
        

game = Game(1250, 750)
game.run()
