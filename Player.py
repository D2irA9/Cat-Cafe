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
        self.animation_speed = 0.1
        self.animation_timer = 0

    def update(self, dt):
        """Обновление анимации"""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_image]
            self.animation_timer = 0

    def start_day(self, screen, tile_group, player):
        """Функция для движения игрока по заданному пути"""

        # Анимация, путь
        path = [
            ("left", 75),
            ("down", 300),
            ("left", 50),
            ("down", 300),

        ]
        clock = py.time.Clock()
        for direction, distance in path:
            moved_distance = 0
            player.current_animation = direction

            while moved_distance < distance:
                dt = clock.tick(60) / 1000.0

                if direction == "right":
                    player.rect.x += player.speed
                elif direction == "down":
                    player.rect.y += player.speed
                elif direction == "left":
                    player.rect.x -= player.speed
                elif direction == "up":
                    player.rect.y -= player.speed

                moved_distance += player.speed


                player.update(dt)

                # Рисуем все плитки
                screen.fill((255, 255, 255))
                for tile in tile_group:
                    tile.draw(screen)

                # Рисуем игрока
                screen.blit(player.image, player.rect)
                py.display.flip()

        player.current_animation = "inaction"