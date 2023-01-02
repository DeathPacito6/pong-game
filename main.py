import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from GameComponents.Game import Game

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((650, 480), vsync=1)
icon = pygame.image.load(os.path.join("./", "icon.png"))

pygame.display.set_caption("Pong!")
pygame.display.set_icon(icon)

game = Game(screen)

# game event loop
while True:
    clock.tick(60)
    # print(f'\rFPS: {clock.get_fps():.0f}{" "*8}', end='')
    events = pygame.event.get()
    
    screen.fill((0, 0, 0))
    game.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
