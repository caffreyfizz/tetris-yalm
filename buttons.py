import pygame
from image_loading import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.buttons = pygame.sprite.Group()

    def is_clicked(self):
        x, y = pygame.mouse.get_pos()
        
        if self.x - 36 <= x <= self.x + 36 and self.y - 36 <= y <= self.y + 36:
            return self.name
        else:
            return False

class ButtonTurn(Button):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("rotate_button.png")
        self.name = "rotate"
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 385, 525

        self.buttons.add(self)

    def rotate(self, figure):
        figure.rotate()

class ButtonReady(Button):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("ready_button.png")
        self.name = "ready"
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 431, 525

        self.buttons.add(self)


class ButtonClue(Button):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("clue_button.png")
        self.name = "clue"
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 477, 525

        self.buttons.add(self)
