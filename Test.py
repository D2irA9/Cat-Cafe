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


def open_cafe_win(player_id, player_email, player_balance, player_name):
    """Функция для открытия кафе с эффектом плавного появления"""
    cafe_screen = py.display.set_mode((640, 960))
    py.display.set_caption("Cat Cafe")

    # Настройки эффекта плавного появления
    fade_surface = py.Surface((640, 960))
    fade_surface.fill(BLACK)
    fade_alpha = 255  # Начинаем с полностью черного экрана
    fade_speed = 3  # Скорость появления

    # Инициализация групп спрайтов
    all_sprites = py.sprite.Group()
    cafe_tile_group = py.sprite.Group()

    # Загрузка карты кафе
    cafe_map = load_pygame("Map/cat-cafe.tmx")

    # Загрузка тайлов
    for layer in cafe_map.visible_layers:
        if hasattr(layer, "data"):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                Tile(pos=pos, surf=surf, groups=cafe_tile_group, scale=scale)

    # Игрок (изменил координаты на (320, 480) - центр экрана)
    player = Player((320, 480), scale=4)
    all_sprites.add(player)

    # Интерфейс
    coin_display = CoinDisplay()
    result = db.execute_query("SELECT `day` FROM `player` WHERE id=%s", (player_id))
    player_day = result[0][0] if result and len(result) > 0 else 0
    day_display = DayDisplay((500, 10), (120, 60), player_day)
    open_button = Button("Начать рабочий день", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185))

    # Основной цикл
    while True:
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

        # Обновление
        all_sprites.update()

        # Постепенное уменьшение затемнения
        if fade_alpha > 0:
            fade_alpha = max(0, fade_alpha - fade_speed)
            fade_surface.set_alpha(fade_alpha)

        # Отрисовка
        cafe_screen.fill(WHITE)

        # Отрисовка карты
        cafe_tile_group.draw(cafe_screen)

        # Отрисовка игрока и других спрайтов
        all_sprites.draw(cafe_screen)

        # Отрисовка интерфейса
        open_button.draw(cafe_screen)
        coin_display.draw(cafe_screen, player_balance)
        day_display.draw(cafe_screen)

        # Наложение эффекта затемнения
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