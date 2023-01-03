import pygame
import os

class Sounds:
    def __init__(self):
        self.channel = pygame.mixer.Channel(0)

        self.paddleSound = pygame.mixer.Sound(os.path.join('resources', 'paddle.ogg'))
        self.scoreSound = pygame.mixer.Sound(os.path.join('resources', 'score.ogg'))
        self.wallSound = pygame.mixer.Sound(os.path.join('resources', 'wall.ogg'))
    
    def playPaddleSound(self):
        self.channel.play(self.paddleSound)
    
    def playScoreSound(self):
        self.channel.play(self.scoreSound)

    def playWallSound(self):
        self.channel.play(self.wallSound)