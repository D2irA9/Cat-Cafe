import pygame as py

class Button:
    def __init__(self, text, x, y, width, height, text_color, bg_color):
        self.image = py.Surface((width, height))
        self.image.fill(bg_color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.font = py.font.Font(None, 36)
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)