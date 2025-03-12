import pygame as py
import sys
from Button import Button

py.init()

# Настройки окна
screen = py.display.set_mode((600, 900))
py.display.set_caption("Hi")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Шрифт
font = py.font.Font("Font/PixelizerBold.ttf", 36)

Greeting = "Привет, мы с тобой знакомы?"

# Создание кнопок с новыми цветами
button_yes = Button("Да", 135, 360, 350, 100, WHITE,(30, 144, 255))
button_no = Button("Нет", 135, 560, 350, 100,  WHITE,(220, 20, 60))

# Основной игровой цикл
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

    # Отрисовка
    screen.fill(WHITE)

    # Отображение заголовка по центру
    header_surface = font.render(Greeting, True, BLACK)
    header_rect = header_surface.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(header_surface, header_rect)

    # Отрисовка кнопок
    button_yes.draw(screen)
    button_no.draw(screen)

    py.display.flip()