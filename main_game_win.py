import pygame
import time

from image_loading import load_image


class MainWindow:
    def __init__(self, width, height):
        self.background_color = (0, 33, 56)
        self.width, self.height = width, height

        self.score = 0
        self.rows = 0

    def render(self, screen):
        background = pygame.image.load("interface.png")
        screen.blit(background, (0, 0))
        font = pygame.font.Font(None, 24)
        
        text_score = font.render(f"{self.score}", 1, (255, 255, 255))
        screen.blit(text_score, (20, 20))   # в каких то координатах

        text_time = font.render(f"{time.time}", 1, (255, 255, 255))   # время игры
        screen.blit(text_time, (20, 20))   # в каких то координатах

        text_rows = font.render(f"{self.rows}", 1, (255, 255, 255))
        screen.blit(text_rows, (20, 20))   # в каких то координатах


    def set_score(self, new_score):
        self.score = new_score
        self.rows += 1
