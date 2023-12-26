import pygame
from image_loading import load_image


class Figure(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        
        self.figures_sprites = pygame.sprite.Group()

    def render(self, screen):
        self.figures_sprites.draw(screen)

    def check_collide(self, *groups):
        for group in groups:
            if pygame.sprite.spritecollideany(self, group):
                return True


class Cube(Figure):
    def __init__(self, color, x, y, *group):
        super().__init__(*group)
        self.image = load_image("cube.png")
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

        self.figures_sprites.add(self)

    def render(self, screen, color):
        pygame.draw.rect(screen, color, (self.rect.x, self.rect.y, self.rect.width, self.rect.width))