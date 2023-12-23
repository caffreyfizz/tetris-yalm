import pygame

from image_loading import load_image


class MainWindow:
    def __init__(self, width, height):
        pygame.mouse.set_visible(False)
        self.background_color = (0, 33, 56)
        self.width, self.height = width, height

        self.main_window_sprites = pygame.sprite.Group()

        # спрайт с названием игры
        title_sprite = pygame.sprite.Sprite()
        title_sprite.image = load_image("title.jpg")
        title_sprite.rect = title_sprite.image.get_rect()
        self.main_window_sprites.add(title_sprite)
        title_sprite.rect.x = (self.width - title_sprite.image.get_rect()[2]) // 2
        title_sprite.rect.y = (self.height - title_sprite.image.get_rect()[3]) // 4

        # спрайт с кнопкой начала игры
        play_button_sprite = pygame.sprite.Sprite()
        play_button_sprite.image = load_image("play_button.png")
        play_button_sprite.rect = play_button_sprite.image.get_rect()
        self.main_window_sprites.add(play_button_sprite)
        play_button_sprite.rect.x = (self.width - play_button_sprite.image.get_rect()[2]) // 2
        play_button_sprite.rect.y = (self.height - play_button_sprite.image.get_rect()[3]) // 2 + 60

        levels_button_sprite = pygame.sprite.Sprite()
        levels_button_sprite.image = load_image("levels_button.png")
        levels_button_sprite.rect = levels_button_sprite.image.get_rect()
        self.main_window_sprites.add(levels_button_sprite)
        levels_button_sprite.rect.x = (self.width - levels_button_sprite.image.get_rect()[2]) // 2 - 30
        levels_button_sprite.rect.y = (self.height - play_button_sprite.image.get_rect()[3]) // 2 + 230


        # спрайт с кнопкой настроек
        settngs_button_sprite = pygame.sprite.Sprite()
        settngs_button_sprite.image = load_image("settings_button.png")
        settngs_button_sprite.rect = settngs_button_sprite.image.get_rect()
        self.main_window_sprites.add(settngs_button_sprite)
        settngs_button_sprite.rect.x = (self.width - levels_button_sprite.image.get_rect()[2]) // 2 + 130
        settngs_button_sprite.rect.y = (self.height - play_button_sprite.image.get_rect()[3]) // 2 + 230

        self.score = 0
        # self.set_score()

        self.cursor_pos = pygame.mouse.get_pos()
        self.cursor = load_image("cursor.png")

    def render(self, screen):
        screen.fill(self.background_color)
        self.draw_stars(screen)

        # рендер всех спрайтов
        self.main_window_sprites.draw(screen)

        font = pygame.font.Font(None, 24)
        text = font.render(f"лучший рекорд: {self.score}", 1, (255, 255, 255))
        screen.blit(text, (20, 20))

        if pygame.mouse.get_focused():
            screen.blit(self.cursor, self.cursor_pos)

    def set_score(self):
        with open("") as file:
            results = [int(res) for res in file.read().split()]

        self.score = max(results)

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
            screen.fill(pygame.Color('white'),
                        (stars[i][0],
                         stars[i][1], 2, 2))

    def check_buttons(self, mouse_position):
        for i, sprite in enumerate(self.main_window_sprites):
            if self.check_click(sprite.rect,  mouse_position):
                if i == 1: # главное меню
                    return self.open_game_window()
                if i == 2: # уровни
                    return self.open_levels()
                if i == 3: # настройки
                    return self.open_settings_window()

    def check_click(self, object_rect,  mouse_position):
        x, y, width, height = object_rect.x, object_rect.y, object_rect.width, object_rect.height
        if (x <= mouse_position[0] <= x + width
                and y <= mouse_position[1] <= y + height):
            return True
        return False

    def events_processing(self, event):
        new_window = None

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                self.cursor_pos = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                new_window = self.check_buttons(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                new_window = self.open_game_window()

        return new_window

    def open_game_window(self):
        return [2, None]

    def open_settings_window(self):
        return [3, None]

    def open_levels(self):
        return [4, None]
