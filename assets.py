import os
import sys

import pygame


FPS = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
RGB_COLORS = {"blue": (22, 128, 212, 100), "green": (0, 125, 104, 100), "yellow": (253, 187, 3, 100),
              "pink": (198, 23, 88, 100), "purple": (98, 5, 198, 100)}
PPM = 10
TIME_STEP = 1.0 / FPS


def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image