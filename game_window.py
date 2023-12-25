import random

import pygame
import pymunk.pygame_util
import time
from image_loading import load_image
from figures import Cube


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class GameWindow:
    def __init__(self, width, height, mode, screen):
        self.background_color = (0, 0, 0)
        self.width, self.height = width, height

        self.mode = mode
        
        self.x_figure, self.y_figure = 100, -100   # будет спавнится в рандомных координатах

        self.score = 0
        self.rows = 0
        self.start_time = time.time()

        self.horizontal_borders = pygame.sprite.Group()
        self.vertical_borders = pygame.sprite.Group()
        Border(20, self.height - 1, self.width // 2 - 20, self.height - 1, self.horizontal_borders)
        Border(20, 2, 20, self.height - 1, self.vertical_borders)
        Border(self.width // 2 + 30, 2, self.width // 2 + 30, self.height - 1, self.vertical_borders)

        self.sand = []

        self.draw_options = pymunk.pygame_util.DrawOptions(screen)

        # настройки Pymunk
        self.space = pymunk.Space()
        self.space.gravity = 0, 1000

        # платформа
        segment_shape = pymunk.Segment(self.space.static_body, (1, self.height),
                                       (self.width // 2 + 50, self.height), 40)
        self.space.add(segment_shape)
        segment_shape.elasticity = 0.8
        segment_shape.friction = 1.0

        segment_shape1 = pymunk.Segment(self.space.static_body, (1, 1), (1, self.height), 10)
        self.space.add(segment_shape1)
        segment_shape1.elasticity = 0.8
        segment_shape1.friction = 1.0

        segment_shape2 = pymunk.Segment(self.space.static_body, (self.width // 2 + 50, 1),
                                        (self.width // 2 + 50, self.height), 10)
        self.space.add(segment_shape2)
        segment_shape2.elasticity = 0.8
        segment_shape2.friction = 1.0

        self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100

    def render(self, screen):
        screen.fill(self.background_color)
        background = load_image("interface.png")
        
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 35)
        
        text_score = font.render(f"{self.score}", 1, (0, 0, 0))
        screen.blit(text_score, (385, 300))   # в каких то координатах

        text_time = font.render(f"{time.time() - self.start_time:.2f}", 1, (0, 0, 0))   # время игры
        screen.blit(text_time, (370, 410))

        text_rows = font.render(f"{self.rows}", 1, (0, 0, 0))
        screen.blit(text_rows, (370, 445))

        cube = Cube(self.color, self.x_figure, self.y_figure)
        if not cube.check_collide(self.horizontal_borders, self.vertical_borders):
            cube.render(screen)

            self.y_figure += 2

        else:
            new_sand = Sand(self.color, self.x_figure, self.y_figure, self.space)
            self.sand.append(new_sand)

            self.y_figure = -100
            self.x_figure = 100
            self.color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 100

        self.space.step(1 / 60)
        self.space.debug_draw(self.draw_options)

    def events_processing(self, event):
        new_window = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:   # вернуться в меню
                new_window = self.open_main()
            if event.key == pygame.K_RIGHT:
                self.x_figure += 10
            if event.key == pygame.K_LEFT:
                self.x_figure -= 10
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

        for step_y in range(0, 100, 20):
            for step_x in range(0, 100, 20):
                self.create_circle((x + step_x, y + step_y))

    def create_circle(self, pos):
        circle_mass = 1
        circle_size = (10, 10)
        circle_moment = pymunk.moment_for_circle(circle_mass, 0, 10, circle_size)
        circle_body = pymunk.Body(circle_mass, circle_moment)
        circle_body.position = pos
        circle_shape = pymunk.Circle(circle_body, 8, circle_size)
        circle_shape.elasticity = 0.1
        circle_shape.friction = 1
        circle_shape.color = self.color
        self.space.add(circle_body, circle_shape)
