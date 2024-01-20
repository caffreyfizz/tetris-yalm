import pygame
import time
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody

from figures import Ishaped, Jshaped, Lshaped, Oshaped, Sshaped, Tshaped, Zshaped
from b2d_figures import (FallingIshaped, FallingJshaped, FallingLshaped, FallingOshaped, FallingSshaped,
                         FallingTshaped, FallingZshaped)
from buttons import ButtonClue, ButtonReady, ButtonTurn, ButtonRestart, Button

from assets import load_image, RGB_COLORS, PPM, TIME_STEP, COUNT_OF_LEVELS

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class GameWindow:
    # функции инициализаций
    def __init__(self, width, height, mode, screen, level):
        pygame.mouse.set_visible(True)
        self.width, self.height = width, height
        self.level = level
        self.screen = screen

        self.figures_types = {"Ishaped": Ishaped, "Jshaped": Jshaped, "Lshaped": Lshaped,
                              "Oshaped": Oshaped, "Sshaped": Sshaped, "Tshaped": Tshaped,
                              "Zshaped": Zshaped}

        self.falling_figures_types = {"Ishaped": FallingIshaped, "Jshaped": FallingJshaped, "Lshaped": FallingLshaped,
                                      "Oshaped": FallingOshaped, "Sshaped": FallingSshaped, "Tshaped": FallingTshaped,
                                      "Zshaped": FallingZshaped}

        self.spawn_figure = None
        self.count_of_rotate = 0
        
        self.level = level

        self.score = 0
        self.start_time = time.time()

        self.box2d_init()
        self.load_lvl(level)

        self.colors = ["blue", "green", "pink", "purple", "yellow"]
        self.figures_init()
        self.load_buttons()

        self.fallen_figures = []

        self.isgame = True
        self.clue = False
        self.end_level_time = None
        self.game_result = None
        self.end_time = None
        self.clue_timer = None


    def figures_init(self):
        self.figures_button = pygame.sprite.Group()
        self.figures_and_coords = []
        self.coords_for_buttons = [(370, 275), (445, 275), (530, 275), (370, 385), (445, 380), (530, 380)]

        figure_index = 0

        for i in range(len(self.list_of_figures)):
            figure = self.figures_types[self.list_of_figures[i][0]](self.list_of_figures[i][1], figure_index)
            self.figures_and_coords.append((figure, self.coords_for_buttons[i]))
            figure.rect = figure.image.get_rect()
            figure.rect.x, figure.rect.y = self.coords_for_buttons[i]
            scale_figure = pygame.transform.scale(figure.image, (figure.image.get_rect().width // 1.6,
                                                                 figure.image.get_rect().height // 1.6))
            figure.image = scale_figure
            self.figures_button.add(figure)
            figure_index += 1

        fall_1 = False
        fall_2 = False
        fall_3 = False
        fall_4 = False
        self.figures_flags = {1: fall_1, 2: fall_2, 3: fall_3, 4: fall_4}

    def load_buttons(self):
        self.buttons = pygame.sprite.Group()
        self.rot_button = ButtonTurn(self.buttons)
        self.ready_button = ButtonReady(self.buttons)
        self.clue_button = ButtonClue(self.buttons)
        self.restart_button = ButtonRestart(self.buttons)

    def box2d_init(self):
        self.space = world(gravity=(0, -100))

        self.ground_body = self.space.CreateStaticBody(position=(0, 16), shapes=polygonShape(box=(30, 1)))
        self.left_body = self.space.CreateStaticBody(position=(25.4, 60), shapes=polygonShape(box=(1, 60)))
        self.right_body = self.space.CreateStaticBody(position=(10.4, 60), shapes=polygonShape(box=(1, 60)))

    def load_lvl(self, lvl):
        self.bottom_border = pygame.sprite.Group()
        self.left_border = pygame.sprite.Group()
        self.right_border = pygame.sprite.Group()
        Border(20, self.height - 1, self.width // 2 + 50, self.height, self.bottom_border)
        Border(114, -100, 114, self.height - 1, self.left_border)
        Border(244, -100, 244, self.height, self.right_border)

        with open(f"data/levels/{lvl}.txt") as file:
            data = [string for string in file.read().split("\n")][:-1]
        data_1 = data[0].split(";")

        self.height, self.figure_piece_size = int(data_1[0]), int(data_1[1])

        self.clues = [(int(coords.split(":")[0]) * self.figure_piece_size,
                       int(coords.split(":")[1]) * self.figure_piece_size) for coords in data_1[2].split(",")]

        self.list_of_figures = [(string.split(";")[0], string.split(";")[1]) for string in data[1:]]

    # функции игрового процесса
    def render(self, screen):
        if self.spawn_figure:
            self.spawn_figure.move(self.left_border, self.right_border)

        self.check_end()

        screen.fill((0, 0, 0))

        background = load_image("interface.png")
        screen.blit(background, (0, 0))

        screen.blit(load_image("pit.png"), (18, 0))

        self.text_render(screen)

        if self.clue and self.spawn_figure:
            self.show_clue(screen)

        if self.isgame:
            self.buttons.draw(screen)
            self.figures_button.draw(screen)

            if self.spawn_figure:
                self.spawn_figure.render(self.screen)

            for fall_figure in self.fallen_figures:
                fall_figure.render(screen)

            self.space.Step(TIME_STEP, 10, 10)
        else:
            self.end_render(screen)

    def end_render(self, screen):
        font = pygame.font.Font(None, 50)
        if self.game_result == "win":
            text_1 = f"счёт: {self.score}"
            text_2 = f"время: {self.end_time}"
            pos1 = (30, 100)
            pos2 = (30, 200)
            text_score = font.render(text_1, 1, (255, 255, 255))
            screen.blit(text_score, pos1)

            text_time = font.render(text_2, 1, (255, 255, 255))
            screen.blit(text_time, pos2)


    def buttons_check(self, mouse_position):
        for button in self.buttons:
            if button.is_clicked(mouse_position):
                res = button.is_clicked(mouse_position)
                return res

    def text_render(self, screen):
        font = pygame.font.Font(None, 35)

        if self.isgame:
            text_1 = f"{self.score}"
            text_2 = f"{time.time() - self.start_time:.1f}"
            pos1 = (503, 45)
            pos2 = (480, 80)
        else:
            text_1 = "you"
            text_2 = self.game_result
            pos1 = (490, 45)
            pos2 = (490, 80)
        text_score = font.render(text_1, 1, (255, 255, 255))
        screen.blit(text_score, pos1)

        text_time = font.render(text_2, 1, (255, 255, 255))
        screen.blit(text_time, pos2)

    def show_clue(self, screen):
        if not self.clue_timer:
            self.clue_timer = time.time()
        if self.clue_timer:
            if time.time() - self.clue_timer >= 2:
                self.clue = False
                self.clue_timer = None

        coords = self.clues[self.spawn_figure.get_index()]
        pygame.draw.line(screen, (255, 255, 0), (114 + coords[0], 440),
                         (114 + coords[1], 440), 8)

    def events_processing(self, event):
        new_window = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:   # вернуться в меню
                new_window = self.open_main()

        if self.isgame:
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = self.buttons_check(event.pos)

                if result == "restart":
                    new_window = self.open_game()

            self.game(event)

        if not self.isgame:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_result == "win":
                        new_window = [2, 2, str(min(int(self.level) + 1, COUNT_OF_LEVELS))]
                    if self.game_result == "lose":
                        new_window = [2, 2, self.level]

        return new_window

    def game(self, event):
        if self.isgame:
            if event.type == pygame.KEYDOWN:
                if self.spawn_figure and event.key == pygame.K_UP:
                    self.spawn_figure.rotate()
                    self.count_of_rotate += 1

                if self.spawn_figure and event.key == pygame.K_DOWN:
                    self.start_fall()
                    self.delete_spawned()

                if event.key == pygame.K_1 and not self.figures_flags[1]:
                    fig = self.figures_and_coords[0]
                    self.spawn_figure = self.figures_types[fig[0].copy()](fig[0].color, fig[0].get_index())
                    self.spawn_figure.start()

                if event.key == pygame.K_2 and not self.figures_flags[2]:
                    fig = self.figures_and_coords[1]
                    self.spawn_figure = self.figures_types[fig[0].copy()](fig[0].color, fig[0].get_index())
                    self.spawn_figure.start()

                if event.key == pygame.K_3 and not self.figures_flags[3]:
                    fig = self.figures_and_coords[2]
                    self.spawn_figure = self.figures_types[fig[0].copy()](fig[0].color, fig[0].get_index())
                    self.spawn_figure.start()

                if event.key == pygame.K_4 and not self.figures_flags[4]:
                    fig = self.figures_and_coords[3]
                    self.spawn_figure = self.figures_types[fig[0].copy()](fig[0].color, fig[0].get_index())
                    self.spawn_figure.start()

            if event.type == pygame.MOUSEBUTTONDOWN:
                result = self.buttons_check(event.pos)

                if result == "rotate" and self.spawn_figure:
                    self.spawn_figure.rotate()
                    self.count_of_rotate += 1

                if result == "ready" and self.spawn_figure:
                    self.start_fall()
                    self.delete_spawned()

                if result == "clue":
                    if self.spawn_figure:
                        self.clue = True

                for i, figure in enumerate(self.figures_and_coords):
                    if figure[0].is_clicked(figure[1], event.pos) and not self.figures_flags[i + 1]:
                        self.spawn_figure = self.figures_types[figure[0].copy()](figure[0].color, figure[0].get_index())
                        self.spawn_figure.start()

    def delete_spawned(self):
        index = self.spawn_figure.get_index()
        self.figures_flags[index + 1] = True
        self.figures_and_coords[index][0].delete()
        self.spawn_figure = None
        self.count_of_rotate = 0

    def start_fall(self):
        x, y = self.spawn_figure.get_coords()
        fallen_figure = (self.falling_figures_types[self.spawn_figure.get_type()]
                         (self.spawn_figure.get_color(), self.space, x, y, 30, self.count_of_rotate))
        self.fallen_figures.append(fallen_figure)
        self.score += 1

    def check_end(self):
        if not bool(self.figures_button):
            if not self.end_level_time:
                self.end_level_time = time.time()

        if self.isgame and self.end_level_time and int(time.time() - self.end_level_time) >= 3:
            self.check_win()
            self.isgame = False

    def check_win(self):
        current_y = None
        all_y = []
        for fall_figure in self.fallen_figures:
            all_y.append(fall_figure.get_y_coord())
        if all_y:
            current_y = min(all_y)

        if current_y:
            if current_y > 600 - (self.height * self.figure_piece_size + 180):
                self.game_result = "win"
                self.change_results()
                self.end_time = round(time.time() - self.start_time, 1)
            else:
                self.game_result = "lose"

    def change_results(self):
        with open(f"data/results.txt", "r") as file:
            res_lvl = int(file.read())
        with open(f"data/results.txt", "w") as file:
            file.write(f"{max(int(self.level), res_lvl)}")

    def open_main(self):
        return [1, None]

    def open_game(self):
        return [2, 2, self.level]


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, *group):
        super().__init__(*group)
        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)