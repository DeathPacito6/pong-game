import pygame
from GameComponents.Paddle import Paddle
from GameComponents.AlgorithmBrain import AlgorithmBrain

# typehinting hack to bypass circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from GameComponents.Game import Game

class ControlledPaddle(Paddle):
    def __init__(self, surface: pygame.Surface, CPU: bool, leftSide: bool = True, debug: bool = False):
        super(ControlledPaddle, self).__init__(surface, leftSide=leftSide, AIControlled=True)

        self.CPU = CPU
        self.debug = debug
        
        if self.CPU:
            self.brain = AlgorithmBrain(self)

        self.game: "Game"

    def assignGame(self, game: "Game"):
        self.game = game
        self.brain.assignGame(game)
    

    def render(self):
        super(ControlledPaddle, self).render()
        if self.debug:
            self.brain.renderPOI()
    
    def moveToPOI(self):
        if self.CPU and self.brain.movementCooldown > 0:
            self.brain.movementCooldown -= 1
            return
        if not self.brain.POI:
            self.direction = 0
            return
        if self.brain.POI < self.top:
            self.up()
            self.direction = 1
        elif self.brain.POI > self.top:
            self.down()
            self.direction = -1
        else:
            self.direction = 0

    def update(self, events):
        if not self.game: 
            return
        
        self.brain.newPOI()
        self.moveToPOI()


