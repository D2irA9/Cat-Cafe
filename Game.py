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

    start = Button("Начать рабочий день", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185))

    # Игрок
    player = Player((130, 310), scale=4)
    all_sprites = py.sprite.Group(player)

    clock = py.time.Clock()

    # Состояние игры
    is_working_day = False
    camera_y = 0
    target_camera_y = 960
    player_path = [(65, 310), (65, 600), (30, 600), (30, 940), (320, 940), (320, 1070), (250, 1070)]  # Пример пути
    current_path_index = 0

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if start.is_clicked(event.pos):
                    is_working_day = True

        if is_working_day:
            if current_path_index < len(player_path):
                target_x, target_y = player_path[current_path_index]
                if player.rect.x < target_x:
                    player.move("right")
                elif player.rect.x > target_x:
                    player.move("left")
                elif player.rect.y < target_y:
                    player.move("down")
                elif player.rect.y > target_y:
                    player.move("up")
                else:
                    current_path_index += 1
            else:
                if camera_y < target_camera_y:
                    camera_y += 5

        all_sprites.update()

        screen.fill(WHITE)

        # Отрисовка с учетом смещения камеры
        for tile in tile_group:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y - camera_y))
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y - camera_y))

        start.draw(screen)

        py.display.flip()
        clock.tick(60)
