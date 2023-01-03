import pygame
import os

class Scoreboard:
    def __init__(self, surface: pygame.Surface, game):
        self.surface = surface
        self.game = game
        self.scoreLeft = 9
        self.scoreRight = 9
        
        self.font = pygame.font.Font(os.path.join("GameComponents", "bit5x3.ttf"), 64)
        self.newCharOffset = self.font.render("0", 0, (255, 255, 255)).get_width() / 2
        print(self.newCharOffset)
        self.update()

    def update(self):
        self.board = self.font.render(f"{self.scoreLeft} | {self.scoreRight}", 0, (255, 255, 255)).convert()
        xPos = self.surface.get_width() / 2 - self.board.get_width() / 2 
        if self.scoreLeft >= 10:
            xPos -= self.newCharOffset
        if self.scoreRight >= 10:
            xPos += self.newCharOffset
        self.placeAt = (xPos, 10)

    def render(self):
        self.surface.blit(self.board, self.placeAt)
    
    def pointLeft(self):
        self.scoreLeft += 1
        self.update()

    def pointRight(self):
        self.scoreRight += 1
        self.update()

