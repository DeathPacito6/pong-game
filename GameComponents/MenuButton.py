import pygame


class MenuButton:
    def __init__(self, surface: pygame.Surface, text: str, font: pygame.font.Font, coords = (0, 0), color = (255, 255, 255)):
        self.surface = surface
        self.text = text
        self.font = font
        self.coords = coords

        self.image = self.font.render(text, 0, color).convert()
        self.updateRect()

    def updateRect(self):
        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.image.get_width(), self.image.get_height())
        return self

    def centered(self):
        self.coords = (self.surface.get_width() / 2 - self.image.get_width() / 2, self.coords[1])
        self.updateRect()
        return self


    def render(self):
        self.surface.blit(self.image, self.coords)
