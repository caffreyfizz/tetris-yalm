import pygame
from image_loading import load_image


class Figure(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        
        self.figures_sprites = pygame.sprite.Group()

    def render(self, horizontal_borders, vertical_borders):
        self.figures_sprites.draw(self.screen)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            pass
        if pygame.sprite.spritecollideany(self, vertical_borders):
            pass

class Cube(Figure):

    def __init__(self, x, y, screen):
        super().__init__()
        self.image = load_image("cube.png")
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.screen = screen

        self.figures_sprites.add(self)