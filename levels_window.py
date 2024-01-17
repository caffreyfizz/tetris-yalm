import pygame

from assets import load_image, COUNT_OF_LEVELS


class LevelsWindow:
    def __init__(self, width, height):
        pygame.mouse.set_visible(False)
        self.background_color = (0, 17, 28)
        self.width, self.height = width, height

        self.levels_window_sprites = pygame.sprite.Group()
        self.cursor_pos = pygame.mouse.get_pos()
        self.cursor = load_image("cursor.png")
        self.sliding = False

        return_button_sprite = pygame.sprite.Sprite()
        return_button_sprite.image = load_image("return_button.png")
        return_button_sprite.rect = return_button_sprite.image.get_rect()
        self.levels_window_sprites.add(return_button_sprite)
        return_button_sprite.rect.x = 10
        return_button_sprite.rect.y = 10

        self.create_levels_buttons()

    def create_levels_buttons(self):
        x, y = 150, 100
        for i in range(COUNT_OF_LEVELS):
            lvl_button = pygame.sprite.Sprite()
            lvl_button.image = load_image(f"levels/{i + 1}.png")
            lvl_button.rect = lvl_button.image.get_rect()
            self.levels_window_sprites.add(lvl_button)
            lvl_button.rect.x = x
            lvl_button.rect.y = y
            y += 120

    def events_processing(self, event):
        new_window = None
        new_level = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:  # вернуться в меню
                new_window = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                new_window = self.check_buttons(event.pos)
                if not new_window:
                    new_window = 2
                    new_level = self.check_levels(event.pos)

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                self.cursor_pos = event.pos

        return [new_window, 2, new_level]

    def render(self, screen):
        screen.fill(self.background_color)
        self.draw_stars(screen)

        # рендер всех спрайтов
        self.levels_window_sprites.draw(screen)

        font = pygame.font.Font(None, 24)
        text = font.render(f"выберите уровень", 1, (255, 255, 255))
        screen.blit(text, (220, 60))

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
        for i, sprite in enumerate(self.levels_window_sprites):
            if self.check_click(sprite.rect, mouse_position):
                if i == 0:
                    return 1

    def check_levels(self, mouse_position):
        for i, sprite in enumerate(self.levels_window_sprites):
            if self.check_click(sprite.rect, mouse_position):
                if i > 0:
                    return i

    def check_click(self, object_rect, mouse_position):
        x, y, width, height = object_rect.x, object_rect.y, object_rect.width, object_rect.height
        if (x <= mouse_position[0] <= x + width
                and y <= mouse_position[1] <= y + height):
            return True
        return False
