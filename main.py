import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from GameComponents.Game import Game
from GameComponents.ControlledPaddle import ControlledPaddle

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((650, 480), vsync=True, flags= pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED )
icon = pygame.image.load(os.path.join("./", "icon.png"))

pygame.display.set_caption("Pong!")
pygame.display.set_icon(icon)

AIPaddleLeft = ControlledPaddle(screen, True, True, True)
AIPaddleLeft.brain.setDifficulty(1)

AIPaddleRight = ControlledPaddle(screen, True, False, True)
AIPaddleRight.brain.setDifficulty(1)

game = Game(screen, leftPaddle=AIPaddleLeft, rightPaddle=AIPaddleRight, silent=False)
AIPaddleLeft.assignGame(game)
AIPaddleRight.assignGame(game)


FPS = 60
# game event loop

while True:
    dt = clock.tick(FPS)
    hSpeed = f'{"+" if game.puck.speedX >= 0 else ""}{game.puck.speedX:.2f}'
    vSpeed = f'{"+" if game.puck.speedY >= 0 else ""}{game.puck.speedY:.2f}'

    print(f'\rFPS: {round(clock.get_fps()):04d} dt: {dt:02d} hSpeed: {hSpeed} vSpeed: {vSpeed}', end=' '*10)
    events = pygame.event.get()
    
    screen.fill((0, 0, 0))
    game.update(events)


    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
