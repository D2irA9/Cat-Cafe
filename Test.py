# import pygame as py
# import sys
# from pytmx.util_pygame import load_pygame
#
# class Tile(py.sprite.Sprite):
#     def __init__(self, pos, surf, groups, scale):
#         super().__init__(groups)
#         if surf is not None:
#             # Проверяем, что surf не None
#             self.image = py.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
#             self.rect = self.image.get_rect(topleft=pos)
#         else:
#             # Создаем пустую поверхность, если surf None
#             self.image = py.Surface((int(16 * scale), int(16 * scale)))
#             self.image.fill((255, 0, 0))
#             self.rect = self.image.get_rect(topleft=pos)
#
#     def draw(self, surface):
#         surface.blit(self.image, self.rect)
#
# # Инициализация Pygame
# py.init()
#
# # Размер плитки
# TILE_SIZE = 16
# # Коэффициент масштабирования
# scale = 4
#
# # Установка размера окна
# window_width = 10 * TILE_SIZE * scale
# window_height = 15 * TILE_SIZE * scale
# screen = py.display.set_mode((window_width, window_height))
# py.display.set_caption("Карта в Pygame")
#
# map = load_pygame("Map/map.tmx")
# sprite_group = py.sprite.Group()
#
# for layer in map.visible_layers:
#     if hasattr(layer, 'data'):
#         for x, y, surf in layer.tiles():
#             pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
#             Tile(pos=pos, surf=surf, groups=sprite_group, scale=scale)
#
# # Цвета
# WHITE = (255, 255, 255)
#
#
# while True:
#     for event in py.event.get():
#         if event.type == py.QUIT:
#             py.quit()
#             sys.exit()
#
#     screen.fill(WHITE)
#
#     # Рисуем все плитки
#     for tile in sprite_group:
#         tile.draw(screen)
#
#     py.display.flip()