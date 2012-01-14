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
        
        # Game Title
        pygame.display.set_caption("Catch the woodstocks!")

        self.score = 0
        self.totalTime = 10

        # Start a timer to figure out when the game ends (in milliseconds)
        pygame.time.set_timer(TIME_UP,self.totalTime*1000)
        self.startTime = pygame.time.get_ticks()

        # font = pygame.font.Font(os.path.join("assets/fonts", "peanuts.tff"), 28)
        self.fontRegular = pygame.font.Font(os.path.join("assets/fonts", "cella.otf"), 28)
        self.fontSmall = pygame.font.Font(os.path.join("assets/fonts", "cella.otf"), 20)
        
        # Render the text with Anti-aliasing
        self.scoreText = self.fontRegular.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.scorepos = self.scoreText.get_rect(left = 40, top = 20)
        self.timerText = self.fontRegular.render("Time Left: " + str(self.time_left()), True, COLOR_BLACK)
        self.timerpos = self.timerText.get_rect(left = 40, top = 50)
        self.instructions = self.fontSmall.render("[ESC] to quit", True, COLOR_BLACK)
        self.instructionsPos = self.instructions.get_rect(bottom = self.height - 20, right = self.width - 20)
        
        # Initialize snoopy and the woodstocks
        self.snoopy = Snoopy(self)
        self.woodstocks = self.createWoodstocks()
        
    def time_left(self):
        return self.totalTime - self.current_time()
    
    # Returns time since startTime in seconds
    def current_time(self):
        return (pygame.time.get_ticks() - self.startTime)/1000

    def run(self):
        while True:
            self.gameOver = False
            timerIsRunning = True
            while not self.gameOver:

                self.resetDeadWoodstocks()

                keys = pygame.key.get_pressed()

                for event in pygame.event.get():
                    if event.type == QUIT or keys and keys[ESCAPE] or timerIsRunning and event.type == TIME_UP:
                        self.gameOver = True
                        break

                self.moveWoodstocks()
                self.snoopy.move(keys)
            
                self.draw()
                pygame.display.update()
        
            # Game End State
            self.snoopy.stop()
            
            # stop the woodstocks too -- TODO

            self.drawTheEnd()
            
            while self.gameOver:
                keys = pygame.key.get_pressed()
                
                for event in pygame.event.get():
                    if event.type == QUIT or keys and keys[ESCAPE]:
                        return
                    elif keys and keys[R]:
                        self.reset()
                        self.gameOver = False

    def reset(self):
      # reset score and position
      self.score = 0
      self.scorepos = self.scoreText.get_rect(left = 40, top = 20)

      # reset timer
      pygame.time.set_timer(TIME_UP,self.totalTime*1000)
      self.startTime = pygame.time.get_ticks()

      # reset game characters
      self.snoopy = Snoopy(self)
      self.woodstocks = self.createWoodstocks()
        
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
        # Redraw the background and the game characters
        self.drawBackground()
        for w in self.woodstocks:
            self.screen.blit(w.image, w.rect)
        self.screen.blit(self.snoopy.image, self.snoopy.rect)
        
        # Update and redraw the score and timer text
        self.scoreText = self.fontRegular.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.screen.blit(self.scoreText, self.scorepos)
        self.timerText = self.fontRegular.render("Time Left: " + str(self.time_left()), True, COLOR_BLACK)
        self.screen.blit(self.timerText, self.timerpos)
        
        # Redraw instructions
        self.screen.blit(self.instructions, self.instructionsPos)

        pygame.display.update()

    def drawBackground(self):
      self.drawSky()
    
    def drawSky(self):
        skyimage = pygame.image.load(os.path.join("assets/images/sky", "sky1.jpg"))
        skyimage = pygame.transform.scale(skyimage, (self.width, self.height))
        skyrect = skyimage.get_rect()
        self.screen.blit(skyimage, skyrect)
    
    def drawTheEnd(self):

        # Draw the background
        self.drawBackground()
        
        # Draw the final score
        self.scoreText = self.fontRegular.render("Score: " + str(self.score), True, COLOR_BLACK)
        self.scorepos = self.scoreText.get_rect(centerx = self.width/2, centery = self.height/2 - 50)
        self.screen.blit(self.scoreText, self.scorepos)

        # Draw "The End"
        theEnd = self.fontRegular.render("The End", True, COLOR_BLACK)
        theEndpos = theEnd.get_rect(centerx = self.width/2, centery = self.height/2)
        self.screen.blit(theEnd, theEndpos)
        
        # Draw Instructions Text
        self.instructions = self.fontSmall.render("[R] to start a new game, [ESC] to quit", True, COLOR_BLACK)
        self.instructionsPos = instructions.get_rect(centerx = self.width/2, centery = self.height/2 + 50)
        self.screen.blit(self.instructions, self.instructionsPos)
        
        pygame.display.update()
        

game = Game(1250, 750)
game.run()
