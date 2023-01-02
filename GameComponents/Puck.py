import pygame
from GameComponents.Paddle import Paddle
import math
import random

class Puck:
    def __init__(self, surface: pygame.Surface, leftPaddle: Paddle, rightPaddle: Paddle):
        self.surface = surface
        self.leftPaddle = leftPaddle
        self.rightPaddle = rightPaddle

        self.paddleHeight = leftPaddle.height
        self.paddleWidth = leftPaddle.width
        self.paddleWallIndent = leftPaddle.wallIndent
        self.paddleSpace = self.paddleWallIndent + self.paddleWidth 

        self.screenHeight = self.surface.get_height()
        self.screenWidth = self.surface.get_width()

        self.maxY = self.screenHeight
        self.minY = 0

        self.colour = (255, 255, 255)

        self.width = 10
        self.height = 10

        self.top = self.screenHeight / 2 - self.height / 2
        self.left = self.screenWidth / 2 - self.width / 2

        self.movementSpeed = 5
        self.angle = random.uniform(math.pi / -5, math.pi / 5 )
        self.verticalMovement = self.movementSpeed * math.sin(self.angle)
        self.horizontalMovement = self.movementSpeed * math.cos(self.angle) * -1

        self.puck = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.puck, self.colour, pygame.Rect(0, 0, self.width, self.height))


    def render(self):
        self.surface.blit(self.puck, (self.left, self.top))

    def checkPaddleCollisions(self):
        if self.paddleWallIndent < self.left < self.paddleSpace or self.paddleWallIndent < self.left + self.width < self.paddleWallIndent: # in right bound
            topBound = self.leftPaddle.top
            bottomBound = self.leftPaddle.top + self.paddleHeight
            if topBound < self.top < bottomBound or topBound < self.top + self.height < bottomBound: 
                self.left = self.paddleSpace
                self.horizontalMovement *= -1
                self.verticalMovement += self.leftPaddle.direction

        if self.left > self.screenWidth - self.paddleSpace - self.width and self.left < self.screenWidth - self.paddleSpace : # in right bound
            topBound = self.rightPaddle.top
            bottomBound = self.rightPaddle.top + self.paddleHeight

            if topBound < self.top < bottomBound or topBound < self.top + self.height < bottomBound:
                self.left = self.screenWidth - self.paddleSpace - self.width
                self.horizontalMovement *= -1
                self.verticalMovement += self.rightPaddle.direction        
    
    def checkBoundsCollisions(self):
        if self.left < 0 or self.left + self.width > self.screenWidth:
            self.horizontalMovement = 0
            self.verticalMovement = 0
            self.left = 0 if self.left < 0 else self.screenWidth - self.width
            print('game over :(')
            #emit game over to parent game class

        elif self.top < self.minY:
            self.top = self.minY
            self.verticalMovement *= -1
        elif self.top + self.height > self.maxY:
            self.top = self.maxY - self.height
            self.verticalMovement *= -1


    def update(self):
        self.checkBoundsCollisions()
        self.checkPaddleCollisions()

        self.top -= self.verticalMovement
        self.left += self.horizontalMovement
