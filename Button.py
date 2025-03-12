import pygame as py

class Button:
    def __init__(self, text, x, y, width, height, text_color, hover_color):
        self.rect = py.Rect(x, y, width, height)
        self.text_color = text_color
        self. hover_color = hover_color
        self.text = text
        self.font = py.font.Font("Font/PixelizerBold.ttf", 36)

    def draw(self, surface):
        #Приверка на наведение мыши
        mouse_pos = py.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            py.draw.rect(surface, self.hover_color, self.rect)
        else:
            py.draw.rect(surface, self.hover_color, self.rect)

        #Отображение текста на кпопке
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rest = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rest)

    def is_clicked(self):
        mouse_pos = py.mouse.get_pos()
        mouse_click = py.mouse.get_pressed()
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]