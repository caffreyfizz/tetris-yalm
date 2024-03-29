import pygame

from assets import load_image, PPM, WINDOW_WIDTH, WINDOW_HEIGHT, RGB_COLORS


class Figure(pygame.sprite.Sprite):
    def __init__(self, color, img_name, index, *group):
        super().__init__(*group)

        self.image = load_image(img_name)

        self.rect = self.image.get_rect()
        self.rect.x = self.x = 100
        self.rect.y = self.y = 100

        self.color = color
        self.index = index
        self.is_del = False

        self.figures_sprites = pygame.sprite.Group()
        self.figures_sprites.add(self)

    def render(self, screen):
        self.figures_sprites.draw(screen)

    def move(self, left_border, right_border):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.x -= 3
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.x += 3

        self.rect.x = self.x

        if self.check_collide(left_border):
            self.x = 114
        if self.check_collide(right_border):
            self.x = 244 - self.rect.width

        self.rect.x, self.rect.y = self.x, self.y

    def start(self):
        self.rect.x = self.x = (335 - self.rect.width) / 2
        self.rect.y = self.y = 50

    def check_collide(self, border):
        if pygame.sprite.spritecollideany(self, border):
            return True

    def get_rect(self):
        return self.rect

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = self.x = (335 - self.rect.width) / 2
        self.rect.y = self.y

    def get_color(self):
        return self.color
    
    def is_clicked(self, coords, mouse_pos):
        if not self.is_del:
            if coords[0] <= mouse_pos[0] <= coords[0] + self.image.get_rect().width and \
            coords[1] <= mouse_pos[1] <= coords[1] + self.image.get_rect().height:
                return self

    def copy(self):
        return self.__class__.__name__

    def get_type(self):
        return self.type

    def get_coords(self):
        return self.rect.x, self.rect.y

    def get_index(self):
        return self.index

    def delete(self):
        self.kill()
        self.is_del = True


class Ishaped(Figure):
    def __init__(self, color, index, *group):
        self.type = "Ishaped"
        super().__init__(color, f"I_shape/I_{color}.png", index, *group)


class Jshaped(Figure):
    def __init__(self, color, index, *group):
        self.type = "Jshaped"
        super().__init__(color, f"J_shape/J_{color}.png", index, *group)


class Lshaped(Figure):
    def __init__(self, color, index, *group):
        self.type = "Lshaped"
        super().__init__(color, f"L_shape/L_{color}.png", index, *group)


class Oshaped(Figure):
    def __init__(self, color, index, *group):
        self.type = "Oshaped"
        super().__init__(color, f"O_shape/O_{color}.png", index, *group)


class Sshaped(Figure):
    def __init__(self, color, index, *group):
        self.type = "Sshaped"
        super().__init__(color, f"S_shape/S_{color}.png", index, *group)


class Tshaped(Figure):
    def __init__(self, color, index, *group):
        self.type = "Tshaped"
        super().__init__(color, f"T_shape/T_{color}.png", index, *group)


class Zshaped(Figure):
    def __init__(self, color, index, *group):
        self.type = "Zshaped"
        super().__init__(color, f"Z_shape/Z_{color}.png", index, *group)