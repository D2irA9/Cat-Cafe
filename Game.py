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

    # Кнопки
    start = Button("Начать рабочий день", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185))
    go_to_market = Button("Идти на рынок", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))

    # Игрок
    player = Player((130, 310), scale=4)
    all_sprites = py.sprite.Group(player)

    clock = py.time.Clock()

    # Состояние игры
    is_working_day = False
    is_market_day = False
    start_button_completed = False  # Флаг завершения логики первой кнопки
    camera_y = 0
    target_camera_y = 960  # Смещение для первой кнопки
    target_camera_y_market = 1920  # Смещение для второй кнопки
    player_path = [(65, 310), (65, 600), (30, 600), (30, 940), (320, 940), (320, 1070), (250, 1070)]  # Путь для первой кнопки
    player_path_market = [(250, 1070), (450, 1070), (450, 2080), (230, 2080)]  # Путь для второй кнопки
    current_path_index = 0

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if not start_button_completed and not is_market_day and start.is_clicked(event.pos):
                    is_working_day = True
                    current_path_index = 0  # Сброс индекса пути для первой кнопки
                elif start_button_completed and not is_market_day and go_to_market.is_clicked(event.pos):
                    is_market_day = True
                    current_path_index = 0  # Сброс индекса пути для второй кнопки

        if is_working_day:
            # Движение игрока
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

            # Движение камеры
            if camera_y < target_camera_y:
                camera_y += 5

            # Проверка завершения логики
            if current_path_index >= len(player_path) and camera_y >= target_camera_y:
                is_working_day = False
                start_button_completed = True
                player.direction = "inaction"  # Сброс анимации на "inaction"

        elif is_market_day:
            # Движение игрока
            if current_path_index < len(player_path_market):
                target_x, target_y = player_path_market[current_path_index]
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

            # Движение камеры
            if camera_y < target_camera_y_market:
                camera_y += 5

            # Проверка завершения логики
            if current_path_index >= len(player_path_market) and camera_y >= target_camera_y_market:
                is_market_day = False  # Завершение логики второй кнопки
                player.direction = "inaction"  # Сброс анимации на "inaction"

        all_sprites.update()

        screen.fill(WHITE)

        # Отрисовка с учетом смещения камеры
        for tile in tile_group:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y - camera_y))
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y - camera_y))

        # Отрисовка кнопки в зависимости от состояния
        if not is_working_day and not is_market_day and not start_button_completed:
            start.draw(screen)
        elif start_button_completed and not is_market_day:
            go_to_market.draw(screen)

        py.display.flip()
        clock.tick(60)

