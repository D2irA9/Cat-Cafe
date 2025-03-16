import pygame as py

class Camera:
    def __init__(self, width, height):
        self.camera = py.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.speed = 5

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target_y):
        # Двигаем камеру вниз
        if self.camera.y < target_y:
            self.camera.y += self.speed
            if self.camera.y > target_y:  # Не превышаем target_y
                self.camera.y = target_y
        elif self.camera.y > target_y:
            self.camera.y -= self.speed
            if self.camera.y < target_y:  # Не опускаемся ниже target_y
                self.camera.y = target_y

        # Ограничиваем камеру, чтобы она не выходила за пределы карты
        if self.camera.y < 0:
            self.camera.y = 0
        if self.camera.y > self.height - self.camera.height:
            self.camera.y = self.height - self.camera.height