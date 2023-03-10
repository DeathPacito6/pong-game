import pygame
import math
import random

from GameComponents.Sounds import Sounds

class Puck:
    def __init__(self, surface: pygame.Surface, target: int = 1, sounds: Sounds = None):
        self.sounds = sounds

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

    def wallBounce(self):
        self.speedY *= -1
        if self.top < 0:
            self.top = 0
            self.bottom = self.top + self.height
        elif self.bottom > self.screenHeight:
            self.bottom = self.screenHeight
            self.top = self.bottom - self.height
        self.sounds.playWallSound()
     
    # does not include left and right edge 
    def checkBoundsCollisions(self):
        if self.top < self.minY:
            self.top = self.minY
            self.wallBounce()

        elif self.bottom > self.maxY:
            self.top = self.maxY - self.height
            self.wallBounce()
        
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
