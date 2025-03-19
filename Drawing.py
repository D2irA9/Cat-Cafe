import pygame as py

class Tile(py.sprite.Sprite):
    """Для прорисовки карты"""
    def __init__(self, pos, surf, groups, scale):
        super().__init__(groups)
        if surf is not None:
            self.image = py.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
            self.rect = self.image.get_rect(topleft=pos)
        else:
            self.image = py.Surface((int(16 * scale), int(16 * scale)))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface):
        surface.blit(self.image, self.rect)