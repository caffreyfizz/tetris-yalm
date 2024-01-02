import random

import pygame
import pymunk.pygame_util
import time
from image_loading import load_image
from figures import Ishaped, Jshaped, Lshaped, Oshaped, Sshaped, Tshaped, Zshaped
from PIL import Image


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

        self.bottom_border = pygame.sprite.Group()
        self.left_border = pygame.sprite.Group()
        self.right_border = pygame.sprite.Group()
        Border(20, self.height - 1, self.width // 2 + 50, self.height, self.bottom_border)
        Border(20, 0, 20, self.height - 1, self.left_border)
        Border(self.width // 2 + 35, 0, self.width // 2 + 35, self.height, self.right_border)

        self.sand = []

        self.draw_options = pymunk.pygame_util.DrawOptions(screen)

        self.pymunk_init()

        if mode == 1:
            self.colors = ["blue", "green", "yellow"]
        elif mode == 2:
            self.colors = ["blue", "green", "yellow", "pink"]
        elif mode == 3:
            self.colors = ["blue", "green", "yellow", "pink", "purple"]

        self.figure = random.choice(self.figures_types)(random.choice(self.colors), next=False)
        self.next_figure = random.choice(self.figures_types)(random.choice(self.colors))

        self.speed = 2

    def pymunk_init(self):
        # настройки Pymunk
        self.space = pymunk.Space()
        self.space.gravity = 0, 1000

        floor = pymunk.Segment(self.space.static_body, (1, self.height + 40),
                               (self.width // 2 + 50, self.height + 40), 40)
        self.space.add(floor)
        floor.elasticity = 0.8
        floor.friction = 1.0

        left_wall = pymunk.Segment(self.space.static_body, (10, 0), (10, self.height), 10)
        self.space.add(left_wall)
        left_wall.elasticity = 0.8
        left_wall.friction = 1.0

        right_wall = pymunk.Segment(self.space.static_body, (self.width // 2 + 45, 1),
                                    (self.width // 2 + 45, self.height), 10)
        self.space.add(right_wall)
        right_wall.elasticity = 0.8
        right_wall.friction = 1.0

    def render(self, screen):
        screen.fill((0, 0, 0))
        background = load_image("interface.png")
        
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 35)
        
        text_score = font.render(f"{self.score}", 1, (0, 0, 0))
        screen.blit(text_score, (385, 300))   # в каких то координатах

        text_time = font.render(f"{time.time() - self.start_time:.2f}", 1, (0, 0, 0))   # время игры
        screen.blit(text_time, (370, 410))

        text_rows = font.render(f"{self.rows}", 1, (0, 0, 0))
        screen.blit(text_rows, (370, 445))

        if not self.figure.check_collide(self.bottom_border):
            self.figure.render(screen)
            self.next_figure.render(screen)

            self.figure.move(self.speed, self.left_border, self.right_border)

        else:
            print()
            new_sand = Sand(self.figure.get_color(), self.figure.get_rect().x, self.figure.get_rect().y, self.space)
            self.sand.append(new_sand)

            self.figure.get_rect().y = -100
            self.figure.get_rect().x = 100

            self.figure = self.next_figure
            self.figure.start()
            self.next_figure = random.choice(self.figures_types)(random.choice(self.colors))

            self.speed += 0.2    # с каждой фигурой скорость увеличивается
            print()

        self.space.step(1 / 60)
        self.space.debug_draw(self.draw_options)

    def events_processing(self, event):
        new_window = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:   # вернуться в меню
                new_window = self.open_main()
            if event.key == pygame.K_UP:
                pass

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


class Sand:
    def __init__(self, color, x, y, space):
        self.color, self.x, self.y, self.space = color, x, y, space

        for step_y in range(0, 60, 15):
            for step_x in range(0, 60, 15):
                self.create_circle((x + step_x, y + step_y))

    def create_circle(self, pos):
        circle_mass = 1
        circle_size = (10, 10)
        circle_moment = pymunk.moment_for_circle(circle_mass, 0, 100, circle_size)
        circle_body = pymunk.Body(circle_mass, circle_moment)
        circle_body.position = pos
        circle_shape = pymunk.Circle(circle_body, 8, circle_size)
        circle_shape.elasticity = 0.1
        circle_shape.friction = 1
        circle_shape.color = RGB_COLORS[self.color]
        self.space.add(circle_body, circle_shape)
