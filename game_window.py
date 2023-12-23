import pygame
import time
import os

from image_loading import load_image


class GameWindow:
    def __init__(self, width, height, mode):
        self.background_color = (0, 33, 56)
        self.width, self.height = width, height

        self.mode = mode

        self.score = 0
        self.rows = 0
        self.start_time = time.time()

    def render(self, screen):
        background = load_image("interface.png")
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 35)
        
        text_score = font.render(f"{self.score}", 1, (0, 0, 0))
        screen.blit(text_score, (385, 300))   # в каких то координатах

        text_time = font.render(f"{time.time() - self.start_time:.2f}", 1, (0, 0, 0))   # время игры
        screen.blit(text_time, (370, 410))   # в каких то координатах

        text_rows = font.render(f"{self.rows}", 1, (0, 0, 0))
        screen.blit(text_rows, (370, 445))   # в каких то координатах

    def events_processing(self, event):
        new_window = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:   # вернуться в меню
                new_window = self.open_main()

        return new_window

    def open_main(self):
        return [1, None]

    def set_score(self, new_score):
        self.score = new_score
        self.rows += 1
