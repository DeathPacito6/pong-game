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

        self.game = None
        
        self.POI = None
        self.puckTrajectoryTowards = False
        self.ReCalcPOI = False

        self.redSquare = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.rect(self.redSquare, (255, 0, 0), pygame.Rect(0, 0, 15, 15))
        self.redSquare = self.redSquare.convert()

        self.greenSquare = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.greenSquare, (0, 255, 0), pygame.Rect(0, 0, 10, 10))
        self.greenSquare = self.greenSquare.convert()

    def assignGame(self, game: "Game"):
        self.game = game

    def renderPOI(self):
        if not self.POI:
            return
        # self.game.surface.blit(self.redSquare, (self.paddle.left, self.POI))
        self.game.surface.blit(self.greenSquare, (self.paddle.right, self.puckPredictedHeight))

    def checkReCalc(self):
        if self.game.puck.speedX * (1 if self.paddle.leftPaddle else -1) < 0:
            self.puckTrajectoryTowards = True
        else:
            self.puckTrajectoryTowards = False
            self.ReCalcPOI = True

    def predictPuckPath(self):
        if self.game.leftPaddle:
            distance = self.game.puck.left - self.paddle.right
        else:
            distance = self.paddle.left - self.game.puck.right

        steps = distance / abs(self.game.puck.speedX)
        predictedHeight = self.game.puck.top + steps * self.game.puck.speedY * -1
        
        usableScreenHeight = self.game.screenHeight - self.game.puck.height

        while predictedHeight < 0 or predictedHeight > usableScreenHeight:
            if predictedHeight < 0:
                predictedHeight *= -1
            else:
                predictedHeight = 2 * usableScreenHeight - predictedHeight
            
        self.puckPredictedHeight = round(predictedHeight)

        POI = self.puckPredictedHeight - self.paddle.height / 2 + self.game.puck.height / 2

        return POI

    def newPOI(self):
        if not self.game:
            return None

        self.checkReCalc()

        if (self.puckTrajectoryTowards and self.ReCalcPOI) or not self.POI:
            self.POI = self.predictPuckPath()
            self.POI = self.paddle.moveSpeed * round(self.POI / self.paddle.moveSpeed)
            self.ReCalcPOI = False

        return self.POI

        
    