import pygame
from image_loading import load_image
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody

from math import pi


PPI = 10


def to_radians(angle):
    return angle * pi / 180


class Figure(pygame.sprite.Sprite):
    def __init__(self, color, space, img_name, group, is_next=True):
        super().__init__(*group)

        self.image = load_image(img_name)

        self.rect = self.image.get_rect()
        self.is_next = is_next

        self.space = space

        if is_next:
            self.rect.x = 470
            self.rect.y = 30
        else:
            self.rect.x = (335 - self.image.get_rect().width) // 2
            self.rect.y = -100
            self.box2d_init()

        self.color = color

    def box2d_init(self):
        x, y = (self.rect.x + 40) // PPI, (600 - self.rect.y - 40) // PPI
        self.body = self.space.CreateDynamicBody(position=(x, y), angle=0)
        self.box = self.body.CreatePolygonFixture(box=(4, 4), density=1, friction=1)

    def update(self):
        print("update")
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.body.position.x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.body.position.x += 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.body.position.y += 1

        self.set_coords()

    def set_coords(self):
        self.rect.x, self.rect.y = self.body.position.x * PPI - 40, self.body.position.y * PPI + 40

    def rotate(self):
        self.body.angle += to_radians(90)
        self.image = pygame.transform.rotate(self.image, 90)
        
    def get_color(self):
        return self.color

    def start(self):
        self.is_next = False
        self.rect.x = (335 - self.image.get_rect().width) // 2
        self.rect.y = -100
        self.box2d_init()


class Ishaped(Figure):
    def __init__(self, color, space, group, next=True):
        super().__init__(color, space, f"I_shape/I_{color}.png", group, next)


class Jshaped(Figure):
    def __init__(self, color, space, group, next=True):
        super().__init__(color, space, f"J_shape/J_{color}.png", group, next)


class Lshaped(Figure):
    def __init__(self, color, space, group, next=True):
        super().__init__(color, space, f"L_shape/L_{color}.png", group, next)


class Oshaped(Figure):
    def __init__(self, color, space, group, next=True):
        super().__init__(color, space, f"O_shape/O_{color}.png", group, next)


class Sshaped(Figure):
    def __init__(self, color, space, group, next=True):
        super().__init__(color, space, f"S_shape/S_{color}.png", group, next)


class Tshaped(Figure):
    def __init__(self, color, space, group, next=True):
        super().__init__(color, space, f"T_shape/T_{color}.png", group, next)


class Zshaped(Figure):
    def __init__(self, color, space, group, next=True):
        super().__init__(color, space, f"Z_shape/Z_{color}.png", group, next)