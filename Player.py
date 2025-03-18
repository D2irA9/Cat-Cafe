import pygame as py

class Player(py.sprite.Sprite):

    def __init__(self, pos, animations, groups):
        super().__init__(groups)
        self.animations = animations
        self.current_animation = "inaction"
        self.current_image = 0
        self.image = self.animations[self.current_animation][self.current_image]
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 5
        self.animation_speed = 0.2
        self.animation_timer = 0

    def update(self, dt):
        """Обновление анимации"""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_image]
            self.animation_timer = 0