import pygame as py

class Camera:
    def __init__(self, width, height):
        self.pos = py.Rect(0, 0, width, height)  # Позиция и размер камеры
        self.width = width  # Ширина экрана
        self.height = height  # Высота экрана
        self.speed = 5  # Скорость движения камеры

    def apply(self, entity):
        """Применяет смещение камеры к объекту."""
        return entity.rect.move(-self.pos.x, -self.pos.y)

    def update(self, target_y):
        """Обновляет позицию камеры, двигая её к целевой позиции."""
        # Двигаем камеру вниз
        if self.pos.y < target_y:
            self.pos.y += self.speed
        #     if self.pos.y > target_y:  # Не превышаем target_y
        #         self.pos.y = target_y
        # elif self.pos.y > target_y:
        #     self.pos.y -= self.speed
        #     if self.pos.y < target_y:  # Не опускаемся ниже target_y
        #         self.pos.y = target_y
        #
        # # Ограничиваем движение камеры
        # if self.pos.y < 0:
        #     self.pos.y = 0
        # if self.pos.y > self.height - self.pos.height:
        #     self.pos.y = self.height - self.pos.height