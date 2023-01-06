import pygame

import math
import random

# typehinting hack to bypass circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from GameComponents.Game import Game
    from GameComponents.Paddle import Paddle

class AlgorithmBrain:
    def __init__(self, paddle: "Paddle"):
        self.paddle = paddle
        self.paddleJitter = False

        self.game = None
        
        self.POI = None
        self.puckTrajectoryTowards = False
        self.ReCalcPOI = False

        self.redSquare = self.newShape((255, 0, 0), (15, 5))
        self.greenSquare = self.newShape((0, 255, 0), (10, 10))
        self.blueSquare = self.newShape((0, 0, 255), (10, 10))

        self.difficulty = 0
        self.movementCooldown = 0

    def newShape(self, color, size = (10, 10)):
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surface, color, pygame.Rect(0, 0, size[0], size[1]))
        return surface.convert()
    
    def assignGame(self, game: "Game"):
        self.game = game
        return self

    def setDifficulty(self, difficulty: list[0, 1, 2, 3] = 0):
        if difficulty in [0, 1, 2, 3]:
            self.difficulty = difficulty
        return self
    
    def setJitter(self, jitter: bool = False):
        self.paddleJitter = jitter
        return self

    def renderPOI(self):
        if self.POI is None:
            return

        xPos = self.paddle.right if self.paddle.leftPaddle else self.paddle.left - 10

        self.game.surface.blit(self.redSquare, (self.paddle.left, self.POI))
        self.game.surface.blit(self.blueSquare, (xPos, self.puckPredictedHeight))
        self.game.surface.blit(self.greenSquare, (xPos, self.realPredictedHeight))


    def checkReCalc(self):
        if self.game.puck.speedX * (1 if self.paddle.leftPaddle else -1) < 0:
            self.puckTrajectoryTowards = True
        else:
            self.puckTrajectoryTowards = False
            self.ReCalcPOI = True

    def refitInScreen(self, value):
        usableScreenHeight = self.game.screenHeight - self.game.puck.height

        while value < 0 or value > usableScreenHeight:
            if value < 0:
                value *= -1
            else:
                value = 2 * usableScreenHeight - value
        return value

    def predictPuckPath(self):
        if self.game.leftPaddle:
            distance = self.game.puck.left - self.paddle.right
        else:
            distance = self.paddle.left - self.game.puck.right

        steps = abs(distance / self.game.puck.speedX)
        predictedHeight = self.game.puck.top + steps * self.game.puck.speedY * -1
        
        predictedHeight = self.refitInScreen(predictedHeight)
        self.realPredictedHeight = round(predictedHeight)

        if self.difficulty > 0:
            offset = round(self.paddle.height / 2  + [0, 9, 18, 30][self.difficulty])
            predictedHeight += random.randint(-offset, offset)
            predictedHeight = self.refitInScreen(predictedHeight)
            self.puckPredictedHeight = predictedHeight
        else:
            self.puckPredictedHeight = predictedHeight

        POI = predictedHeight - self.paddle.height / 2 + self.game.puck.height / 2
        if POI > self.game.screenHeight - self.paddle.height:
            POI = self.game.screenHeight - self.paddle.height
        elif POI < 0:
            POI = 0

        self.movementCooldown = random.randint(0, [0, 20, 30, 45][self.difficulty])

        return POI

    def newPOI(self):
        if not self.game:
            return None

        self.checkReCalc()

        # print("\r", self.difficulty, self.puckTrajectoryTowards, self.ReCalcPOI, self.POI, end=' '*10)
        if self.puckTrajectoryTowards and (self.ReCalcPOI or self.difficulty == 0):
            self.POI = self.predictPuckPath()
            self.POI = self.paddle.moveSpeed * round(self.POI / self.paddle.moveSpeed)
            if self.paddleJitter:
                self.POI += 0.5

            self.ReCalcPOI = False

        return self.POI

        
    