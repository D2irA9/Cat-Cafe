import pygame as py

class NPC(py.sprite.Sprite):
    def __init__(self, pos, scale, sprite_sheet_path, path=None):
        super().__init__()
        self.scale = scale
        self.sprite_sheet = py.image.load(sprite_sheet_path).convert_alpha()
        self.animations = {
            "inaction": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((48, 0, 48, 48)), (48 * scale, 48 * scale))
            ],
            "up": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 48, 48, 48)), (48 * scale, 48 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((48, 48, 48, 48)), (48 * scale, 48 * scale))
            ],
            "down": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),  # Первый спрайт
                py.transform.scale(self.sprite_sheet.subsurface((48, 0, 48, 48)), (48 * scale, 48 * scale))   # Второй спрайт
            ],
            "left": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 48, 48, 48)), (48 * scale, 48 * scale)),  # Первый спрайт
                py.transform.scale(self.sprite_sheet.subsurface((48, 48, 48, 48)), (48 * scale, 48 * scale))   # Второй спрайт
            ],
            "right": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),  # Первый спрайт
                py.transform.scale(self.sprite_sheet.subsurface((48, 0, 48, 48)), (48 * scale, 48 * scale))   # Второй спрайт
            ]
        }
        self.direction = "inaction"
        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.frame_index = 0
        self.animation_speed = 0.1
        self.last_update = py.time.get_ticks()
        self.path = path  # Маршрут NPC
        self.current_path_index = 0  # Текущая точка маршрута

    def update(self):
        """Обновление анимации и движения NPC"""
        now = py.time.get_ticks()
        if now - self.last_update > 100:  # Задержка между кадрами анимации
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.frame_index]
            self.last_update = now

        # Логика движения по маршруту
        if self.path and self.current_path_index < len(self.path):
            target_x, target_y = self.path[self.current_path_index]
            if self.rect.x < target_x:
                self.rect.x += 1
                self.direction = "right"
            elif self.rect.x > target_x:
                self.rect.x -= 1
                self.direction = "left"
            elif self.rect.y < target_y:
                self.rect.y += 1
                self.direction = "down"
            elif self.rect.y > target_y:
                self.rect.y -= 1
                self.direction = "up"
            else:
                self.current_path_index += 1  # Переход к следующей точке маршрута
                if self.current_path_index >= len(self.path):
                    self.direction = "inaction"  # Остановка после завершения маршрута