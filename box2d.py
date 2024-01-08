import pygame
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody
import sys, os

PPM = 4.0
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

world = world(gravity=(0, -1000))

# walls
ground_body = world.CreateStaticBody(position=(0, 0), shapes=polygonShape(box=(75, 1)))
left_body = world.CreateStaticBody(position=(75, 150), shapes=polygonShape(box=(1, 175)))
right_body = world.CreateStaticBody(position=(0, 150), shapes=polygonShape(box=(1, 175)))

# prepare image for pygame.sprite
def load_image(name, colorkey=None):
    fullname = os.path.join('data/images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()

    return image

# sprite
class SomeFigure(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image("T_shape/T_blue.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 100, 30

        self.figures_sprites = pygame.sprite.Group()
        self.figures_sprites.add(self)
    
    def render(self):
        self.rect.y += 1
        self.figures_sprites.draw(screen)

figure = SomeFigure()


def create_circles(pos):
    x, y = pos[0] // 4, (600 - pos[1]) // 4
    for step_y in range(0, 60, 16):
        step_y = -step_y // 4
        for step_x in range(0, 60, 16):
            print(x + step_x, y + step_y)
            step_x = step_x // 4
            body = world.CreateDynamicBody(position=(x + step_x, y + step_y))
            circle = body.CreateCircleFixture(radius=1, density=1, friction=1)
        print()


def create_rectangles(pos):
    for step_y in range(0, 60, 15):
        for step_x in range(0, 60, 15):
            body = world.CreateDynamicBody(position=(pos[0] + step_x, pos[1] + step_y), angle=0)
            box = body.CreatePolygonFixture(box=(1, 1), density=1, friction=1)


colors = {staticBody: (255, 255, 255, 255),
          dynamicBody: (0, 35, 245, 127)
}


def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)


polygonShape.draw = my_draw_polygon


def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type],
                       [int(x) for x in position], int(circle.radius * PPM))


circleShape.draw = my_draw_circle

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            create_circles(event.pos)
    screen.fill((0, 0, 0, 0))
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)
    world.Step(TIME_STEP, 10, 10)
    figure.render()
    pygame.display.flip()
    clock.tick(TARGET_FPS)
pygame.quit()
