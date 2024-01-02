import pygame
from image_loading import load_image


class Figure(pygame.sprite.Sprite):
    def __init__(self, color, img_name, next=True, *group):
        super().__init__(*group)

        self.image = load_image(img_name)

        self.rect = self.image.get_rect()
        self.next = next
        if next:
            self.rect.x = 470
            self.rect.y = 30
        else:
            self.rect.x = (335 - self.image.get_rect().width) // 2
            self.rect.y = -100

        self.color = color

        self.figures_sprites = pygame.sprite.Group()
        self.figures_sprites.add(self)

    def render(self, screen):
        self.figures_sprites.draw(screen)

    def move(self, speed, left_border, right_border):
        print(self.rect)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.x -= 10
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.x += 10
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rect.y += 10

        if self.check_collide(left_border):
            self.rect.x = 20
        if self.check_collide(right_border):
            self.rect.x = 335 - self.rect.width

        if not self.next:
            self.rect.y += speed

    def start(self):
        self.next = False
        self.rect.x = (335 - self.image.get_rect().width) // 2
        self.rect.y = -100

    def check_collide(self, border):
        if pygame.sprite.spritecollideany(self, border):
            return True

    def get_rect(self):
        return self.rect

    def rotate(self):
        pass

    def get_color(self):
        return self.color


class Ishaped(Figure):
    def __init__(self, color, next=True, *group):
        super().__init__(color, f"I_shape/I_{color}.png", *group, next)


class Jshaped(Figure):
    def __init__(self, color, next=True, *group):
        super().__init__(color, f"J_shape/J_{color}.png", *group, next)


class Lshaped(Figure):
    def __init__(self, color, next=True, *group):
        super().__init__(color, f"L_shape/L_{color}.png", *group, next)


class Oshaped(Figure):
    def __init__(self, color, next=True, *group):
        super().__init__(color, f"O_shape/O_{color}.png", *group, next)


class Sshaped(Figure):
    def __init__(self, color, next=True, *group):
        super().__init__(color, f"S_shape/S_{color}.png", *group, next)


class Tshaped(Figure):
    def __init__(self, color, next=True, *group):
        super().__init__(color, f"T_shape/T_{color}.png", *group, next)


class Zshaped(Figure):
    def __init__(self, color, next=True, *group):
        super().__init__(color, f"Z_shape/Z_{color}.png", *group, next)
