import pygame as py
import sys
from pytmx.util_pygame import load_pygame
from Drawing import Tile
from Button import Button
from Player import Player

def Game():
    """Игра"""
    py.init()

    screen = py.display.set_mode((640, 960))
    py.display.set_caption("Cat-Cafe")

    # Загруска карты
    map = load_pygame("Map/map.tmx")
    tile_group = py.sprite.Group()

    # Размер плиток
    TILE_SIZE = 16
    # Маштаб
    scale = 4

    # Вытвскивание всех слоёв карты
    for layer in map.visible_layers:
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                Tile(pos=pos, surf=surf, groups=tile_group, scale=scale)

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Шрифт
    font = py.font.Font("Font/PixelizerBold.ttf", 36)

    start = Button("Начать рабочий день", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185))

    # Игрок
    player = Player((130, 310), scale=4)
    all_sprites = py.sprite.Group(player)

    clock = py.time.Clock()

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()


        all_sprites.update()

        screen.fill(WHITE)
        tile_group.draw(screen)
        all_sprites.draw(screen)

        start.draw(screen)

        py.display.flip()
        clock.tick(60)
