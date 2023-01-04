import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from GameComponents.Game import Game

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((650, 480), vsync=True, flags= pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED )
icon = pygame.image.load(os.path.join("./", "icon.png"))

pygame.display.set_caption("Pong!")
pygame.display.set_icon(icon)

game = Game(screen)
FPS = 60
# game event loop

while True:
    dt = clock.tick(FPS)
    print(f'\rFPS: {clock.get_fps():.0f} dt: {dt} hSpeed: {game.puck.speedX:.2f} vSpeed: {game.puck.speedY:.2f}', end=' '*10)
    events = pygame.event.get()
    
    screen.fill((0, 0, 0))
    game.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
