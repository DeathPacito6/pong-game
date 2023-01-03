import pygame
import os

from GameComponents.Paddle import Paddle
from GameComponents.Puck import Puck
from GameComponents.Scoreboard import Scoreboard
from GameComponents.Sounds import Sounds
import random


class Game:
    def __init__(self, surface: pygame.Surface, sounds: Sounds = None):
        self.sounds = sounds
        
        self.surface = surface
        self.screenWidth = self.surface.get_width()
        self.screenHeight = self.surface.get_height()

        self.leftPaddle = Paddle(surface, pygame.K_w, pygame.K_s)
        self.rightPaddle = Paddle(surface, pygame.K_UP, pygame.K_DOWN, False)
        
        self.newPuck()
        self.maxPuckSpeed = 7
        self.puckSpeedIncrements = 0.3
        
        self.scoreboard = Scoreboard(self.surface, self)
        self.winner = 0

    def newPuck(self, direction:int = 1):
        self.puck = Puck(self.surface, direction, self.sounds)

    def render(self):
        self.leftPaddle.render()
        self.rightPaddle.render()
        self.puck.render()
        self.scoreboard.render()

    def checkPuckPaddleCollision(self, paddle: Paddle):
        checkX = lambda point: paddle.left < point < paddle.right
        checkY = lambda point: paddle.top < point < paddle.bottom

        if (checkX(self.puck.left) or checkX(self.puck.right)) and (checkY(self.puck.top) or checkY(self.puck.bottom)):
            self.puck.left = paddle.right if paddle.leftPaddle else paddle.left - self.puck.width
            self.puck.right = self.puck.left + self.puck.width
            self.puck.speedX *= -1

            self.puck.speedX += self.puckSpeedIncrements * self.puck.getDirection()
            if abs(self.puck.speedX) > self.maxPuckSpeed:
                self.puck.speedX = self.maxPuckSpeed * self.puck.getDirection()

            self.puck.speedY += random.randint(1, 2) * self.leftPaddle.direction
            if self.sounds: 
                self.sounds.playPaddleSound()
            return True
        return False
    
    def checkPointScore(self):
        if self.puck.left < 0:
            self.scoreboard.pointRight()
            self.newPuck(1)
            if self.sounds:
                self.sounds.playScoreSound()

        elif self.puck.right > self.screenWidth:
            self.scoreboard.pointLeft()
            self.newPuck(-1)
            if self.sounds:
                self.sounds.playScoreSound()

        self.winner = self.scoreboard.checkWinner()

    def update(self, events: list[pygame.event.Event]):
        if self.winner:
            self.render()
            return

        self.leftPaddle.update(events)
        self.rightPaddle.update(events)
        self.puck.update()

        if not self.checkPuckPaddleCollision(self.leftPaddle):
            self.checkPuckPaddleCollision(self.rightPaddle)
            # no need to check for both

        self.checkPointScore()
        self.render()
