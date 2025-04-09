import pygame as py

class DayDisplay:
    def __init__(self, position, size, day_count):
        self.position = position
        self.size = size
        self.day_count = day_count
        self.color = (100, 149, 237)
        self.border_color = (70, 100, 180)

    def draw(self, screen):
        # Рисуем квадрат
        rect = py.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        py.draw.rect(screen, self.color, rect)

        # Рисуем обводку
        py.draw.rect(screen, self.border_color, rect, 2)

        # Отображаем количество дней
        font = py.font.Font("Font/PixelizerBold.ttf", 32)
        day_text = font.render(f"{self.day_count}", True, (0, 0, 0))
        text_rect = day_text.get_rect(center=rect.center)
        screen.blit(day_text, text_rect)