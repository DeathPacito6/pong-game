import pygame
import math
import random

class Puck:
    def __init__(self, surface: pygame.Surface, target: int = 1):
        self.surface = surface

        self.screenHeight = self.surface.get_height()
        self.screenWidth = self.surface.get_width()

        self.maxY = self.screenHeight
        self.minY = 0

        self.colour = (255, 255, 255)

        self.width = 10
        self.height = 10

        self.top = self.screenHeight / 2 - self.height / 2
        self.left = self.screenWidth / 2 - self.width / 2
        self.bottom = self.top + self.height
        self.right = self.left + self.width

        self.movementSpeed = 5
        self.angle = random.uniform(math.pi / -4, math.pi / 4 )
        self.speedY = math.ceil(self.movementSpeed * math.sin(self.angle))
        self.speedX = math.ceil(self.movementSpeed * math.cos(self.angle)) * target

        self.pauseFrames = 30

        self.puck = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.puck, self.colour, pygame.Rect(0, 0, self.width, self.height))
        self.puck = self.puck.convert()

    def getDirection(self):
        return 1 if self.speedX > 0 else -1

    def render(self):
        self.surface.blit(self.puck, (self.left, self.top))  
     
    # does not include left and right edge 
    def checkBoundsCollisions(self):
        if self.top < self.minY:
            self.top = self.minY
            self.speedY *= -1

        elif self.bottom > self.maxY:
            self.top = self.maxY - self.height
            self.speedY *= -1
        
        self.bottom = self.top + self.height


    def update(self):
        if self.pauseFrames > 0:
            self.pauseFrames -= 1
            return

        self.top -= self.speedY
        self.left += self.speedX
        self.right += self.speedX
        #self.bottom is done at the end of selfcheckBoundsCollisions()

        self.checkBoundsCollisions()
