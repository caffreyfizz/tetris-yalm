import pygame

from assets import load_image


class Slider:
    def __init__(self, window_width, window_height, mode):
        self.start_x, self.start_y = (window_width - 300) // 2, 200
        self.window_width, self.window_height = window_width, window_height

        self.step_x, self.step_y = None, None
        self.width = 10
        self.height = 100
        self.mode = mode
        self.x, self.y = self.start_x + self.mode * 3, self.start_y - 50

    def check(self, mouse_x):
        if self.x <= mouse_x <= self.x + self.width:
            return True
        return False

    def set_steps_values(self, mouse_x):
        if self.check(mouse_x):
            self.step_x = mouse_x - self.x

    def del_steps(self):
        self.step_x = None

    def check_mode(self):
        self.mode = round(self.x - self.start_x) // 3
        pygame.mixer.music.set_volume(self.mode * 0.01)

    def move(self, mouse_x):
        if self.step_x:
            self.x = mouse_x - self.step_x
            if self.x < self.start_x:
                self.x = self.start_x
            if self.x > self.window_width - self.start_x:
                self.x = self.window_width - self.start_x
            self.check_mode()

    def get_mode(self):
        return self.mode

    def render(self, screen):
        pygame.draw.line(screen, (100, 100, 100), (self.start_x, self.start_y),
                         (self.window_width - self.start_x, self.start_y), width=5)
        pygame.draw.rect(screen, (170, 170, 170),
                         (self.x, self.y, self.width, self.height))

        font = pygame.font.Font(None, 24)
        text = font.render(f"{self.mode}", 1, (255, 255, 255))
        screen.blit(text, (self.x, self.y + 105))


class SettingsWindow:
    def __init__(self, width, height, mode):
        pygame.mouse.set_visible(False)
        self.background_color = (0, 17, 28)
        self.width, self.height = width, height

        self.settings_window_sprites = pygame.sprite.Group()
        self.slider = Slider(width, height, mode)
        self.cursor_pos = pygame.mouse.get_pos()
        self.cursor = load_image("cursor.png")
        self.sliding = False

        return_button_sprite = pygame.sprite.Sprite()
        return_button_sprite.image = load_image("return_button.png")
        return_button_sprite.rect = return_button_sprite.image.get_rect()
        self.settings_window_sprites.add(return_button_sprite)
        return_button_sprite.rect.x = 10
        return_button_sprite.rect.y = 10

        self.music_is_paused = False

    def events_processing(self, event):
        new_window = None
        new_mode = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:  # вернуться в меню
                new_window = 1
            if event.key == pygame.K_SPACE:
                if not self.music_is_paused:
                    pygame.mixer.music.pause()
                    self.music_is_paused = True
                elif self.music_is_paused:
                    pygame.mixer.music.unpause()
                    self.music_is_paused = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                new_window = self.check_buttons(event.pos)
            self.slider.set_steps_values(event.pos[0])
            if self.slider.check(event.pos[0]):
                self.sliding = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.slider.del_steps()
            self.sliding = False
            new_mode = self.slider.get_mode()
        if event.type == pygame.MOUSEMOTION:
            if self.sliding:
                self.slider.move(event.pos[0])
            if pygame.mouse.get_focused():
                self.cursor_pos = event.pos

        return [new_window, 1, new_mode]

    def render(self, screen):
        screen.fill(self.background_color)
        self.draw_stars(screen)

        # рендер всех спрайтов
        self.settings_window_sprites.draw(screen)

        self.slider.render(screen)

        font = pygame.font.Font(None, 35)
        text = font.render(f"громкость", 1, (255, 255, 255))
        screen.blit(text, (245, 80))

        screen.blit(load_image("backspace.png"), (200, 300))
        text = font.render(f"вернуться в меню", 1, (255, 255, 255))
        screen.blit(text, (100, 300))

        screen.blit(load_image("down.png"), (200, 360))
        text = font.render(f"запустить фигуру", 1, (255, 255, 255))
        screen.blit(text, (100, 360))

        if pygame.mouse.get_focused():
            screen.blit(self.cursor, self.cursor_pos)


    def draw_stars(self, screen):
        stars = [(575, 164), (139, 1), (541, 29), (101, 459), (24, 267), (545, 470), (183, 509),
                 (326, 420), (524, 250), (441, 177), (146, 96), (122, 469), (218, 539), (481, 487),
                 (58, 141), (531, 55), (400, 92), (303, 401), (11, 52), (86, 61), (355, 372),
                 (256, 141), (228, 257), (473, 516), (25, 283), (194, 404), (390, 415), (336, 191),
                 (371, 559), (250, 504), (156, 114), (38, 408), (250, 497), (294, 570), (578, 577),
                 (155, 234), (441, 591), (236, 435), (465, 520), (222, 458), (553, 585), (430, 423),
                 (136, 347), (383, 525), (248, 282), (33, 237), (140, 525), (160, 378), (308, 201),
                 (401, 284), (409, 544), (568, 286), (0, 479), (142, 60), (167, 64), (335, 435),
                 (222, 322), (207, 428), (180, 209), (349, 570), (545, 312), (224, 482), (129, 338),
                 (515, 295), (467, 54), (430, 245), (239, 40), (50, 155), (243, 421), (144, 569),
                 (26, 51), (501, 237), (590, 244), (564, 78), (85, 424), (194, 530), (485, 179),
                 (248, 108), (94, 490), (273, 293), (462, 563), (405, 283), (264, 204), (446, 513),
                 (559, 355), (125, 325), (262, 392), (87, 74), (492, 560), (217, 306), (435, 521),
                 (247, 315), (373, 184), (244, 195), (204, 478), (321, 409), (417, 408), (283, 184),
                 (538, 535), (104, 585)]

        for i in range(100):
            screen.fill(pygame.Color(128, 128, 128),
                        (stars[i][0],
                         stars[i][1], 2, 2))

    def check_buttons(self, mouse_position):
        for i, sprite in enumerate(self.settings_window_sprites):
            if self.check_click(sprite.rect, mouse_position):
                if i == 0:
                    return 1

    def check_click(self, object_rect, mouse_position):
        x, y, width, height = object_rect.x, object_rect.y, object_rect.width, object_rect.height
        if (x <= mouse_position[0] <= x + width
                and y <= mouse_position[1] <= y + height):
            return True
        return False