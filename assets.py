import os
import random
import sys
import time

import pygame


FPS = 60
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
RGB_COLORS = {"blue": (22, 128, 212, 100), "green": (0, 125, 104, 100), "yellow": (253, 187, 3, 100),
              "pink": (198, 23, 88, 100), "purple": (98, 5, 198, 100)}
PPM = 10
TIME_STEP = 1.0 / FPS
COUNT_OF_LEVELS = 3


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, draw_range):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0

        self.draw_range = draw_range
        self.image = self.frames[self.cur_frame]
        self.rect.x, self.rect.y = (random.randint(self.draw_range[0], self.draw_range[2]),
                                    random.randint(self.draw_range[1], self.draw_range[3]))
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self)

        self.start = time.time()
        self.timer = random.random()
        self.show = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        if not self.show and time.time() - self.start >= self.timer:
            self.show = True

        if self.show:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.cur_frame == len(self.frames) - 1:
                self.rect.x, self.rect.y = (random.randint(self.draw_range[0], self.draw_range[2]),
                                            random.randint(self.draw_range[1], self.draw_range[3]))
                self.start = time.time()
                self.timer = random.random()
                self.show = False
            self.image = self.frames[self.cur_frame]

    def render(self, screen):
        if self.show:
            self.sprites.draw(screen)
