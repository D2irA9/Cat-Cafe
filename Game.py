import pygame as py
from pygame.examples.go_over_there import screen

from Button import Button
def Game():
    """Игра"""
    py.init()
    screen = py.display.set_mode((600, 900))
    py.display.set_caption("Cat-Cafe")
    # color
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

