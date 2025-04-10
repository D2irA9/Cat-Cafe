import pygame as py

class Player(py.sprite.Sprite):
    def __init__(self, pos, scale):
        super().__init__()
        self.scale = scale
        self.sprite_sheet = py.image.load("Sprite/player/Player.png").convert_alpha()
        self.animations = {
            "inaction": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((48, 0, 48, 48)), (48 * scale, 48 * scale))
            ],
            "up": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 48, 48, 48)), (48 * scale, 48 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((144, 48, 48, 48)), (48 * scale, 48 * scale))
            ],
            "down": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((144, 0, 48, 48)), (48 * scale, 48 * scale))
            ],
            "left": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 96, 48, 48)), (48 * scale, 48 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((144, 96, 48, 48)), (48 * scale, 48 * scale))
            ],
            "right": [
                py.transform.scale(self.sprite_sheet.subsurface((0, 144, 48, 48)), (48 * scale, 48 * scale)),
                py.transform.scale(self.sprite_sheet.subsurface((144, 144, 48, 48)), (48 * scale, 48 * scale))
            ]
        }

        self.direction = "inaction"
        self.image = self.animations[self.direction][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.frame_index = 0
        self.animation_speed = 0.1 # 0.5
        self.last_update = py.time.get_ticks()

    def update(self):
        """Обновление анимации"""
        now = py.time.get_ticks()
        if now - self.last_update > 100:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.frame_index]
            self.last_update = now

    def move(self, direction):
        """Движение игрока и изменение анимации"""
        if direction == "up":
            self.rect.y -= 5
            self.direction = "up"
        elif direction == "down":
            self.rect.y += 5
            self.direction = "down"
        elif direction == "left":
            self.rect.x -= 5
            self.direction = "left"
        elif direction == "right":
            self.rect.x += 5
            self.direction = "right"

    def move_to(self, x, y):
        """Перемещает игрока в заданную позицию"""
        self.rect.centerx = x
        self.rect.centery = y