import pygame
from GameComponents.Paddle import Paddle
from GameComponents.AlgorithmBrain import AlgorithmBrain

# typehinting hack to bypass circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from GameComponents.Game import Game

class ControlledPaddle(Paddle):
    def __init__(self, surface: pygame.Surface, CPU: bool, leftSide: bool = True):
        super(ControlledPaddle, self).__init__(surface, leftSide=leftSide, AIControlled=True)

        self.CPU = CPU
        
        if self.CPU:
            self.brain = AlgorithmBrain(self)

        self.game: "Game"

    def assignGame(self, game: "Game"):
        self.game = game
        self.brain.assignGame(game)
    

    def render(self):
        super(ControlledPaddle, self).render()
        self.brain.renderPOI()
    
    def moveToPOI(self):
        if not self.brain.POI:
            return
        if self.brain.POI < self.top:
            self.up()
        elif self.brain.POI > self.top:
            self.down()

    def update(self, events):
        if not self.game: 
            return
        
        self.brain.newPOI()
        self.moveToPOI()


