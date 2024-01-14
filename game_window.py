import random

import pygame
import time
from image_loading import load_image
from figures import Ishaped, Jshaped, Lshaped, Oshaped, Sshaped, Tshaped, Zshaped
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody
from buttons import ButtonClue, ButtonReady, ButtonTurn, Button


RGB_COLORS = {"blue": (22, 128, 212, 100), "green": (0, 125, 104, 100), "yellow": (253, 187, 3, 100),
              "pink": (198, 23, 88, 100), "purple": (98, 5, 198, 100)}
PPI = 10


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class GameWindow:
    def __init__(self, width, height, mode, screen, level):
        pygame.mouse.set_visible(True)
        self.width, self.height = width, height

        self.figure_piece_size = 30

        self.figures_types = {"Ishaped": Ishaped, "Jshaped": Jshaped, "Lshaped": Lshaped,
                              "Oshaped": Oshaped, "Sshaped": Sshaped, "Tshaped": Tshaped,
                              "Zshaped": Zshaped}

        self.level = mode

        self.score = 0
        self.rows = 0
        self.start_time = time.time()

        self.fallen_figures = pygame.sprite.Group()

        if level == 1:
            pass
        elif level == 2:
            self.figures = ["Ishaped", "Oshaped", "Jshaped", "Lshaped"]
        elif level == 3:
            pass

        self.box2d_init()
        self.load_lvl(level)

        self.colors = ["blue", "green", "pink", "purple", "yellow"]
        self.coords_for_buttons = [(380, 275), (465, 275), (535, 275), (380, 385), (465, 380), (535, 380)]
        self.figures_button = pygame.sprite.Group()
        
        for i in range(len(self.figures)):
            figure = self.figures_types[self.figures[i]](random.choice(self.colors))
            figure.x, figure.y = self.coords_for_buttons[i]
            figure.figures_sprites.draw(screen)

    def box2d_init(self):
        self.space = world(gravity=(0, -1000))

        self.ground_body = self.space.CreateStaticBody(position=(0, 0), shapes=polygonShape(box=(30, 1)))
        self.left_body = self.space.CreateStaticBody(position=(30, 60), shapes=polygonShape(box=(1, 60)))
        self.right_body = self.space.CreateStaticBody(position=(0, 60), shapes=polygonShape(box=(1, 60)))

    def load_lvl(self, lvl):
        self.bottom_border = pygame.sprite.Group()
        self.left_border = pygame.sprite.Group()
        self.right_border = pygame.sprite.Group()
        Border(20, self.height - 1, self.width // 2 + 50, self.height, self.bottom_border)
        Border(20, -100, 20, self.height - 1, self.left_border)
        Border(self.width // 2 + 35, -100, self.width // 2 + 35, self.height, self.right_border)

        with open(f"data/levels/{lvl}.txt") as file:
            data = [string for string in file.read().split("\n")][:-1]

        self.height = int(data[0]) * self.figure_piece_size
        self.figures = [(string.split(";")[0], string.split(";")[1]) for string in data[1:]]

    def render(self, screen):
        screen.fill((0, 0, 0))

        background = load_image("interface.png")
        screen.blit(background, (0, 0))

        font = pygame.font.Font(None, 35)

        text_score = font.render(f"{self.score}", 1, (255, 255, 255))
        screen.blit(text_score, (503, 45))

        text_time = font.render(f"{time.time() - self.start_time:.2f}", 1, (255, 255, 255))
        screen.blit(text_time, (480, 80))

        self.button = Button()
        self.rot_button = ButtonTurn()
        self.ready_button = ButtonReady()
        self.clue_button = ButtonClue()

        self.fallen_figures.update()
        self.fallen_figures.draw(screen)

        """self.figure.get_rect().y = -100
        self.figure.get_rect().x = 100

        self.figure = self.next_figure
        self.figure.start()
        self.next_figure = random.choice(self.figures_types)(random.choice(self.colors))"""

    def events_processing(self, event):
        new_window = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:   # вернуться в меню
                new_window = self.open_main()
            if event.key == pygame.K_UP:
                self.figure.rotate()
            if event.key == pygame.K_ESCAPE:
                self.pause()
            if event.key == pygame.MOUSEBUTTONDOWN:
                result = self.button.is_clicked()
                if result == "rotate":
                    self.rot_button.rotate(self.figure)
                elif result == "ready":
                    pass
                elif result == "clue":
                    pass

        return new_window

    def open_main(self):
        return [1, None]

    def set_score(self, new_score):
        self.score = new_score
        self.rows += 1

    def pause(self):
        pass


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, *group):
        super().__init__(*group)
        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)