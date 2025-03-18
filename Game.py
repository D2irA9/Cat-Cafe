import pygame as py
import sys
from pytmx.util_pygame import load_pygame
from Drawing import Tile
from Player import Player
from Button import Button
from Camera import Camera

def Game(WHITE, BLACK):
    """Запуск игры"""
    py.init()

    screen = py.display.set_mode((640, 960))
    py.display.set_caption("Cat-Cafe")

    # Загруска карты
    map = load_pygame("Map/map.tmx")
    tile_group = py.sprite.Group()
    player_group = py.sprite.Group()

    TILE_SIZE = 16
    scale = 4

    for layer in map.visible_layers:
        if hasattr(layer, 'data'):
            for x, y, surf in layer.tiles():
                pos = (x * TILE_SIZE * scale, y * TILE_SIZE * scale)
                Tile(pos=pos, surf=surf, groups=tile_group, scale=scale)

    camera = Camera(640, 960)
    camera_moving = False
    camera_direction = "down"

    sprite_sheet = py.image.load("Sprite/Player/Player.png").convert_alpha()

    animations = {
        "inaction": [
            py.transform.scale(sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((48, 0, 48, 48)), (48 * scale, 48 * scale))
        ],
        "up": [
            py.transform.scale(sprite_sheet.subsurface((0, 48, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((144, 48, 48, 48)), (48 * scale, 48 * scale))
        ],
        "down": [
            py.transform.scale(sprite_sheet.subsurface((0, 0, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((144, 0, 48, 48)), (48 * scale, 48 * scale))
        ],
        "left": [
            py.transform.scale(sprite_sheet.subsurface((0, 96, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((144, 96, 48, 48)), (48 * scale, 48 * scale))
        ],
        "right": [
            py.transform.scale(sprite_sheet.subsurface((0, 144, 48, 48)), (48 * scale, 48 * scale)),
            py.transform.scale(sprite_sheet.subsurface((144, 144, 48, 48)), (48 * scale, 48 * scale))
        ]
    }

    player = Player(pos=(140, 300), animations=animations, groups=player_group)

    # Анимация, путь
    start = [
        ("left", 75),
        ("down", 300),
        ("left", 50),
        ("down", 340),
        ("right", 310),
        ("down", 110),
        ("left", 100),
    ]

    button_start = Button("Начать рабочий день", 135, 760, 350, 100, (0, 0, 0), (255, 218, 185))
    button_go_store = Button("Идти на рынок", 135, 760, 350, 100, (0, 0, 0), (152, 251, 152))
    button_go_store.visible = False
    button_return = Button("Вернуться", 135, 2680, 350, 100, (0, 0, 0), (255, 218, 185))
    button_open = Button("Открыться", 135, 1720, 350, 100, (0, 0, 0), (244, 164, 96))

    clock = py.time.Clock()

    # Флаги для управления движением игрока
    player_moving = False
    current_path_index = 0
    moved_distance = 0

    while True:
        dt = clock.tick(60) / 1000.0

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.KEYDOWN:
                if event.key == py.K_LALT or event.key == py.K_RALT:
                    py.quit()
                    sys.exit()

            if button_start.is_clicked() and not player_moving:
                camera_moving = True
                camera_direction = "down"
                button_start.visible = False
                player_moving = True

        if camera_moving:
            if camera_direction == "down":
                camera.pos.y += camera.speed
                if camera.pos.y >= 960:
                    camera_moving = False
                    button_go_store.visible = True

        if player_moving and current_path_index < len(start):
            direction, distance = start[current_path_index]
            player.current_animation = direction

            if moved_distance < distance:
                if direction == "right":
                    player.rect.x += player.speed
                elif direction == "down":
                    player.rect.y += player.speed
                elif direction == "left":
                    player.rect.x -= player.speed
                elif direction == "up":
                    player.rect.y -= player.speed

                moved_distance += player.speed
            else:
                moved_distance = 0
                current_path_index += 1

            if current_path_index >= len(start):
                player_moving = False
                player.current_animation = "inaction"

        tile_group.update()
        player.update(dt)

        screen.fill(WHITE)
        for tile in tile_group:
            screen.blit(tile.image, camera.apply(tile))
        screen.blit(player.image, camera.apply(player))

        if button_start.visible:
            button_start.draw(screen)
        if button_go_store.visible:
            button_go_store.draw(screen)
        if button_open.visible:
            button_open.draw(screen)

        py.display.flip()