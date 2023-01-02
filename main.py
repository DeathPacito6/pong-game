import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from GameComponents.Paddle import Paddle
from GameComponents.Puck import Puck

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((650, 480))
icon = pygame.image.load(os.path.join("./", "icon.png"))

pygame.display.set_caption("Pong!")
pygame.display.set_icon(icon)


opponent = Paddle(screen, pygame.K_w, pygame.K_s)
player = Paddle(screen, pygame.K_UP, pygame.K_DOWN, False)
puck = Puck(screen, opponent, player)

# game event loop
while True:
    clock.tick(60)
    # print(f'\rFPS: {clock.get_fps():.0f}{" "*8}', end='')
    screen.fill((0, 0, 0))
    events = pygame.event.get()

    cursor = pygame.mouse.get_pos()
    opponent.update(events)
    player.update(events)
    opponent.render()
    player.render()
    puck.update()
    puck.render()

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
