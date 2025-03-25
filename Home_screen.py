import pygame as py
import sys
from Button import Button
from Sql import Database
from Game import Game

def Home_screen():
    """Начальный экран"""
    db = Database()
    db.connect()
    db.creating_tables()
    db.close()
    py.init()
    screen = py.display.set_mode((600, 900))
    py.display.set_caption("Hi")

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Шрифт
    font = py.font.Font("Font/PixelizerBold.ttf", 36)

    # Создание кнопок
    button_yes = Button("Да", 135, 360, 350, 100, WHITE, (30, 144, 255))
    button_no = Button("Нет", 135, 560, 350, 100, WHITE, (220, 20, 60))

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

        # Проверка нажатия левой кнопки мыши
        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:  # 1 - это ЛКМ
            mouse_pos = py.mouse.get_pos()  # Получаем позицию курсора

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

def No_button(WHITE, BLACK, font):
    """Если выброно нет"""
    py.init()
    new_screen = py.display.set_mode((600, 900))
    py.display.set_caption("Регистрация")

    # Ввод текста
    input_boxes = [
        py.Rect(75, 300, 450, 70), # Email
        py.Rect(75, 450, 450, 70), # Пароль
        py.Rect(75, 600, 450, 70)  # Имя
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

    # Подключение к БД
    db = Database()
    db.connect()

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
                            db.add_player(input_texts[2], input_texts[0], input_texts[1])
                            db.close()
                            input_texts = ['', '', '']
                            active_input = -1
                            cursor_position = 0
                            text_er_surf = None
                            # Если все хорошо, то игра запускается
                            Game()
                        else:
                            text_er_surf = font.render("Все поля должны быть заполнены", True, (220, 20, 60))
                            text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))

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
                        cursor_position = len(input_texts[i])  # Устанавливаем курсор в конец текста
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
        if cursor_timer >= 30:  # Каждые 30 кадров переключаем видимость курсора
            cursor_visible = not cursor_visible
            cursor_timer = 0

        py.display.flip()

def Yes_button(WHITE, BLACK, font):
    """Если выбрано да"""
    py.init()
    new_screen = py.display.set_mode((600, 900))
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

    # Позиция курсора
    cursor_position = 0
    cursor_visible = True
    cursor_timer = 0

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

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    return Home_screen()

                if active_input != -1:
                    if event.key == py.K_RETURN:
                        if all(input_texts):
                            email = input_texts[0]
                            password = input_texts[1]
                            if db.check_user(email, password):
                                db.close()
                                print("Успешный вход в аккаунт!")
                                input_texts = ['', '']
                                active_input = -1
                                cursor_position = 0
                                text_er_surf = None
                                # Если все хорошо, то игра запускается
                                Game()
                            else:
                                text_er_surf = font.render("Неверный email или пароль.", True, (220, 20, 60))
                                text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))

                        else:
                            text_er_surf = font.render("Все поля должны быть заполнены", True, (220, 20, 60))
                            text_er_rect = text_er_surf.get_rect(center=(new_screen.get_width() // 2, 750))

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
                        cursor_position = len(input_texts[i])  # Устанавливаем курсор в конец текста
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
        if cursor_timer >= 30:  # Каждые 30 кадров переключаем видимость курсора
            cursor_visible = not cursor_visible
            cursor_timer = 0

        py.display.flip()



