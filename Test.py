import pygame as py
import sys

# Инициализация Pygame
py.init()

# Настройки экрана
screen = py.display.set_mode((600, 900))
py.display.set_caption("Карта в Pygame")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Пример карты (0 - пустое место, 1 - земля, 2 - вода)
map_data = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1]
]

# Размер плитки
TILE_SIZE = 100

# Основной игровой цикл
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

    # Заполнение фона
    screen.fill(WHITE)

    # Отрисовка карты
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            tile = map_data[row][col]
            if tile == 1:
                py.draw.rect(screen, GREEN, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 2:
                py.draw.rect(screen, BLUE, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    py.display.flip()