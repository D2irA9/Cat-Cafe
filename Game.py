import pygame as py
import sys
import random
from pytmx.util_pygame import load_pygame
from Drawing import Tile
from Button import Button
from Player import Player
from NPS import NPC

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
    return_button = Button("Вернуться", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))

    # Игрок
    player = Player((130, 310), scale=4)
    all_sprites = py.sprite.Group(player)

    # Список возможных NPC
    npc_data = [
        {"name": "Lyubava", "sprite": "Sprite/client/Lyubava.png"},
        {"name": "Panteleimon", "sprite": "Sprite/client/Panteleimon.png"},
        {"name": "Vasiliy", "sprite": "Sprite/client/Vasiliy.png"},
        {"name": "Khariton", "sprite": "Sprite/client/Khariton.png"},
        {"name": "Nona", "sprite": "Sprite/client/Nona.png"},
        {"name": "Yevsey", "sprite": "Sprite/client/Yevsey.png"},
        {"name": "Kostya", "sprite": "Sprite/client/Kostya.png"},
        {"name": "Viola", "sprite": "Sprite/client/Viola.png"},
    ]
    available_npcs = npc_data.copy()

    # Возможные стартовые позиции и пути
    start_positions = [(-24, y) for y in [1750, 1740, 1730]] + [(640, y) for y in [1750, 1740, 1730]]
    possible_paths = [
        [start, (640 if start[0] == -24 else -24, start[1]), start]
        for start in start_positions
    ]

    # Таймер и активные NPC
    npc_spawn_timer = 0
    npc_spawn_interval = 5000
    active_npcs = []

    def spawn_random_npc():
        """Создает уникального NPC"""
        if len(active_npcs) < 3 and available_npcs:
            npc_info = random.choice(available_npcs)
            start_pos = random.choice(start_positions)
            path = random.choice([p for p in possible_paths if p[0] == start_pos])

            new_npc = NPC(start_pos, scale, npc_info["sprite"], path)
            new_npc.info = npc_info
            all_sprites.add(new_npc)
            active_npcs.append(new_npc)
            available_npcs.remove(npc_info)

            if not available_npcs:
                available_npcs.extend(npc_data)

    def remove_completed_npcs():
        """Удаляет завершивших путь NPC"""
        for npc in active_npcs[:]:
            if hasattr(npc, 'path_completed') and npc.path_completed:
                all_sprites.remove(npc)
                active_npcs.remove(npc)
                if npc.info not in available_npcs:
                    available_npcs.append(npc.info)

    clock = py.time.Clock()
    game_states = {
        "is_working_day": False,
        "is_market_day": False,
        "start_button_completed": False,
        "return_button_shown": False,
        "camera_y": 0,
        "target_camera_y": 960,
        "target_camera_y_market": 1920,
        "player_path": [(65, 310), (65, 600), (30, 600), (30, 940), (320, 940), (320, 1070), (250, 1070)],
        "player_path_market": [(250, 1070), (450, 1070), (450, 2080), (230, 2080)],
        "current_path_index": 0,
    }

    def handle_movement(player, path, camera_y, target_camera_y):
        """Обработка движения игрока и камеры"""
        if game_states["current_path_index"] < len(path):
            target_x, target_y = path[game_states["current_path_index"]]
            if player.rect.x < target_x:
                player.move("right")
            elif player.rect.x > target_x:
                player.move("left")
            elif player.rect.y < target_y:
                player.move("down")
            elif player.rect.y > target_y:
                player.move("up")
            else:
                game_states["current_path_index"] += 1

        if camera_y < target_camera_y:
            game_states["camera_y"] += 5

        return game_states["current_path_index"] >= len(path) and camera_y >= target_camera_y

    while True:
        current_time = py.time.get_ticks()

        # Управление появлением NPC
        if current_time - npc_spawn_timer > npc_spawn_interval:
            spawn_random_npc()
            npc_spawn_timer = current_time

        remove_completed_npcs()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if not game_states["start_button_completed"] and not game_states["is_market_day"] and start.is_clicked(
                        event.pos):
                    game_states["is_working_day"] = True
                    game_states["current_path_index"] = 0
                elif game_states["start_button_completed"] and not game_states[
                    "is_market_day"] and go_to_market.is_clicked(event.pos):
                    game_states["is_market_day"] = True
                    game_states["current_path_index"] = 0
                elif game_states["return_button_shown"] and return_button.is_clicked(event.pos):
                    # Логика для кнопки "Вернуться"
                    game_states["is_market_day"] = False
                    game_states["return_button_shown"] = False
                    # Сброс позиции игрока и камеры
                    player.rect.topleft = (130, 310)
                    game_states["camera_y"] = 0
                    game_states["current_path_index"] = 0

        # Обработка состояний игры
        if game_states["is_working_day"] and handle_movement(player, game_states["player_path"],
                                                             game_states["camera_y"], game_states["target_camera_y"]):
            game_states["is_working_day"] = False
            game_states["start_button_completed"] = True
            player.direction = "inaction"

        elif game_states["is_market_day"] and handle_movement(player, game_states["player_path_market"],
                                                              game_states["camera_y"],
                                                              game_states["target_camera_y_market"]):
            game_states["is_market_day"] = False
            game_states["return_button_shown"] = True
            player.direction = "inaction"

        all_sprites.update()
        screen.fill(WHITE)

        # Отрисовка
        for tile in tile_group:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y - game_states["camera_y"]))
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y - game_states["camera_y"]))

        # Отрисовка кнопок
        if not game_states["is_working_day"] and not game_states["is_market_day"]:
            if not game_states["start_button_completed"]:
                start.draw(screen)
            elif not game_states["return_button_shown"]:
                go_to_market.draw(screen)

        # Отрисовка кнопки "Вернуться"
        if game_states["return_button_shown"]:
            return_button.draw(screen)

        py.display.flip()
        clock.tick(60)

