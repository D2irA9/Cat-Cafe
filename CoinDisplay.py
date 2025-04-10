import pygame as py

class CoinDisplay:
    def __init__(self):
        self.sprite_sheet = py.image.load("Sprite/coins/coins.png").convert_alpha()
        self.frame_size = 16
        self.total_frames = 13
        self.display_size = 48
        self.frames = []
        for i in range(self.total_frames):
            frame = py.Surface((self.frame_size, self.frame_size), py.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * self.frame_size, 0, self.frame_size, self.frame_size))
            self.frames.append(py.transform.scale(frame, (self.display_size, self.display_size)))

        # Настройки анимации
        self.animation_sequence = list(range(13))
        self.current_frame_index = 0
        self.animation_speed = 15
        self.animation_timer = 0
        self.cooldown_timer = 0
        self.cooldown_duration = 300
        self.is_animating = False

        # Параметры отображения
        self.bg_color = (242, 231, 116)
        self.border_color = (200, 180, 60)
        self.text_color = (0, 0, 0)
        self.position = (10, 10)
        self.size = (250, 60)
        self.normal_color = (0, 0, 0)
        self.positive_color = (0, 200, 0)
        self.negative_color = (200, 0, 0)
        self.color_change_timer = 0
        self.current_text_color = self.normal_color

    def update(self):
        """Обновление состояния анимации"""
        self.cooldown_timer += 1

        if self.color_change_timer > 0:
            self.color_change_timer -= 1
            if self.color_change_timer == 0:
                self.current_text_color = self.normal_color

        if not self.is_animating and self.cooldown_timer >= self.cooldown_duration:
            self.is_animating = True
            self.current_frame_index = 0
            self.cooldown_timer = 0

        if self.is_animating:
            self.animation_timer += 1
            if self.animation_timer >= 60 / self.animation_speed:
                self.current_frame_index += 1
                self.animation_timer = 0

                if self.current_frame_index >= len(self.animation_sequence):
                    self.current_frame_index = 0
                    self.is_animating = False

    def update_balance(self, new_balance, change):
        """Запускает анимацию при изменении баланса"""
        self.is_animating = True
        self.current_frame_index = 0
        self.animation_timer = 0
        self.cooldown_timer = 0

        if change < 0:
            self.current_text_color = self.negative_color
            self.color_change_timer = 30
        elif change > 0:
            self.current_text_color = self.positive_color
            self.color_change_timer = 30

    def update_text_color(self, color):
        """Изменяет цвет текста"""
        self.current_text_color = color
        self.color_change_timer = 30

    def draw(self, screen, balance):
        """Отрисовка элемента с балансом"""
        rect = py.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

        # Фон и рамка
        py.draw.rect(screen, self.bg_color, rect)
        py.draw.rect(screen, self.border_color, rect, 2)

        # Получаем текущий кадр
        frame_num = self.animation_sequence[self.current_frame_index] if self.is_animating else 0
        current_frame = self.frames[frame_num]

        # Позиционирование увеличенной монетки
        coin_x = self.position[0] + 5
        coin_y = self.position[1] + (self.size[1] - self.display_size) // 2

        # Отрисовка увеличенной монеты
        screen.blit(current_frame, (coin_x, coin_y))

        # Текст баланса
        font = py.font.Font("Font/PixelizerBold.ttf", 32)
        balance_text = font.render(f"{balance}", True, self.current_text_color)
        text_x = coin_x + self.display_size + 10
        text_y = coin_y + (self.display_size - balance_text.get_height()) // 2
        screen.blit(balance_text, (text_x, text_y))

    def get_coin_sprite(self):
        """Возвращает спрайт монеты для отображения"""
        return self.image