import pygame

from GameComponents.Paddle import Paddle
from GameComponents.Puck import Puck
import random


class Game:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.screenWidth = self.surface.get_width()
        self.screenHeight = self.surface.get_height()

        self.scoreLeft = self.scoreRight = 0
        self.leftPaddle = Paddle(surface, pygame.K_w, pygame.K_s)
        self.rightPaddle = Paddle(surface, pygame.K_UP, pygame.K_DOWN, False)
        self.puck = Puck(surface)

        self.leftScore = 0
        self.rightScore = 0

    def render(self):
        self.leftPaddle.render()
        self.rightPaddle.render()
        self.puck.render()

    def checkPuckPaddleCollision(self, paddle: Paddle):
        checkX = lambda point: paddle.left < point < paddle.right
        checkY = lambda point: paddle.top < point < paddle.bottom

        if (checkX(self.puck.left) or checkX(self.puck.right)) and (checkY(self.puck.top) or checkY(self.puck.bottom)):
            self.puck.left = paddle.right if paddle.leftPaddle else paddle.left - self.puck.width
            self.puck.right = self.puck.left + self.puck.width
            self.puck.horizontalMovement *= -1
            self.puck.verticalMovement += random.randint(1, 2) * self.leftPaddle.direction
            return True
        return False
    
    def checkPointScore(self):
        if self.puck.left < 0:
            self.rightScore += 1
            self.puck = Puck(self.surface, 1)

        elif self.puck.right > self.screenWidth:
            self.leftScore += 1
            self.puck = Puck(self.surface, -1)

    def update(self, events: list[pygame.event.Event]):
        self.leftPaddle.update(events)
        self.rightPaddle.update(events)
        self.puck.update()

        if not self.checkPuckPaddleCollision(self.leftPaddle):
            self.checkPuckPaddleCollision(self.rightPaddle)
            # no need to check for both
        
        self.checkPointScore()

        self.render()
        print(f'\rScore:  {self.leftScore} | {self.rightScore}', end='    ')
