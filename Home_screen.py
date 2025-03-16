import pygame as py
import sys
import re
from Button import Button
from Sql import Database
from Game import Game

def is_valid_email(email):
    """Проверки почты"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    else:
        return False


def Home_screen(WHITE, BLACK):
    """Начальный экран"""
    py.init()
    screen = py.display.set_mode((600, 900))
    py.display.set_caption("Hi")

    # Шрифт
    font = py.font.Font("Font/PixelizerBold.ttf", 36)
    Greeting = "Привет, мы с тобой знакомы?"

    # Создание кнопок с новыми цветами
    button_yes = Button("Да", 135, 360, 350, 100, WHITE,(30, 144, 255))
    button_no = Button("Нет", 135, 560, 350, 100,  WHITE,(220, 20, 60))

    # Основной игровой цикл
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

        if button_yes.is_clicked():
            Yes_button()
            return

        if button_no.is_clicked():
            No_button()
            return

            # Отрисовка
        screen.fill(WHITE)

        # Отображение заголовка по центру
        header_surface = font.render(Greeting, True, BLACK)
        header_rect = header_surface.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(header_surface, header_rect)

        # Отрисовка кнопок
        button_yes.draw(screen)
        button_no.draw(screen)

        py.display.flip()

def No_button():
    """Если выброно нет"""
    py.init()
    new_screen = py.display.set_mode((600, 900))
    py.display.set_caption("Регистрация")

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Переменные для ввода текста
    input_boxes = [
        py.Rect(75, 300, 450, 70),
        py.Rect(75, 450, 450, 70),
        py.Rect(75, 600, 450, 70)
    ]
    # Список для хранения введенного текста
    input_texts = ['', '', '']
    active_input = -1
    color_inactive = py.Color('lightskyblue3')
    color_active = py.Color('dodgerblue2')
    text = "Для начала введи свои данные ;)"
    text_enter = "После заполнения нажмите - Enter"
    text_er = "Все поля должны заполнены"
    text_er_em = "Некорректная почта"

    # Шрифт
    font = py.font.Font("Font/PixelizerBold.ttf", 36)

    # Инициализация переменной для текста ошибки
    text_er_surf = None
    text_er_rect = None
    text_er_em_surf = None
    text_er_em_rect = None

    # Подключение к БД
    db = Database()
    db.connect()

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            # Обработка нажатий клавиш
            if event.type == py.KEYDOWN:
                if active_input != -1:
                    if event.key == py.K_RETURN:
                        if all(input_texts):
                            if is_valid_email(input_texts[0]):
                                # print("Email:", input_texts[0])
                                # print("Пароль:", input_texts[1])
                                # print("Имя:", input_texts[2])
                                db.add_player(input_texts[2], input_texts[0], input_texts[1])
                                db.close()
                                input_texts = ['', '', '']
                                active_input = -1
                                text_er_surf = None
                                text_er_em_surf = None
                                # Запуск game
                                Game(WHITE, BLACK)
                            else:
                                text_er_em_surf = font. render(text_er_em, True, (220, 20, 60))
                                text_er_em_rect = text_er_em_surf.get_rect(center=(new_screen.get_width() // 2, 850))
                        else:
                            text_er_surf = font.render(text_er, True, (220, 20, 60))
                            text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))

                    elif event.key == py.K_BACKSPACE:
                        input_texts[active_input] = input_texts[active_input][:-1]
                    else:
                        input_texts[active_input] += event.unicode

            # Обработка клика мыши для активации полей ввода
            if event.type == py.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_input = i
                if active_input == -1 and not any(box.collidepoint(event.pos) for box in input_boxes):
                    active_input = -1

        new_screen.fill(WHITE)

        # Отображение текста
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=(new_screen.get_width() // 2, 50))
        new_screen.blit(text_surf, text_rect)

        text_enter_surf = font.render(text_enter, True, BLACK)
        text_enter_rect = text_enter_surf.get_rect(center=(new_screen.get_width()//2, 100))
        new_screen.blit(text_enter_surf, text_enter_rect)

        # Отрисовка текстовых полей и меток
        labels = ["Email", "Пароль", "Имя"]

        for i, box in enumerate(input_boxes):
            # Отрисовка метки
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

        # Отрисовка текста ошибки, если он существует
        if text_er_surf:
            new_screen.blit(text_er_surf, text_er_rect)
        if text_er_em_surf:
            new_screen.blit(text_er_em_surf, text_er_em_rect)

        py.display.flip()


def Yes_button():
    """Если выброно да"""
    py.init()
    new_screen = py.display.set_mode((600, 900))
    py.display.set_caption("Вход")

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Переменные для ввода текста
    input_boxes = [
        py.Rect(75, 300, 450, 70),  # Email
        py.Rect(75, 450, 450, 70),  # Пароль
    ]

    # Список для хранения введенного текста
    input_texts = ['', '']
    active_input = -1
    color_inactive = py.Color('lightskyblue3')
    color_active = py.Color('dodgerblue2')
    text = "Для входа введите свои данные ;)"
    text_enter = "После заполнения нажмите - Enter"
    text_er = "Все поля должны быть заполнены"

    # Шрифт
    font = py.font.Font("Font/PixelizerBold.ttf", 36)

    # Инициализация переменной для текста ошибки
    text_er_surf = None
    text_er_rect = None

    # Подключение к БД
    db = Database()
    db.connect()

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            # Обработка нажатий клавиш
            if event.type == py.KEYDOWN:
                if active_input != -1:
                    if event.key == py.K_RETURN:
                        if all(input_texts):
                            email = input_texts[0]
                            password = input_texts[1]

                            # Проверка пользователя
                            if db.check_user(email, password):
                                print("Успешный вход в аккаунт!")
                                # Здесь можно добавить логику для перехода на следующий экран
                                input_texts = ['', '']
                                active_input = -1
                                text_er_surf = None
                                # Запуск game
                                Game(WHITE, BLACK)
                            else:
                                text_er_surf = font.render("Неверный email или пароль.", True, (220, 20, 60))
                                text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))

                        else:
                            text_er_surf = font.render(text_er, True, (220, 20, 60))
                            text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))

                    elif event.key == py.K_BACKSPACE:
                        input_texts[active_input] = input_texts[active_input][:-1]
                    else:
                        input_texts[active_input] += event.unicode

            # Обработка клика мыши для активации полей ввода
            if event.type == py.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        active_input = i
                if active_input == -1 and not any(box.collidepoint(event.pos) for box in input_boxes):
                    active_input = -1

        new_screen.fill(WHITE)

        # Отображение текста
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=(new_screen.get_width() // 2, 50))
        new_screen.blit(text_surf, text_rect)

        text_enter_surf = font.render(text_enter, True, BLACK)
        text_enter_rect = text_enter_surf.get_rect(center=(new_screen.get_width() // 2, 100))
        new_screen.blit(text_enter_surf, text_enter_rect)

        # Отрисовка текстовых полей и меток
        labels = ["Email", "Пароль"]
        for i, box in enumerate(input_boxes):
            # Отрисовка метки
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

        # Отрисовка текста ошибки, если он существует
        if text_er_surf:
            new_screen.blit(text_er_surf, text_er_rect)

        py.display.flip()

    db.close()


if __name__ == "__Home_screen__":
    Home_screen()