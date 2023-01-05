import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from GameComponents.Menu import Menu

FPS = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((650, 480), vsync=True, flags= pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED )
icon = pygame.image.load(os.path.join("./", "icon.png"))

pygame.display.set_caption("Pong!")
pygame.display.set_icon(icon)



menu = Menu(screen, clock, True)


while True:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    events = pygame.event.get()

    menu.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.flip()
