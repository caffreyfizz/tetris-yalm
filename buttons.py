import pygame
from assets import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

    def is_clicked(self, mouse_position):
        x, y = mouse_position
        
        if self.rect.x - 36 <= x <= self.rect.x + 36 and self.rect.y - 36 <= y <= self.rect.y + 36:
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

    def rotate(self, figure):
        figure.rotate()


class ButtonReady(Button):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("ready_button.png", colorkey=-1)
        self.name = "ready"
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 431, 525


class ButtonClue(Button):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("clue_button.png")
        self.name = "clue"
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 477, 525


class ButtonRestart(Button):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("rotate_button.png")
        self.name = "restart"
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 530, 175
