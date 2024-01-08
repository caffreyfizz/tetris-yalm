import pygame
from image_loading import load_image
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody


class Figure():
    def __init__(self, color, next=True):

        self.space = world(gravity=(0, -1000))
        self.color = color

    def move(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.body.position.x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.body.position.x += 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.body.position.y += 1

    def start(self):
        self.body = self.space.CreateDynamicBody(position=(150, -100))

    def rotate(self):
        self.body.angle += 90
        
    def get_color(self):
        return self.color


class Ishaped(Figure):
    def __init__(self, color, next=True):
        super().__init__(color, next)


class Jshaped(Figure):
    def __init__(self, color, next=True):
        super().__init__(color, next)


class Lshaped(Figure):
     def __init__(self, color, next=True):
        super().__init__(color, next)


class Oshaped(Figure):
     def __init__(self, color, next=True):
        super().__init__(color, next)


class Sshaped(Figure):
     def __init__(self, color, next=True):
        super().__init__(color, next)


class Tshaped(Figure):
     def __init__(self, color, next=True):
        super().__init__(color, next)

class Zshaped(Figure):
     def __init__(self, color, next=True):
        super().__init__(color, next)
