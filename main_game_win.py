import pygame
import time
import os

from image_loading import load_image


class MainWindow:
    def __init__(self, width, height):
        self.background_color = (0, 33, 56)
        self.width, self.height = width, height

        self.score = 0
        self.rows = 0

    def render(self, screen):
        filename = os.path.join('data\images', "interface.png")
        background = pygame.image.load(filename)
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 35)
        
        text_score = font.render(f"{self.score}", 1, (0, 0, 0))
        screen.blit(text_score, (385, 300))   # в каких то координатах

        text_time = font.render(f"{time.time}", 1, (0, 0, 0))   # время игры
        screen.blit(text_time, (370, 410))   # в каких то координатах

        text_rows = font.render(f"{self.rows}", 1, (0, 0, 0))
        screen.blit(text_rows, (370, 445))   # в каких то координатах


    def set_score(self, new_score):
        self.score = new_score
        self.rows += 1
