import pygame
import os

class Sounds:
    def __init__(self, silent: bool = False):
        self.silent = silent
        self.channel = pygame.mixer.Channel(0)

        self.paddleSound = pygame.mixer.Sound(os.path.join('resources', 'paddle.ogg'))
        self.scoreSound = pygame.mixer.Sound(os.path.join('resources', 'score.ogg'))
        self.wallSound = pygame.mixer.Sound(os.path.join('resources', 'wall.ogg'))
    
    def toggleSound(self):
        self.silent = not self.silent
    
    def playPaddleSound(self):
        if not self.silent:
            self.channel.play(self.paddleSound)
    
    def playScoreSound(self):
        if not self.silent:
            self.channel.play(self.scoreSound)

    def playWallSound(self):
        if not self.silent:
            self.channel.play(self.wallSound)