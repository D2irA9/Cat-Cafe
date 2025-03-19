import pygame as py
import sys
from pytmx.util_pygame import load_pygame
from Drawing import Tile
from Player import Player
from Button import Button
from Camera import Camera

def Game(WHITE, BLACK):
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
    camera_moving = False
    camera_target_y = 0  # Целевая позиция камеры

    sprite_sheet = py.image.load("Sprite/Player/Player.png").convert_alpha()
    animations = {
        "inaction": [py.transform.scale(sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
                     py.transform.scale(sprite_sheet.subsurface((48, 0, 48, 48)), (48 * scale, 48 * scale))],
        "up": [py.transform.scale(sprite_sheet.subsurface((0, 48, 48, 48)), (48 * scale, 48 * scale)),
               py.transform.scale(sprite_sheet.subsurface((144, 48, 48, 48)), (48 * scale, 48 * scale))],
        "down": [py.transform.scale(sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
                 py.transform.scale(sprite_sheet.subsurface((144, 0, 48, 48)), (48 * scale, 48 * scale))],
        "left": [py.transform.scale(sprite_sheet.subsurface((0, 96, 48, 48)), (48 * scale, 48 * scale)),
                 py.transform.scale(sprite_sheet.subsurface((144, 96, 48, 48)), (48 * scale, 48 * scale))],
        "right": [py.transform.scale(sprite_sheet.subsurface((0, 144, 48, 48)), (48 * scale, 48 * scale)),
                  py.transform.scale(sprite_sheet.subsurface((144, 144, 48, 48)), (48 * scale, 48 * scale))]
    }

    player = Player(pos=(140, 300), animations=animations, groups=player_group)

    # Пути для игрока
    paths = {
        "start": [("left", 75), ("down", 300), ("left", 50), ("down", 340), ("right", 310), ("down", 110), ("left", 100)],
        "go_store": [("right", 100), ("down", 400), ("left", 150), ("down", 300)]
    }

    buttons = {
        "start": Button("Начать рабочий день", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185)),
        "go_store": Button("Идти на рынок", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152)),
        "return": Button("Вернуться", 135, 2680, 350, 100, (0, 0, 0), (255, 218, 185)),
        "open": Button("Открыться", 135, 1720, 350, 100, (0, 0, 0), (244, 164, 96))
    }
    buttons["go_store"].visible = False

    clock = py.time.Clock()

    # Флаги для управления движением игрока и камеры
    player_moving = False
    current_path_index = 0
    moved_distance = 0
    current_path = []  # Текущий путь игрока

    while True:
        dt = clock.tick(60) / 1000.0

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.KEYDOWN and event.key in (py.K_LALT, py.K_RALT):
                py.quit()
                sys.exit()

            if buttons["start"].is_clicked() and not player_moving:
                camera_moving, camera_target_y = True, 960
                buttons["start"].visible = False
                player_moving, current_path = True, paths["start"]
                current_path_index, moved_distance = 0, 0

            if buttons["go_store"].is_clicked() and not player_moving:
                camera_moving, camera_target_y = True, 1920  # Устанавливаем целевую позицию камеры
                buttons["go_store"].visible = False  # Скрываем кнопку после нажатия
                player_moving, current_path = True, paths["go_store"]
                current_path_index, moved_distance = 0, 0

        # Движение камеры
        if camera_moving:
            camera.pos.y += camera.speed
            if camera.pos.y >= camera_target_y:
                camera.pos.y = camera_target_y  # Устанавливаем позицию камеры на целевую
                camera_moving = False
                if camera_target_y == 960:
                    buttons["go_store"].visible = True  # Показываем кнопку "Идти на рынок"
                elif camera_target_y == 1920:
                    buttons["return"].visible = True  # Показываем кнопку "Вернуться"

        # Движение игрока
        if player_moving and current_path_index < len(current_path):
            direction, distance = current_path[current_path_index]
            player.current_animation = direction

            if moved_distance < distance:
                if direction == "right":
                    player.rect.x += player.speed
                elif direction == "down":
                    player.rect.y += player.speed
                elif direction == "left":
                    player.rect.x -= player.speed
                elif direction == "up":
                    player.rect.y -= player.speed

                moved_distance += player.speed
            else:
                moved_distance, current_path_index = 0, current_path_index + 1

            if current_path_index >= len(current_path):
                player_moving = False
                player.current_animation = "inaction"

        # Обновление спрайтов
        tile_group.update()
        player.update(dt)

        # Отрисовка
        screen.fill(WHITE)
        for tile in tile_group:
            screen.blit(tile.image, camera.apply(tile))
        screen.blit(player.image, camera.apply(player))

        # Отрисовка кнопок
        for button in buttons.values():
            if button.visible:
                button.draw(screen)

        py.display.flip()