import os
import sys

import pygame

class Paddle:
    def __init__(self, surface: pygame.Surface, upKey: str = None, downKey: str = None, leftSide: bool = True):
        self.surface = surface
        self.width = 15
        self.height = 80
        self.wallIndent = 30
        self.leftPaddle = leftSide

        self.top = self.surface.get_height() / 2 - self.height / 2
        self.bottom = self.top + self.height
        self.left = self.wallIndent if leftSide else self.surface.get_width() - self.wallIndent - self.width
        self.right = self.left + self.width

        self.upKey = upKey
        self.downKey = downKey
        self.moveSpeed = 8
        self.direction = 0 # 1 = up, 0 = none, -1 = down
        self.maxY = self.surface.get_height()
        self.minY = 0

        self.colour = (255, 255, 255)

        self.paddle = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.paddle, self.colour, pygame.Rect(0, 0, self.width, self.height))

    def up(self):
        self.top -= self.moveSpeed
        if self.top < self.minY:
            self.top = self.minY

        self.bottom = self.top + self.height

    def down(self):
        self.top += self.moveSpeed
        if self.top + self.height> self.maxY:
            self.top = self.maxY - self.height

        self.bottom = self.top + self.height

    def render(self):
        self.surface.blit(self.paddle, (self.left, self.top))

    def update(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.upKey:
                    self.direction = 1
                elif event.key == self.downKey:
                    self.direction = -1
            if event.type == pygame.KEYUP:
                if event.key == self.upKey and self.direction == 1:
                    self.direction = 0
                if event.key == self.downKey and self.direction == -1:
                    self.direction = 0

        if self.direction == 1:
            self.up()
        elif self.direction == -1:
            self.down()