import pygame
import os

from GameComponents.MenuButton import MenuButton
from GameComponents.Game import Game
from GameComponents.ControlledPaddle import ControlledPaddle

class Menu:
    def __init__(self, surface: pygame.Surface, clock: pygame.time.Clock, debug: bool = False):
        self.surface = surface
        self.debug = debug
        self.clock = clock


        self.smallFont = pygame.font.Font(os.path.join("resources", "PressStart2P.ttf"), 20)
        self.largeFont = pygame.font.Font(os.path.join("resources", "PressStart2P.ttf"), 80)
        
        self.title = self.largeFont.render('PONG', 0, (255, 255, 255)).convert()
        self.titleCoords = (self.surface.get_width() / 2 - self.title.get_width() /2, 40)

        self.page = 0

        self.quitGame = MenuButton(self.surface, "X", self.smallFont, (4, 4), (255, 0, 0))
        self.quitGame.coords = (self.surface.get_width() - self.quitGame.image.get_width() - 4, self.quitGame.coords[1])
        self.quitGame.updateRect()

        self.onePlayerBtn = MenuButton(self.surface, "1 Player", self.smallFont, (200, 200)).centered()
        self.twoPlayerBtn = MenuButton(self.surface, "2 Player", self.smallFont, (200, 250)).centered()

        self.gameModeSelect = MenuButton(self.surface, "Select Gamemode", self.smallFont, (200, 145)).centered()
        self.easyModeBtn = MenuButton(self.surface, "Easy", self.smallFont, (200, 210)).centered()
        self.medModeBtn = MenuButton(self.surface, "Medium", self.smallFont, (200, 260)).centered()
        self.hardModeBtn = MenuButton(self.surface, "Hard", self.smallFont, (200, 310)).centered()
        self.impossibleModeBtn = MenuButton(self.surface, "Impossible", self.smallFont, (200, 360)).centered()
        self.backButton = MenuButton(self.surface, "Back", self.smallFont, (200, 430)).centered()

        self.game: "Game" = None

    def new1PGame(self, difficulty: list[0, 1, 2, 3] = 3):
        AIPaddle = ControlledPaddle(self.surface, True, True, self.debug)
        AIPaddle.brain.setDifficulty(difficulty)
        self.game = Game(self.surface, leftPaddle=AIPaddle)
        AIPaddle.assignGame(self.game)
        self.game.puck.pauseFrames = 60

    def new2PGame(self):
        self.game = Game(self.surface)
        self.game.puck.pauseFrames = 60

    def render(self):
        if self.game:
            self.game.render()
            self.quitGame.render()
        elif self.page == 0:
            self.surface.blit(self.title, self.titleCoords)
            self.onePlayerBtn.render()
            self.twoPlayerBtn.render()
        elif self.page == 1:
            self.surface.blit(self.title, self.titleCoords)
            self.gameModeSelect.render()
            self.easyModeBtn.render()
            self.medModeBtn.render()
            self.hardModeBtn.render()
            self.impossibleModeBtn.render()
            self.backButton.render()

    def update(self, events: list[pygame.event.Event]):
        if self.game:
            self.game.update(events)

        cursorPos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game:
                    if self.quitGame.rect.collidepoint(cursorPos):
                        self.game = None
                        self.page = 0
                elif self.page == 0:
                    if self.onePlayerBtn.rect.collidepoint(cursorPos):
                        self.page = 1
                    elif self.twoPlayerBtn.rect.collidepoint(cursorPos):
                        self.new2PGame()
                elif self.page == 1:
                    if self.easyModeBtn.rect.collidepoint(cursorPos):
                        self.new1PGame(3)
                    elif self.medModeBtn.rect.collidepoint(cursorPos):
                        self.new1PGame(2)
                    elif self.hardModeBtn.rect.collidepoint(cursorPos):
                        self.new1PGame(1)
                    elif self.impossibleModeBtn.rect.collidepoint(cursorPos):
                        self.new1PGame(0)
                    elif self.backButton.rect.collidepoint(cursorPos):
                        self.page = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.debug = not self.debug
                    if self.game:
                        self.game.toggleDebug()
        
        self.render()

        if self.debug and self.game:
            hSpeed = f'{"+" if self.game.puck.speedX >= 0 else ""}{self.game.puck.speedX:.2f}'
            vSpeed = f'{"+" if self.game.puck.speedY >= 0 else ""}{self.game.puck.speedY:.2f}'
            FPS = round(self.clock.get_fps())

            print(f'\rFPS: {FPS:04d} hSpeed: {hSpeed} vSpeed: {vSpeed} elapsedFrames: {self.game.elapsedFrames}', end=' '*10)

                
                    



