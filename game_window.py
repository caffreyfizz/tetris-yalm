import random

import pygame
import time
from image_loading import load_image
from figures import Ishaped, Jshaped, Lshaped, Oshaped, Sshaped, Tshaped, Zshaped
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody


RGB_COLORS = {"blue": (22, 128, 212, 100), "green": (0, 125, 104, 100), "yellow": (253, 187, 3, 100),
              "pink": (198, 23, 88, 100), "purple": (98, 5, 198, 100)}


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class GameWindow:
    def __init__(self, width, height, mode, screen):
        pygame.mouse.set_visible(True)
        self.width, self.height = width, height

        self.figures_types = [Ishaped, Jshaped, Lshaped, Oshaped, Sshaped, Tshaped, Zshaped]

        self.mode = mode

        self.score = 0
        self.rows = 0
        self.start_time = time.time()

        space = world(gravity=(0, -1000))

        self.ground_body = space.CreateStaticBody(position=(0, 0), shapes=polygonShape(box=(75, 1)))
        self.left_body = space.CreateStaticBody(position=(75, 150), shapes=polygonShape(box=(1, 175)))
        self.right_body = space.CreateStaticBody(position=(0, 150), shapes=polygonShape(box=(1, 175)))

        self.fallen_figures = pygame.sprite.Group()

        if mode == 1:
            self.colors = ["blue", "green", "yellow"]
        elif mode == 2:
            self.colors = ["blue", "green", "yellow", "pink"]
        elif mode == 3:
            self.colors = ["blue", "green", "yellow", "pink", "purple"]

        self.figure = random.choice(self.figures_types)(random.choice(self.colors), next=False)
        self.next_figure = random.choice(self.figures_types)(random.choice(self.colors))

        self.speed = 0.5

    def render(self, screen):
        self.fallen_figures.draw(screen)
        screen.fill((0, 0, 0))
        background = load_image("interface.png")
        
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 35)

        text_score = font.render(f"{self.score}", 1, (0, 0, 0))
        screen.blit(text_score, (385, 300))

        text_time = font.render(f"{time.time() - self.start_time:.2f}", 1, (0, 0, 0))
        screen.blit(text_time, (370, 410))

        text_rows = font.render(f"{self.rows}", 1, (0, 0, 0))
        screen.blit(text_rows, (370, 445))

        self.figure.render(screen)
        self.next_figure.render(screen)

        self.figure.move(self.speed, self.left_border, self.right_border)

        """else:
            self.fallen_figures.add(self.figure)

            self.figure.get_rect().y = -100
            self.figure.get_rect().x = 100

            self.figure = self.next_figure
            self.figure.start()
            self.next_figure = random.choice(self.figures_types)(random.choice(self.colors))

            self.speed += 0    # с каждой фигурой скорость увеличивается
"""
    def events_processing(self, event):
        new_window = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:   # вернуться в меню
                new_window = self.open_main()
            if event.key == pygame.K_UP:
                self.figure.rotate()

        return new_window

    def open_main(self):
        return [1, None]

    def set_score(self, new_score):
        self.score = new_score
        self.rows += 1


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, *group):
        super().__init__(*group)
        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)