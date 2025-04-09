import pygame as py
import sys
import random
from pytmx.util_pygame import load_pygame
from Drawing import Tile
from Button import Button
from Player import Player
from NPS import NPC
from Food import Food
from CoinDisplay import CoinDisplay
from DayDisplay import DayDisplay
from Player_data import clear_player_data
from Sql import Database
import Home_screen

py.init()
font = py.font.Font("Font/PixelizerBold.ttf", 36)
def exit_confirmation_screen():
    """Экран подтверждения выхода из игры"""
    exit_screen = py.display.set_mode((600, 900))
    py.display.set_caption("Подтверждение выхода")

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Кнопки
    button_yes = Button("Да", 135, 360, 350, 100, BLACK, (220, 20, 60))
    button_login_another = Button("Войти в другой аккаунт", 120, 480, 380, 100, BLACK, (152, 251, 152))
    button_no = Button("Нет", 135, 600, 350, 100, BLACK, (30, 144, 255))

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = py.mouse.get_pos()

                if button_yes.is_clicked(mouse_pos):
                    py.quit()
                    sys.exit()

                if button_login_another.is_clicked(mouse_pos):
                    clear_player_data()
                    Home_screen.Home_screen()
                    return

                if button_no.is_clicked(mouse_pos):
                    return

        exit_screen.fill(BLACK)

        header_surface = font.render("Выйти из игры?", True, WHITE)
        header_rect = header_surface.get_rect(center=(exit_screen.get_width() // 2, 50))
        exit_screen.blit(header_surface, header_rect)

        # Отрисовка кнопок
        button_yes.draw(exit_screen)
        button_login_another.draw(exit_screen)
        button_no.draw(exit_screen)

        py.display.flip()

def Game(player_id, player_email, player_balance, player_name):
    """Игра"""
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

    # Монеты
    coin_display = CoinDisplay()

    # Дни
    db = Database()
    db.connect()
    result = db.execute_query("SELECT `day` FROM `player` WHERE id=%s", (player_id))
    player_day = result[0][0] if result and len(result) > 0 else 0
    day_display = DayDisplay((500, 10), (120, 60), player_day)

    # Кнопки
    start = Button("Начать рабочий день", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185))
    go_to_market = Button("Купить", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))
    return_button = Button("Вернуться", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))
    open_caff = Button("Открыть кафе", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))

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

    # Подключаемся к БД
    menu_prices = db.get_menu_items()

    used_npcs = []
    used_foods = []

    def get_random_npc():
        """Получает случайного NPC, который еще не был использован"""
        available_npcs = [npc for npc in npc_data if npc not in used_npcs]
        if available_npcs:
            npc = random.choice(available_npcs)
            used_npcs.append(npc)
            return npc
        return None

    def get_random_food():
        """Получает случайную еду, которая еще не была использована"""
        available_foods = [food for food in menu_prices.keys() if food not in used_foods]
        if available_foods:
            food = random.choice(available_foods)
            used_foods.append(food)
            return food
        return None

    if not menu_prices:
        menu_prices = {
            "Pasta": 51, "Tacos": 17, "Ramen": 33, "Hamburg": 29,
            "Pizza": 41, "Rolls": 31, "Soup": 19, "Fried_egg": 11,
            "Water": 5, "Cocoa": 16, "Tea": 12, "Milkshake": 20,
            "Coffee": 17, "Cocktail": 18, "Lemonade": 15, "Soda": 15,
            "Cupcake": 19, "Cheesecake": 23, "Cake": 25, "Ice_cream": 25, "Pie": 30
        }

    food_group = py.sprite.Group()
    inventory = {food_type: 0 for food_type in menu_prices}

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
            if hasattr(npc, "path_completed") and npc.path_completed:
                all_sprites.remove(npc)
                active_npcs.remove(npc)
                if npc.info not in available_npcs:
                    available_npcs.append(npc.info)

    def show_market(player_id, player_email, player_balance, player_name):
        """Отображение рынка"""
        market_screen = py.display.set_mode((640, 960))
        py.display.set_caption("Рынок")

        # Загруска карты рынка
        market_map = load_pygame("Map/Market.tmx")
        market_tile_group = py.sprite.Group()

        # Вытаскивание всех слоёв карты
        for layer in market_map.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                    Tile(pos=pos, surf=surf, groups=market_tile_group, scale=scale)

        # Кнопка "Вернуться"
        return_button = Button("Вернуться", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))

        # Позиции для NPC и еды
        spawn_points = [
            (110, 140),
            (370, 140),
            (110, 400),
            (370, 400)
        ]

        food_group.empty()  # Очищаем группу еды перед добавлением новой

        # Создаем NPC
        trader_npcs = [
            {"name": "Lyubava", "sprite": "Sprite/client/Lyubava.png"},
            {"name": "Panteleimon", "sprite": "Sprite/client/Panteleimon.png"},
            {"name": "Vasiliy", "sprite": "Sprite/client/Vasiliy.png"},
            {"name": "Khariton", "sprite": "Sprite/client/Khariton.png"},
            {"name": "Nona", "sprite": "Sprite/client/Nona.png"},
            {"name": "Yevsey", "sprite": "Sprite/client/Yevsey.png"},
        ]

        for pos in spawn_points:
            food_type = get_random_food()  # Получаем случайную еду
            if food_type is None:
                continue  # Если еды больше нет, пропускаем

            quantity = random.randint(1, 5)
            price = menu_prices[food_type]

            # Создаем еду
            new_food = Food((pos[0] + 45, pos[1] + 150), food_type, scale=3, quantity=quantity, price=price)
            food_group.add(new_food)

            # Создаем NPC только из списка торговцев
            npc_info = random.choice(trader_npcs)
            npc_pos = (pos[0], pos[1])
            new_npc = NPC(npc_pos, scale, npc_info["sprite"], [npc_pos])
            new_npc.is_market_npc = True
            all_sprites.add(new_npc)  # Добавляем NPC в группу всех спрайтов

        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()

                if event.type == py.MOUSEBUTTONDOWN:
                    if return_button.is_clicked(event.pos):
                        return

                    # Проверка кликов по еде
                    for food in food_group:
                        if food.is_clicked(event.pos):
                            if player_balance >= food.price:
                                player_balance -= food.price
                                inventory[food.type] += 1
                                food.decrease_quantity()  # Уменьшаем количество еды
                                food.update_ui()  # Обновляем интерфейс еды
                                # Обновление баланса
                                if db.check_player_exists(player_id):
                                    db.update_balance(player_id, player_balance)

                market_screen.fill(WHITE)

                # Отрисовка плиток
                for tile in market_tile_group:
                    market_screen.blit(tile.image, (tile.rect.x, tile.rect.y))

                # Отрисовка NPC
                for npc in all_sprites:
                    if isinstance(npc, NPC):
                        market_screen.blit(npc.image, npc.rect.topleft)

                # Отрисовка еды
                food_group.update()
                for food in food_group:
                    food.draw(market_screen, 0)

                # Отрисовка кнопки "Вернуться"
                return_button.draw(market_screen)

                # Обновляем и рисуем монеты и дни
                coin_display.update()
                coin_display.draw(market_screen, player_balance)
                day_display.draw(market_screen)

                py.display.flip()
                clock.tick(60)

    clock = py.time.Clock()
    game_states = {
        "is_working_day": False,
        "is_market_day": False,
        "is_returning": False,
        "is_open": False,

        "start_button_show": False,
        "return_button_show": False,
        "open_button_show": False,

        "camera_y": 0,
        "target_camera_y": 960,
        "target_camera_y_market": 1920,

        "player_path": [(65, 310), (65, 600), (30, 600), (30, 940), (320, 940), (320, 1070), (250, 1070)],
        "player_path_market": [(250, 1070), (450, 1070), (450, 2080), (230, 2080)],
        "player_path_return_caf": [(230, 2080), (230, 1070), (250, 1070)],
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

        # Обновление позиции камеры
        if camera_y < target_camera_y:
            game_states["camera_y"] += 5
        if camera_y > target_camera_y:
            game_states["camera_y"] -= 5
        return game_states["current_path_index"] >= len(path) and abs(camera_y - target_camera_y) < 5


    while True:
        current_time = py.time.get_ticks()

        # Управление появлением NPC
        if current_time - npc_spawn_timer > npc_spawn_interval:
            spawn_random_npc()
            npc_spawn_timer = current_time

        remove_completed_npcs()

        for event in py.event.get():
            if event.type == py.QUIT:
                db.close()
                py.quit()
                sys.exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    exit_confirmation_screen()

            if event.type == py.MOUSEBUTTONDOWN:
                # Проверка клики по кнопкам
                if not game_states["start_button_show"] and not game_states["is_market_day"] and start.is_clicked(event.pos):
                    game_states["is_working_day"] = True
                    game_states["current_path_index"] = 0
                # Идти на рынок
                if game_states["start_button_show"] and not game_states["is_market_day"] and go_to_market.is_clicked(
                        event.pos):
                    show_market(player_id, player_email, player_balance, player_name)
                # Вернутся
                elif game_states["return_button_show"] and return_button.is_clicked(event.pos):
                    game_states["is_returning"] = True
                    game_states["return_button_show"] = False
                    game_states["current_path_index"] = 0
                    game_states["target_camera_y"] = 960

                    # Очищаем еду и NPC рынка
                    for food in food_group:
                        food.kill()
                    for npc in [n for n in active_npcs if hasattr(n, "is_market_npc")]:
                        npc.kill()

                elif game_states["open_button_show"] and open_caff.is_clicked(event.pos):
                    print("Кафе открыто!")
                    game_states["current_path_index"] = 0

                if game_states["is_market_day"] or game_states["return_button_show"]:
                    for food in food_group:
                        if food.is_clicked(event.pos, game_states["camera_y"]):
                            if player_balance >= food.price:
                                player_balance -= food.price
                                inventory[food.type] += 1
                                food.quantity -= 1
                                if food.quantity <= 0:
                                    food.kill()
                                else:
                                    food.update_ui()

        # Начать рабочий день
        if game_states["is_working_day"]:
            if handle_movement(player, game_states["player_path"], game_states["camera_y"], game_states["target_camera_y"]):
                game_states["is_working_day"] = False
                game_states["start_button_show"] = True
                player.direction = "inaction"
        # Купить
        elif game_states["is_market_day"]:
            if handle_movement(player, game_states["player_path_market"], game_states["camera_y"], game_states["target_camera_y_market"]):
                game_states["is_market_day"] = False
                game_states["return_button_show"] = True
                player.direction = "inaction"
        # Вернутся
        elif game_states["is_returning"]:
            if handle_movement(player, game_states["player_path_return_caf"], game_states["camera_y"], 960):
                game_states["is_returning"] = False
                game_states["open_button_show"] = True
                player.direction = "inaction"
                game_states["camera_y"] = 960
        # Открыть кафе
        elif game_states["is_open"]:
            game_states["open_button_show"] = False
            player.direction = "inaction"

        all_sprites.update()
        screen.fill(WHITE)

        # Отрисовка карты
        for tile in tile_group:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y - game_states["camera_y"]))
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y - game_states["camera_y"]))

        # Отрисовка кнопок
        if not game_states["is_working_day"] and not game_states["is_market_day"]:
            if not game_states["start_button_show"]:
                start.draw(screen)
            elif game_states["open_button_show"]:
                open_caff.draw(screen)
            elif not game_states["return_button_show"]:
                go_to_market.draw(screen)
        if game_states["return_button_show"]:
            return_button.draw(screen)

        # Отрисовка еды
        food_group.update()
        for food in food_group:
            food.draw(screen, game_states["camera_y"])

        # Монеты и дни
        coin_display.update()
        coin_display.draw(screen, player_balance)
        day_display.draw(screen)

        py.display.flip()
        clock.tick(60)
