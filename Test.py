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
from Sql import Database
import Home_screen

db = Database()
db.connect()

py.init()
clock = py.time.Clock()
font = py.font.Font("Font/PixelizerBold.ttf", 36)

purchased_items = []
current_screen = "home"

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# vfinj,bhjdfybt
TILE_SIZE = 16
scale = 4
# Меню
menu_prices = db.get_menu_items()
if not menu_prices:
    menu_prices = {
        "Pasta": 51, "Tacos": 17, "Ramen": 33, "Hamburg": 29,
        "Pizza": 41, "Rolls": 31, "Soup": 19, "Fried_egg": 11,
        "Water": 5, "Cocoa": 16, "Tea": 12, "Milkshake": 20,
        "Coffee": 17, "Cocktail": 18, "Lemonade": 15, "Soda": 15,
        "Cupcake": 19, "Cheesecake": 23, "Cake": 25, "Ice_cream": 25, "Pie": 30
    }
used_foods = []
food_group = py.sprite.Group()
inventory = {food_type: 0 for food_type in menu_prices}

def get_random_food():
    """Получает случайную еду, которая еще не была использована"""
    available_foods = [food for food in menu_prices.keys() if food not in used_foods]
    if available_foods:
        food = random.choice(available_foods)
        used_foods.append(food)
        return food
    return None

def exit_confirmation_screen():
    """Экран подтверждения выхода из игры"""
    exit_screen = py.display.set_mode((600, 900))
    py.display.set_caption("Подтверждение выхода")

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
                    global all_sprites, tile_group, food_group
                    all_sprites.empty()
                    tile_group.empty()
                    food_group.empty()
                    db.close()
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


def show_market(player_id, player_email, player_balance, player_name):
    global used_foods, purchased_items
    used_foods = []
    purchased_items = []
    """Отображение рынка с эффектами плавного появления и затемнения"""
    market_screen = py.display.set_mode((640, 960))
    py.display.set_caption("Рынок")

    # Настройки эффектов
    fade_surface = py.Surface((640, 960))
    fade_surface.fill(BLACK)

    # Эффект появления: начинаем с черного экрана
    fade_alpha = 255
    fade_in_speed = 3

    # Эффект исчезновения (для перехода в кафе)
    fading_out = False
    fade_out_speed = 5

    # Кнопка возврата
    return_button = Button("В кафе", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))

    # Загрузка всех объектов рынка (как в вашем оригинальном коде)
    market_map = load_pygame("Map/Market.tmx")
    market_tile_group = py.sprite.Group()
    all_sprites = py.sprite.Group()
    coin_display = CoinDisplay()

    # Загрузка дней
    result = db.execute_query("SELECT `day` FROM `player` WHERE id=%s", (player_id))
    player_day = result[0][0] if result and len(result) > 0 else 0
    day_display = DayDisplay((500, 10), (120, 60), player_day)

    # Загрузка тайлов карты
    for layer in market_map.visible_layers:
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                Tile(pos=pos, surf=surf, groups=market_tile_group, scale=scale)

    # Создание NPC и еды (как в оригинале)
    spawn_points = [(110, 140), (370, 140), (110, 400), (370, 400)]
    food_group = py.sprite.Group()
    used_npcs = []

    trader_npcs = [
        {"name": "Lyubava", "sprite": "Sprite/client/Lyubava.png"},
        {"name": "Panteleimon", "sprite": "Sprite/client/Panteleimon.png"},
        {"name": "Vasiliy", "sprite": "Sprite/client/Vasiliy.png"},
        {"name": "Khariton", "sprite": "Sprite/client/Khariton.png"},
        {"name": "Nona", "sprite": "Sprite/client/Nona.png"},
        {"name": "Yevsey", "sprite": "Sprite/client/Yevsey.png"},
    ]
    random.shuffle(trader_npcs)
    for i, pos in enumerate(spawn_points):
        food_type = get_random_food()
        if food_type is None:
            continue

        quantity = random.randint(1, 5)
        price = menu_prices[food_type]

        # Создаем еду
        new_food = Food((pos[0] + 45, pos[1] + 150), food_type, scale=3, quantity=quantity, price=price)
        food_group.add(new_food)

        # Берем NPC по порядку из перемешанного списка
        if i < len(trader_npcs):
            npc_info = trader_npcs[i]
        else:
            # Если NPC меньше чем точек спавна, берем случайного
            npc_info = random.choice(trader_npcs)

        # Создаем NPC
        new_npc = NPC((pos[0], pos[1]), scale, npc_info["sprite"], [(pos[0], pos[1])])
        new_npc.is_market_npc = True
        all_sprites.add(new_npc)

    # Основной цикл
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                if return_button.is_clicked(event.pos) and not fading_out and fade_alpha <= 0:
                    fading_out = True

                # Обработка покупок (только когда видно экран)
                if fade_alpha <= 0 and not fading_out:
                    for food in food_group:
                        if food.is_clicked(event.pos) and player_balance >= food.price:
                            player_balance -= food.price
                            inventory[food.type] += 1
                            food.decrease_quantity()
                            food.update_ui()
                            purchased_items.append({
                                "name": food.type,
                                "price": food.price,
                                "time": py.time.get_ticks()
                            })
                            if db.check_player_exists(player_id):
                                db.update_balance(player_id, player_balance)

        # Логика эффектов
        if not fading_out:
            if fade_alpha > 0:
                fade_alpha = max(0, fade_alpha - fade_in_speed)
        else:
            fade_alpha = min(255, fade_alpha + fade_out_speed)
            if fade_alpha == 255:
                if db.check_player_exists(player_id):
                    db.update_balance(player_id, player_balance)
                py.display.quit()
                open_cafe_win(player_id, player_email, player_balance, player_name)

                # running = False
                return

        # Отрисовка
        market_screen.fill(WHITE)

        # Отрисовка объектов рынка
        market_tile_group.draw(market_screen)
        for npc in all_sprites:
            if isinstance(npc, NPC):
                market_screen.blit(npc.image, npc.rect.topleft)

        food_group.update()
        for food in food_group:
            food.draw(market_screen, 0)

        return_button.draw(market_screen)
        coin_display.draw(market_screen, player_balance)
        day_display.draw(market_screen)

        # Наложение эффектов
        if fade_alpha > 0:
            fade_surface.set_alpha(fade_alpha)
            market_screen.blit(fade_surface, (0, 0))

        py.display.flip()
        clock.tick(60)

class FoodIndicator(py.sprite.Sprite):
    def __init__(self, npc, food_type):
        super().__init__()
        self.npc = npc
        self.food_type = food_type

        # Создаем временный объект Food для получения спрайта
        temp_food = Food((0, 0), food_type, scale=2)  # Масштаб 2 для лучшей видимости

        # Создаем основное изображение индикатора
        self.image = py.Surface((50, 50), py.SRCALPHA)

        # Рисуем круг с темным контуром
        py.draw.circle(self.image, (255, 255, 255), (25, 25), 22)
        py.draw.circle(self.image, (50, 50, 50), (25, 25), 22, 2)

        # Размещаем спрайт еды по центру
        food_img = temp_food.image
        food_rect = food_img.get_rect(center=(25, 25))
        self.image.blit(food_img, food_rect)

        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        # Позиционируем над NPC
        self.rect.centerx = self.npc.rect.centerx
        self.rect.bottom = self.npc.rect.top - 5

    def is_clicked(self, pos):
        """Проверяет, был ли клик по индикатору еды"""
        return self.rect.collidepoint(pos)

def open_cafe_win(player_id, player_email, player_balance, player_name):
    """Функция для открытия кафе с NPC клиентами"""
    cafe_screen = py.display.set_mode((640, 960))
    py.display.set_caption("Cat Cafe")

    # Настройки эффекта плавного появления
    fade_surface = py.Surface((640, 960))
    fade_surface.fill(BLACK)
    fade_alpha = 255
    fade_speed = 3

    # Инициализация групп спрайтов
    all_sprites = py.sprite.Group()
    cafe_tile_group = py.sprite.Group()
    npc_group = py.sprite.Group()
    food_indicators = py.sprite.Group()

    # Загрузка карты кафе
    cafe_map = load_pygame("Map/cat-cafe.tmx")

    # Загрузка тайлов
    for layer in cafe_map.visible_layers:
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                Tile(pos=pos, surf=surf, groups=cafe_tile_group, scale=scale)

    # Игрок
    player = Player((60, 180), scale=4)
    all_sprites.add(player)

    # Состояния игры
    class GameState:
        WAITING = 0
        NPC_MOVING = 1
        NPC_WAITING = 2
        PLAYER_MOVING = 3
        PLAYER_MOVING_BACK = 4
        SERVING = 5
        WAIT_BEFORE_DISAPPEAR = 6  # Новое состояние для ожидания перед исчезновением
        FOOD_DISAPPEARING = 7
        NPC_LEAVING = 8

    game_state = GameState.WAITING
    current_npc = None
    player_path = []
    current_target = 0
    wait_timer = 0
    serving_timer = 0
    food_timer = 0  # Таймер для исчезновения еды
    wait_before_disappear_timer = 0  # Таймер для ожидания перед исчезновением
    npc_path_used = None

    # Интерфейс
    coin_display = CoinDisplay()
    result = db.execute_query("SELECT `day` FROM `player` WHERE id=%s", (player_id))
    player_day = result[0][0] if result and len(result) > 0 else 0
    day_display = DayDisplay((500, 10), (120, 60), player_day)
    open_button = Button("Открыть кафе", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185))
    show_open_button = True

    # Настройки NPC
    npc_data = [
        {"name": "Lyubava", "sprite": "Sprite/client/Lyubava.png"},
        {"name": "Panteleimon", "sprite": "Sprite/client/Panteleimon.png"},
        {"name": "Vasiliy", "sprite": "Sprite/client/Vasiliy.png"},
        {"name": "Khariton", "sprite": "Sprite/client/Khariton.png"},
        {"name": "Nona", "sprite": "Sprite/client/Nona.png"},
        {"name": "Yevsey", "sprite": "Sprite/client/Yevsey.png"},
    ]
    # Пути для NPC
    npc_paths_cafe = [
        [(-50, 810), (50, 810), (50, 400), (175, 400)],  # Путь 1
        [(-40, 810), (40, 810), (40, 350), (350, 350), (350, 400)],  # Путь 2
        [(175, 400), (175, 350), (500, 350), (500, 810), (690, 810)], # Для 1 пути
        [(350, 400), (350, 350), (500, 350), (500, 810), (690, 810)], # Для 2 пути
    ]

    def move_player(player, path, current_target):
        """Перемещает игрока по заданному пути."""
        if current_target < len(path):
            target_x, target_y = path[current_target]
            if player.rect.x < target_x:
                player.move("right")
            elif player.rect.x > target_x:
                player.move("left")
            elif player.rect.y < target_y:
                player.move("down")
            elif player.rect.y > target_y:
                player.move("up")
            else:
                return True  # Достигли цели
        return False  # Не достигли цели

    # Основной цикл
    while True:
        current_time = py.time.get_ticks()
        player_balance = db.get_player_balance(player_id)

        # Обработка событий
        for event in py.event.get():
            if event.type == py.QUIT:
                db.close()
                py.quit()
                sys.exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    exit_confirmation_screen()

            if event.type == py.MOUSEBUTTONDOWN and show_open_button:
                if open_button.is_clicked(event.pos):
                    show_open_button = False
                    # Создаем нового NPC
                    npc_info = random.choice(npc_data)
                    path = random.choice(npc_paths_cafe)
                    new_npc = NPC(path[0], scale, npc_info["sprite"], path)
                    npc_group.add(new_npc)
                    game_state = GameState.NPC_MOVING
                    current_npc = new_npc
                    npc_path_used = path

            # Обработка клика по индикатору еды
            if game_state == GameState.NPC_WAITING and event.type == py.MOUSEBUTTONDOWN:
                for indicator in food_indicators:
                    if indicator.is_clicked(event.pos):
                        # Задаем путь игрока к NPC
                        player_path = [
                            (player.rect.x, player.rect.y),
                            (370, player.rect.y), (370, 300), (185, 300)
                        ]
                        current_target = 0
                        game_state = GameState.PLAYER_MOVING

        # Логика состояний игры
        if game_state == GameState.NPC_MOVING:
            if current_npc.path_completed:
                # NPC дошел до конечной точки
                wait_timer = current_time
                game_state = GameState.NPC_WAITING

        elif game_state == GameState.NPC_WAITING:
            # Ждем 2 секунды перед показом индикатора
            if current_time - wait_timer > 2000 and not hasattr(current_npc, 'food_indicator'):
                if purchased_items:  # Проверяем, есть ли купленные товары
                    food_item = random.choice(purchased_items)
                    indicator = FoodIndicator(current_npc, food_item["name"])
                    food_indicators.add(indicator)
                    current_npc.food_indicator = indicator

        elif game_state == GameState.PLAYER_MOVING:
            # Движение игрока к NPC
            if current_target < len(player_path):
                target_x, target_y = player_path[current_target]
                if player.rect.x < target_x:
                    player.move("right")
                elif player.rect.x > target_x:
                    player.move("left")
                elif player.rect.y < target_y:
                    player.move("down")
                elif player.rect.y > target_y:
                    player.move("up")
                else:
                    current_target += 1
            else:
                # Игрок дошел до NPC
                serving_timer = current_time
                player.direction = "inaction"
                game_state = GameState.SERVING

                # Спавн еды в зависимости от пути
                if npc_path_used == npc_paths_cafe[0]:
                    spawn_food_at = (270, 470)
                elif npc_path_used == npc_paths_cafe[1]:
                    spawn_food_at = (340, 470)
                # Создаем объект еды в нужной позиции
                food_item = Food(spawn_food_at, indicator.food_type, scale=2.5)  # Передаем scale
                food_indicators.add(food_item)
                food_timer = current_time

                current_npc.food_indicator.kill()
                del current_npc.food_indicator

                # Создаем обратный путь
                reverse_player_path = player_path[::-1]  # Создаем обратный путь
                current_target = 0  # Сбрасываем текущую цель
                game_state = GameState.PLAYER_MOVING_BACK  # Устанавливаем новое состояние

        elif game_state == GameState.PLAYER_MOVING_BACK:
            # Движение игрока обратно
            if current_target < len(reverse_player_path):
                target_x, target_y = reverse_player_path[current_target]
                if player.rect.x < target_x:
                    player.move("right")
                elif player.rect.x > target_x:
                    player.move("left")
                elif player.rect.y < target_y:
                    player.move("down")
                elif player.rect.y > target_y:
                    player.move("up")
                else:
                    current_target += 1
            else:
                serving_timer = current_time
                player.direction = "inaction"
                food_timer = current_time
                game_state = GameState.WAIT_BEFORE_DISAPPEAR  # Переход к ожиданию перед исчезновением

        elif game_state == GameState.WAIT_BEFORE_DISAPPEAR:
            # Ждем 10-15 секунд перед исчезновением еды и NPC
            if current_time - serving_timer > 10000:  # 10 секунд
                game_state = GameState.FOOD_DISAPPEARING  # Переход к состоянию исчезновения еды

        elif game_state == GameState.FOOD_DISAPPEARING:
            # Проверяем, прошло ли 5 секунд с момента появления еды
            if current_time - food_timer > 5000:
                for food in food_indicators:  # Удаляем всю еду
                    food.kill()
                # Убираем круг над NPC
                if hasattr(current_npc, 'food_indicator'):
                    current_npc.food_indicator.kill()
                    del current_npc.food_indicator

                # Определяем путь ухода в зависимости от пути прихода
                if npc_path_used == npc_paths_cafe[0]:  # Если пришел по пути 0
                    leaving_path = npc_paths_cafe[2]  # Уходит по пути 2
                elif npc_path_used == npc_paths_cafe[1]:  # Если пришел по пути 1
                    leaving_path = npc_paths_cafe[3]  # Уходит по пути 3

                # Обновляем путь NPC
                current_npc.path = leaving_path
                current_npc.current_path_index = 0
                current_npc.path_completed = False

                game_state = GameState.NPC_LEAVING

        elif game_state == GameState.NPC_LEAVING:
            current_npc.update()  # Обновляем NPC для движения по пути
            if current_npc.path_completed:
                current_npc.kill()
                game_state = GameState.WAITING
                show_open_button = True
                current_npc = None

        elif game_state == GameState.SERVING:
            # Процесс обслуживания (2 секунды)
            if current_time - serving_timer > 2000:
                # Завершаем обслуживание
                if hasattr(current_npc, 'food_indicator'):
                    current_npc.food_indicator.kill()
                current_npc.kill()
                game_state = GameState.WAITING
                current_npc = None
                show_open_button = True

        # Обновление объектов
        all_sprites.update()
        npc_group.update()
        food_indicators.update()

        # Постепенное уменьшение затемнения
        if fade_alpha > 0:
            fade_alpha = max(0, fade_alpha - fade_speed)
            fade_surface.set_alpha(fade_alpha)

        # Отрисовка
        cafe_screen.fill(WHITE)
        cafe_tile_group.draw(cafe_screen)
        all_sprites.draw(cafe_screen)
        npc_group.draw(cafe_screen)
        food_indicators.draw(cafe_screen)

        if show_open_button:
            open_button.draw(cafe_screen)
        coin_display.draw(cafe_screen, player_balance)
        day_display.draw(cafe_screen)

        if fade_alpha > 0:
            cafe_screen.blit(fade_surface, (0, 0))

        py.display.flip()
        clock.tick(60)

def Game(player_id, player_email, player_name):
    screen = py.display.set_mode((640, 960))
    py.display.set_caption("Дом")

    global all_sprites, tile_group, food_group
    all_sprites = py.sprite.Group()
    tile_group = py.sprite.Group()
    food_group = py.sprite.Group()

    # Загрузка карты
    game_map = load_pygame("Map/home.tmx")

    # Вытаскивание всех слоёв карты
    for layer in game_map.visible_layers:
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                Tile(pos=pos, surf=surf, groups=tile_group, scale=scale)

    # Монеты и дни
    coin_display = CoinDisplay()
    result = db.execute_query("SELECT `day` FROM `player` WHERE id=%s", (player_id))
    player_day = result[0][0] if result and len(result) > 0 else 0
    day_display = DayDisplay((500, 10), (120, 60), player_day)

    # Кнопка
    buy_button = Button("Купить", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))

    # Игрок
    player = Player((130, 310), scale=4)
    all_sprites.add(player)

    # Переменные для движения и затемнения
    path = [(65, 310), (65, 600), (30, 600), (30, 940), (320, 940), (320, 1070), (250, 1070)]
    current_target = 0
    is_moving = False
    fade_alpha = 0
    fade_surface = py.Surface((640, 960))
    fade_surface.fill(BLACK)
    market_opened = False

    while True:
        player_balance = db.get_player_balance(player_id)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    exit_confirmation_screen()

            if event.type == py.MOUSEBUTTONDOWN:
                if not is_moving and buy_button.is_clicked(event.pos):
                    is_moving = True

        # Логика движения игрока
        if is_moving and not market_opened:
            if current_target < len(path):
                target_x, target_y = path[current_target]

                # Движение по X
                if player.rect.x < target_x:
                    player.move("right")
                elif player.rect.x > target_x:
                    player.move("left")

                # Движение по Y
                if player.rect.y < target_y:
                    player.move("down")
                elif player.rect.y > target_y:
                    player.move("up")

                # Проверка достижения точки
                if (abs(player.rect.x - target_x) < 5 and abs(player.rect.y - target_y) < 5):
                    current_target += 1

                # Постепенное затемнение (начинаем после 3-й точки)
                if current_target >= 3 and fade_alpha < 255:
                    fade_alpha += 3
                    fade_surface.set_alpha(fade_alpha)
            else:
                market_opened = True
                py.display.quit()
                show_market(player_id, player_email, player_balance, player_name)
                # Сброс состояния после закрытия магазина
                is_moving = False
                market_opened = False
                current_target = 0
                fade_alpha = 0
                player.rect.x, player.rect.y = 130, 310
                return

        # Отрисовка
        all_sprites.update()
        screen.fill(WHITE)

        # Отрисовка всех спрайтов
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.topleft)

        # Отрисовка карты
        for tile in tile_group:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y - 0))
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y - 0))

        buy_button.draw(screen)

        # Монеты и дни
        coin_display.update()
        coin_display.draw(screen, player_balance)
        day_display.draw(screen)

        # Затемнение экрана
        if fade_alpha > 0:
            screen.blit(fade_surface, (0, 0))

        py.display.flip()
        clock.tick(60)