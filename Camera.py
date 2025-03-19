import pygame as py

class Camera:
    def __init__(self, width, height):
        self.pos = py.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.speed = 5

    def apply(self, entity):
        """Применяет смещение камеры к объекту."""
        return entity.rect.move(-self.pos.x, -self.pos.y)

    def update(self, target_y):
        """Обновляет позицию камеры, двигая её к целевой позиции."""
        if self.pos.y < target_y:
            self.pos.y += self.speed
            if self.pos.y > target_y:
                self.pos.y = target_y
        elif self.pos.y > target_y:
            self.pos.y -= self.speed
            if self.pos.y < target_y:
                self.pos.y = target_y

        # Ограничиваем движение камеры
        self.pos.y = max(0, min(self.pos.y, self.height - self.pos.height))