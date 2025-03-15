import pygame as py
import sys
from pytmx.util_pygame import load_pygame
from Drawing import Tile
from Player import Player
from Button import Button

def game():
    """Запуск игры"""
    py.init()

    screen = py.display.set_mode((640, 960))
    py.display.set_caption("Cat-Cafe")

    # Загруска карты
    map = load_pygame("Map/map.tmx")
    tile_group = py.sprite.Group()
    # Группа для игрока
    # player_group = py.sprite.Group()

    # Размер плитки
    TILE_SIZE = 16
    # Коэффициент масштабирования
    scale = 4

    for layer in map.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                Tile(pos=pos, surf=surf, groups=tile_group, scale=scale)

    # Загрузка изображений спрайта игрока
    # sprite_sheet = py.image.load("Sprite/Player/Player.png").convert_alpha()

    # Разделение спрайт-листа на анимации
    # animations = {
    #     "inaction": [
    #         py.transform.scale(sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
    #         py.transform.scale(sprite_sheet.subsurface((48, 0, 48, 48)), (48 * scale, 48 * scale))
    #     ],
    #     "forward": [
    #         py.transform.scale(sprite_sheet.subsurface((0, 48, 48, 48)), (48 * scale, 48 * scale)),
    #         py.transform.scale(sprite_sheet.subsurface((144, 48, 48, 48)), (48 * scale, 48 * scale))
    #     ],
    #     "back": [
    #         py.transform.scale(sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
    #         py.transform.scale(sprite_sheet.subsurface((144, 0, 48, 48)), (48 * scale, 48 * scale))
    #     ],
    #     "left": [
    #         py.transform.scale(sprite_sheet.subsurface((0, 96, 48, 48)), (48 * scale, 48 * scale)),
    #         py.transform.scale(sprite_sheet.subsurface((144, 96 , 48, 48)), (48 * scale, 48 * scale))
    #     ],
    #     "right": [
    #         py.transform.scale(sprite_sheet.subsurface((0, 144, 48, 48)), (48 * scale, 48 * scale)),
    #         py.transform.scale(sprite_sheet.subsurface((144, 144, 48, 48)), (48 * scale, 48 * scale))
    #     ]
    # }

    # Создание игрока
    # player = Player(pos=(140, 300), animations=animations, groups=player_group)

    # Цвета
    WHITE = (255, 255, 255)

    # clock = py.time.Clock()
    button_start = Button("Начать рабочий день", 135, 560, 350, 100, (0, 0, 0), (255, 218, 185))

    while True:
        # dt = clock.tick(60) / 1000.0  # Время в секундах с последнего кадра

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()



        # Обновляем игрока и плитки
        tile_group.update()  # Обновление плиток
        # player_group.update(dt)  # Обновление игрока

        screen.fill(WHITE)  # Очистка экрана

        # Рисуем все плитки
        for tile in tile_group:
            tile.draw(screen)

        # # Рисуем игрока
        # screen.blit(player.image, player.rect)
        button_start.draw(screen)
        py.display.flip()  # Обновление экрана

