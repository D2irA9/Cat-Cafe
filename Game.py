import pygame as py
import sys
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

    # NPC
    npc_path = [(200, 310), (200, 400), (300, 400), (300, 310)]  # Пример маршрута для NPC
    Lyubava = NPC((200, 310), scale, "Sprite/client/Lyubava.png", npc_path)  # Путь к спрайтам NPC
    all_sprites.add(Lyubava)  # Добавляем NPC в группу спрайтов
    sprite_sheet = py.image.load("Sprite/client/Lyubava.png").convert_alpha()
    print(sprite_sheet.get_size())  # Выведет (96, 96), если размеры правильные

    clock = py.time.Clock()

    # Состояние игры
    game_states = {
        "is_working_day": False,
        "is_market_day": False,
        "start_button_completed": False,
        "camera_y": 0,
        "target_camera_y": 960,
        "target_camera_y_market": 1920,
        "player_path": [(65, 310), (65, 600), (30, 600), (30, 940), (320, 940), (320, 1070), (250, 1070)],
        "player_path_market": [(250, 1070), (450, 1070), (450, 2080), (230, 2080)],
        "current_path_index": 0
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

        # Проверка завершения логики
        if game_states["current_path_index"] >= len(path) and camera_y >= target_camera_y:
            return True
        return False

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if not game_states["start_button_completed"] and not game_states["is_market_day"] and start.is_clicked(event.pos):
                    game_states["is_working_day"] = True
                    game_states["current_path_index"] = 0
                elif game_states["start_button_completed"] and not game_states["is_market_day"] and go_to_market.is_clicked(event.pos):
                    game_states["is_market_day"] = True
                    game_states["current_path_index"] = 0

        if game_states["is_working_day"]:
            if handle_movement(player, game_states["player_path"], game_states["camera_y"], game_states["target_camera_y"]):
                game_states["is_working_day"] = False
                game_states["start_button_completed"] = True
                player.direction = "inaction"

        elif game_states["is_market_day"]:
            if handle_movement(player, game_states["player_path_market"], game_states["camera_y"], game_states["target_camera_y_market"]):
                game_states["is_market_day"] = False
                player.direction = "inaction"

        all_sprites.update()

        screen.fill(WHITE)

        # Отрисовка с учетом смещения камеры
        for tile in tile_group:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y - game_states["camera_y"]))
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y - game_states["camera_y"]))

        # Отрисовка кнопки в зависимости от состояния
        if not game_states["is_working_day"] and not game_states["is_market_day"] and not game_states["start_button_completed"]:
            start.draw(screen)
        elif game_states["start_button_completed"] and not game_states["is_market_day"]:
            go_to_market.draw(screen)

        py.display.flip()
        clock.tick(60)
