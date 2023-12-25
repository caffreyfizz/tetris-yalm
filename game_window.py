import pygame
import time
from image_loading import load_image
from figures import Cube


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class GameWindow:
    def __init__(self, width, height, mode):
        self.background_color = (0, 33, 56)
        self.width, self.height = width, height

        self.mode = mode
        
        self.x_figure, self.y_figure = 40, 40   # будет спавнится в рандомных координатах

        self.score = 0
        self.rows = 0
        self.start_time = time.time()

    def render(self, screen):
        background = load_image("interface.png")
        
        Border(20, 2, self.width // 2 - 20, 1)
        Border(20, self.height - 1, self.width // 2 - 20, self.height - 1)
        Border(20, 2, 20, self.height - 1)
        Border(self.width // 2 + 30, 2, self.width // 2 + 30, self.height - 1)
        
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 35)
        
        text_score = font.render(f"{self.score}", 1, (0, 0, 0))
        screen.blit(text_score, (385, 300))   # в каких то координатах

        text_time = font.render(f"{time.time() - self.start_time:.2f}", 1, (0, 0, 0))   # время игры
        screen.blit(text_time, (370, 410))

        text_rows = font.render(f"{self.rows}", 1, (0, 0, 0))
        screen.blit(text_rows, (370, 445))
        Cube(self.x_figure, self.y_figure, screen).render(horizontal_borders, vertical_borders)
        self.y_figure += 0.5

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
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
