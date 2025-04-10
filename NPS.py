import pygame as py

class NPC(py.sprite.Sprite):
    def __init__(self, pos, scale, sprite_sheet_path, path=None):
        super().__init__()
        self.scale = scale
        self.sprite_sheet = py.image.load(sprite_sheet_path).convert_alpha()
        self.animations = {
            "inaction": [
                py.transform.scale(self.sprite_sheet.subsurface((24, 0, 24, 24)), (24 * scale, 24 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((24, 0, 24, 24)), (24 * scale, 24 * scale))
            ],
            "up": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 72, 24, 24)), (24 * scale, 24 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((72, 72, 24, 24)), (24 * scale, 24 * scale))
            ],
            "down": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 0, 24, 24)), (24 * scale, 24 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((72, 0, 24, 24)), (24 * scale, 24 * scale))
            ],
            "left": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 24, 24, 24)), (24 * scale, 24 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((72, 24, 24, 24)), (24 * scale, 24 * scale))
            ],
            "right": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 48, 24, 24)), (24 * scale, 24 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((72, 48, 24, 24)), (24 * scale, 24 * scale))
                ]
        }
        self.direction = "inaction"
        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.frame_index = 0
        self.animation_speed = 0.1 # 0.28
        self.last_update = py.time.get_ticks()
        # Маршрут NPC
        self.path = path
        self.current_path_index = 0
        self.path_completed = False

    def update(self):
        """Обновление анимации и движения NPC"""
        now = py.time.get_ticks()
        if now - self.last_update > 100:
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
                self.current_path_index += 1
                if self.current_path_index >= len(self.path):
                    self.direction = "inaction"
                    self.path_completed = True