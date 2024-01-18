import pygame
import time
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody

from figures import Ishaped, Jshaped, Lshaped, Oshaped, Sshaped, Tshaped, Zshaped
from b2d_figures import (FallingIshaped, FallingJshaped, FallingLshaped, FallingOshaped, FallingSshaped,
                         FallingTshaped, FallingZshaped)
from buttons import ButtonClue, ButtonReady, ButtonTurn, Button

from assets import load_image, RGB_COLORS, PPM, TIME_STEP


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class GameWindow:
    # функции инициализаций
    def __init__(self, width, height, mode, screen, level):
        pygame.mouse.set_visible(True)
        self.width, self.height = width, height
        self.figure_piece_size = 30
        self.screen = screen

        self.figures_types = {"Ishaped": Ishaped, "Jshaped": Jshaped, "Lshaped": Lshaped,
                              "Oshaped": Oshaped, "Sshaped": Sshaped, "Tshaped": Tshaped,
                              "Zshaped": Zshaped}

        self.falling_figures_types = {"Ishaped": FallingIshaped, "Jshaped": FallingJshaped, "Lshaped": FallingLshaped,
                                      "Oshaped": FallingOshaped, "Sshaped": FallingSshaped, "Tshaped": FallingTshaped,
                                      "Zshaped": FallingZshaped}

        self.spawn_figure = None
        self.count_of_rotate = 0
        
        self.level = mode

        self.score = 0
        self.rows = 0
        self.start_time = time.time()

        self.static_figures = pygame.sprite.Group()

        self.box2d_init()
        self.load_lvl(level)

        self.colors = ["blue", "green", "pink", "purple", "yellow"]
        self.figures_button = pygame.sprite.Group()

        self.figures_init()
        self.load_buttons()

        self.fallen_figures = []

        self.clue = None

    def figures_init(self):
        self.figures_and_coords = []
        self.coords_for_buttons = [(370, 275), (445, 275), (530, 275), (370, 385), (445, 380), (530, 380)]

        for i in range(len(self.list_of_figures)):
            figure = self.figures_types[self.list_of_figures[i][0]](self.list_of_figures[i][1])
            self.figures_and_coords.append((figure, self.coords_for_buttons[i]))
            figure.rect = figure.image.get_rect()
            figure.rect.x, figure.rect.y = self.coords_for_buttons[i]
            scale_figure = pygame.transform.scale(figure.image, (figure.image.get_rect().width // 1.6,
                                                                 figure.image.get_rect().height // 1.6))
            figure.image = scale_figure
            self.figures_button.add(figure)

    def load_buttons(self):
        self.buttons = pygame.sprite.Group()
        self.rot_button = ButtonTurn(self.buttons)
        self.ready_button = ButtonReady(self.buttons)
        self.clue_button = ButtonClue(self.buttons)

    def box2d_init(self):
        self.space = world(gravity=(0, -10))

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

        self.height, self.figure_piece_size = int(data[0].split(";")[0]), int(data[0].split(";")[1])
        self.list_of_figures = [(string.split(";")[0], string.split(";")[1]) for string in data[1:]]

    # функции игрового процесса
    def render(self, screen):
        screen.fill((0, 0, 0))

        background = load_image("interface.png")
        screen.blit(background, (0, 0))

        self.text_render(screen)

        self.static_figures.update()
        self.static_figures.draw(screen)

        self.buttons.draw(screen)
        self.figures_button.draw(screen)

        if self.spawn_figure:
            self.spawn_figure.render(self.screen)

        for figure in self.fallen_figures:
            figure.render(screen)
            print(figure.get_y_coord())

        self.space.Step(TIME_STEP, 10, 10)

    def buttons_check(self, mouse_position):
        for button in self.buttons:
            if button.is_clicked(mouse_position):
                res = button.is_clicked(mouse_position)
                return res

    def text_render(self, screen):
        font = pygame.font.Font(None, 35)

        text_score = font.render(f"{self.score}", 1, (255, 255, 255))
        screen.blit(text_score, (503, 45))

        text_time = font.render(f"{time.time() - self.start_time:.2f}", 1, (255, 255, 255))
        screen.blit(text_time, (480, 80))

    def events_processing(self, event):
        new_window = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:   # вернуться в меню
                new_window = self.open_main()

        self.game(event)
        
        return new_window

    def game(self, event):
        if event.type == pygame.KEYDOWN:
            if self.spawn_figure and event.key == pygame.K_UP:
                self.spawn_figure.rotate()
            if self.spawn_figure and event.key == pygame.K_DOWN:
                self.start_fall()
                self.spawn_figure = None
                self.count_of_rotate = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            result = self.buttons_check(event.pos)

            if result == "rotate" and self.spawn_figure:
                self.spawn_figure.rotate()
                self.count_of_rotate += 1

            if result == "ready" and self.spawn_figure:
                self.start_fall()
                self.spawn_figure = None
                self.count_of_rotate = 0

            if result == "clue":
                print("clue")

            for figure in self.figures_and_coords:
                if figure[0].is_clicked(figure[1], event.pos):
                    self.spawn_figure = self.figures_types[figure[0].copy()](figure[0].color)
                    print(self.spawn_figure)
                    self.spawn_figure.start()

        if self.spawn_figure:
            self.spawn_figure.move(self.left_border, self.right_border)

    def start_fall(self):
        x, y = self.spawn_figure.get_coords()
        fallen_figure = (self.falling_figures_types[self.spawn_figure.get_type()]
                         (self.spawn_figure.get_color(), self.space, x, y, 30, self.count_of_rotate))
        self.fallen_figures.append(fallen_figure)

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