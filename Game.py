import pygame as py
import sys
from pytmx.util_pygame import load_pygame
from Drawing import Tile
from Player import Player
from Button import Button
from Camera import Camera


def game():
    """Запуск игры"""
    py.init()

    screen = py.display.set_mode((640, 960))
    py.display.set_caption("Cat-Cafe")

    # Загруска карты
    map = load_pygame("Map/map.tmx")
    tile_group = py.sprite.Group()
    player_group = py.sprite.Group()

    TILE_SIZE = 16
    scale = 4

    for layer in map.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                Tile(pos=pos, surf=surf, groups=tile_group, scale=scale)

    camera = Camera(640, 960)

    sprite_sheet = py.image.load("Sprite/Player/Player.png").convert_alpha()

    animations = {
        "inaction": [
            py.transform.scale(sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((48, 0, 48, 48)), (48 * scale, 48 * scale))
        ],
        "up": [
            py.transform.scale(sprite_sheet.subsurface((0, 48, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((144, 48, 48, 48)), (48 * scale, 48 * scale))
        ],
        "down": [
            py.transform.scale(sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((144, 0, 48, 48)), (48 * scale, 48 * scale))
        ],
        "left": [
            py.transform.scale(sprite_sheet.subsurface((0, 96, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((144, 96, 48, 48)), (48 * scale, 48 * scale))
        ],
        "right": [
            py.transform.scale(sprite_sheet.subsurface((0, 144, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((144, 144, 48, 48)), (48 * scale, 48 * scale))
        ]
    }

    player = Player(pos=(140, 300), animations=animations, groups=player_group)

    WHITE = (255, 255, 255)

    clock = py.time.Clock()
    button_start = Button("Начать рабочий день", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185))

    camera_moving = False  # Флаг для отслеживания движения камеры

    while True:
        dt = clock.tick(60) / 1000.0

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            # Проверка на нажатие
            if event.type == py.MOUSEBUTTONDOWN and button_start.rect.collidepoint(event.pos):
                player.start_day(screen, tile_group, player)
                button_start.visible = False
                camera_moving = True  # Начинаем движение камеры

        # Обновляем плитки
        tile_group.update()

        # Обновляем анимацию игрока
        player.update(dt)

        # Двигаем камеру, если это необходимо
        if camera_moving:
            camera.update(960)  # Двигаем камеру вниз на высоту окна
            # Проверяем, достигла ли камера целевой позиции
            if camera.camera.y >= 960:  # Если камера достигла или превысила целевую позицию
                camera.camera.y = 960  # Устанавливаем её на целевую позицию
                camera_moving = False  # Останавливаем движение камеры

        # Рисуем все плитки
        screen.fill(WHITE)
        for tile in tile_group:
            screen.blit(tile.image, camera.apply(tile))

        # Рисуем игрока
        screen.blit(player.image, camera.apply(player))

        if button_start.visible:
            button_start.draw(screen)
        py.display.flip()