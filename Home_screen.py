import pygame as py
import sys
import re
from Button import Button
from Sql import Database
from Game import Game
import json


# Подключение к БД
db = Database()
db.connect()

def is_valid_email(email):
    """Проверки почты"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    else:
        return False

def Home_screen():
    """Начальный экран"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    py.init()
    screen = py.display.set_mode((640, 960))
    py.display.set_caption("Hi")

    # Шрифт
    font = py.font.Font("Font/PixelizerBold.ttf", 36)

    # Проверка существования файла с данными игрока
    # try:
    #     with open("player_data.json", "r") as file:
    #         # Проверяем, что файл не пустой
    #         if file.readable():
    #             file.seek(0)  # Возвращаемся в начало файла
    #             player_data = json.load(file)
    #             current_player_id = player_data["id"]
    #             current_player_email = player_data["email"]
    #             current_player_balance = player_data["balance"]
    #             current_player_name = player_data["name"]
    #
    #             # Если игрок существует, показываем приветствие
    #             show_welcome_screen(current_player_name)
    #             return
    #         else:
    #             print("Файл player_data.json пуст.")
    # except FileNotFoundError:
    #     print("Файл player_data.json не найден. Создайте новый аккаунт.")
    # except json.JSONDecodeError:
    #     print("Ошибка чтения файла player_data.json. Проверьте формат файла.")
    #     # Удаляем поврежденный файл, чтобы создать новый
    #     import os
    #     if os.path.exists("player_data.json"):
    #         os.remove("player_data.json")
    #     print("Поврежденный файл удален. Попробуйте снова.")

    # Кнопки
    button_yes = Button("Да", 135, 360, 350, 100, WHITE, (30, 144, 255))
    button_no = Button("Нет", 135, 560, 350, 100, WHITE, (220, 20, 60))

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = py.mouse.get_pos()

                if button_yes.is_clicked(mouse_pos):
                    Yes_button(WHITE, BLACK, font)
                    return

                if button_no.is_clicked(mouse_pos):
                    No_button(WHITE, BLACK, font)
                    return

        screen.fill(WHITE)

        header_surface = font.render("Привет, мы с тобой знакомы?", True, BLACK)
        header_rect = header_surface.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(header_surface, header_rect)

        # Отрисовка кнопок
        button_yes.draw(screen)
        button_no.draw(screen)

        py.display.flip()

def show_welcome_screen(name):
    """Приветствие"""
    py.init()
    screen = py.display.set_mode((640, 960))
    clock = py.time.Clock()
    font = py.font.Font("Font/PixelizerBold.ttf", 48)

    text = f"Привет, {name}!"
    alpha = 0
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(300, 450))

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.KEYDOWN or event.type == py.MOUSEBUTTONDOWN:
                running = False

        # Плавное появление текста
        if alpha < 255:
            alpha += 3
            text_surface.set_alpha(alpha)

        screen.fill((0, 0, 0))
        screen.blit(text_surface, text_rect)
        py.display.flip()
        clock.tick(60)

def No_button(WHITE, BLACK, font):
    """Если выбрано нет"""

    global current_player_id, current_player_email, current_player_balance, current_player_name

    py.init()
    new_screen = py.display.set_mode((640, 960))
    py.display.set_caption("Регистрация")

    # Ввод текста
    input_boxes = [
        py.Rect(75, 300, 450, 70),      # Email
        py.Rect(75, 450, 450, 70),      # Пароль
        py.Rect(75, 600, 450, 70)       # Имя
    ]
    input_texts = ['', '', '']
    active_input = -1
    color_inactive = py.Color('lightskyblue3')
    color_active = py.Color('dodgerblue2')

    # Позиция курсора
    cursor_position = 0
    cursor_visible = True
    cursor_timer = 0

    text_er_surf = None
    text_er_rect = None
    text_er_em_surf = None  # Инициализация переменной
    text_er_em_rect = None

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                db.close()
                py.quit()
                sys.exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    db.close()
                    return Home_screen()

                if active_input != -1:
                    if event.key == py.K_RETURN:
                        if all(input_texts):
                            current_player_name = input_texts[2]
                            current_player_email = input_texts[0]
                            current_player_balance = 100

                            # Проверка на существование email
                            if db.get_player_id(current_player_email) is not None:
                                text_er_surf = font.render("Email уже существует", True, (220, 20, 60))
                                text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))
                            else:
                                try:
                                    db.add_player(current_player_name, current_player_email, input_texts[1], current_player_balance)
                                    # Получаем ID нового игрока
                                    current_player_id = db.get_player_id(current_player_email)

                                    # Сбрасываем поля ввода
                                    input_texts = ['', '', '']
                                    active_input = -1
                                    # Запускаем игру
                                    show_welcome_screen(current_player_name)
                                    Game(current_player_id, current_player_email, current_player_name)

                                except Exception as e:
                                    print(f"Ошибка при регистрации: {e}")
                                    text_er_surf = font.render("Ошибка регистрации", True, (220, 20, 60))
                                    text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))
                        else:
                            text_er_surf = font.render("Все поля должны быть заполнены", True, (220, 20, 60))
                            text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))

                    elif event.key == py.K_BACKSPACE:
                        if cursor_position > 0:
                            input_texts[active_input] = (input_texts[active_input][:cursor_position - 1] + input_texts[active_input][cursor_position:])
                            cursor_position -= 1
                    elif event.key == py.K_DELETE:
                        if cursor_position < len(input_texts[active_input]):
                            input_texts[active_input] = (input_texts[active_input][:cursor_position] + input_texts[active_input][cursor_position + 1:])
                    elif event.key == py.K_LEFT:
                        cursor_position = max(0, cursor_position - 1)
                    elif event.key == py.K_RIGHT:
                        cursor_position = min(len(input_texts[active_input]), cursor_position + 1)
                    else:
                        input_texts[active_input] = (input_texts[active_input][:cursor_position] +
                                                      event.unicode +
                                                      input_texts[active_input][cursor_position:])
                        cursor_position += 1

            # Обработка клика мыши для активации полей ввода
            if event.type == py.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_input = i
                        cursor_position = len(input_texts[i])
                if active_input == -1 and not any(box.collidepoint(event.pos) for box in input_boxes):
                    active_input = -1

        new_screen.fill(WHITE)

        # Отображение текста
        text_surf = font.render("Для начала введи свои данные ;)", True, BLACK)
        text_rect = text_surf.get_rect(center=(new_screen.get_width() // 2, 50))
        new_screen.blit(text_surf, text_rect)

        text_enter_surf = font.render("После заполнения нажмите - Enter", True, BLACK)
        text_enter_rect = text_enter_surf.get_rect(center=(new_screen.get_width() // 2, 100))
        new_screen.blit(text_enter_surf, text_enter_rect)

        # Отрисовка текстовых полей и меток
        labels = ["Email", "Пароль", "Имя"]

        for i, box in enumerate(input_boxes):
            label_surface = font.render(labels[i], True, BLACK)
            label_rect = label_surface.get_rect(center=(box.centerx, box.top - 20))
            new_screen.blit(label_surface, label_rect)

            # Отрисовка текстового поля
            color = color_active if i == active_input else color_inactive
            py.draw.rect(new_screen, color, box, 2)
            text_surface = font.render(input_texts[i], True, BLACK)
            new_screen.blit(text_surface, (box.x + 5, box.y + 5))

            # Отображение курсора
            if i == active_input and cursor_visible:
                cursor_x = box.x + 5 + font.size(input_texts[i][:cursor_position])[0]
                cursor_y = box.y + 5
                py.draw.line(new_screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        # Отрисовка текста ошибки
        if text_er_surf:
            new_screen.blit(text_er_surf, text_er_rect)
        if text_er_em_surf:  # Убедитесь, что эта переменная инициализирована, если вы ее используете
            new_screen.blit(text_er_em_surf, text_er_em_rect)

        # Управление видимостью курсора
        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        py.display.flip()

def Yes_button(WHITE, BLACK, font):
    """Если выбрано да"""

    global current_player_id, current_player_email, current_player_balance, current_player_name

    py.init()
    new_screen = py.display.set_mode((640, 960))
    py.display.set_caption("Вход")

    # Переменные для ввода текста
    input_boxes = [
        py.Rect(75, 300, 450, 70),  # Email
        py.Rect(75, 450, 450, 70),  # Пароль
    ]
    input_texts = ['', '']
    active_input = -1
    color_inactive = py.Color('lightskyblue3')
    color_active = py.Color('dodgerblue2')

    cursor_position = 0
    cursor_visible = True
    cursor_timer = 0

    text_er_surf = None
    text_er_rect = None

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    return Home_screen()

                if active_input != -1:
                    if event.key == py.K_RETURN:
                        if all(input_texts):
                            email = input_texts[0]
                            password = input_texts[1]

                            if db.check_user(email, password):
                                # Получаем все данные игрока
                                query = "SELECT id, name, balance FROM player WHERE email = %s"
                                result = db.execute_query(query, (email,))

                                if result and result[0]:
                                    current_player_id = result[0][0]
                                    current_player_name = result[0][1]
                                    current_player_balance = result[0][2]
                                    current_player_email = email
                                    db.close()

                                    # Запуск игры
                                    Game(current_player_id, current_player_email, current_player_name)
                                else:
                                    text_er_surf = font.render("Ошибка получения данных", True, (220, 20, 60))
                                    text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))
                            else:
                                text_er_surf = font.render("Неверный email или пароль", True, (220, 20, 60))
                                text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))

                    # Обработка других клавиш для ввода текста
                    elif event.key == py.K_BACKSPACE:
                        if cursor_position > 0:
                            input_texts[active_input] = (input_texts[active_input][:cursor_position - 1] +
                                                          input_texts[active_input][cursor_position:])
                            cursor_position -= 1
                    elif event.key == py.K_DELETE:
                        if cursor_position < len(input_texts[active_input]):
                            input_texts[active_input] = (input_texts[active_input][:cursor_position] +
                                                          input_texts[active_input][cursor_position + 1:])
                    elif event.key == py.K_LEFT:
                        cursor_position = max(0, cursor_position - 1)
                    elif event.key == py.K_RIGHT:
                        cursor_position = min(len(input_texts[active_input]), cursor_position + 1)
                    else:
                        input_texts[active_input] = (input_texts[active_input][:cursor_position] +
                                                      event.unicode +
                                                      input_texts[active_input][cursor_position:])
                        cursor_position += 1

            # Обработка клика мыши для активации полей ввода
            if event.type == py.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_input = i
                        cursor_position = len(input_texts[i])
                if active_input == -1 and not any(box.collidepoint(event.pos) for box in input_boxes):
                    active_input = -1

        new_screen.fill(WHITE)

        # Отображение текста
        text_surf = font.render("Для входа введите свои данные ;)", True, BLACK)
        text_rect = text_surf.get_rect(center=(new_screen.get_width() // 2, 50))
        new_screen.blit(text_surf, text_rect)

        text_enter_surf = font.render("После заполнения нажмите - Enter", True, BLACK)
        text_enter_rect = text_enter_surf.get_rect(center=(new_screen.get_width() // 2, 100))
        new_screen.blit(text_enter_surf, text_enter_rect)

        # Отрисовка текстовых полей и меток
        labels = ["Email", "Пароль"]
        for i, box in enumerate(input_boxes):
            label_surface = font.render(labels[i], True, BLACK)
            label_rect = label_surface.get_rect(center=(box.centerx, box.top - 20))
            new_screen.blit(label_surface, label_rect)

            # Отрисовка текстового поля
            if i == active_input:
                color = color_active
            else:
                color = color_inactive
            py.draw.rect(new_screen, color, box, 2)
            text_surface = font.render(input_texts[i], True, BLACK)
            new_screen.blit(text_surface, (box.x + 5, box.y + 5))

            # Отображение курсора
            if i == active_input and cursor_visible:
                cursor_x = box.x + 5 + font.size(input_texts[i][:cursor_position])[0]
                cursor_y = box.y + 5
                py.draw.line(new_screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        # Отрисовка текста ошибки
        if text_er_surf:
            new_screen.blit(text_er_surf, text_er_rect)

        # Управление видимостью курсора
        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        py.display.flip()