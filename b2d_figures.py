import pygame

from assets import load_image, PPM, WINDOW_WIDTH, WINDOW_HEIGHT, RGB_COLORS
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody, weldJoint


def my_draw_polygon(polygon, body, fixture, color, screen):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], WINDOW_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, color, vertices)
    return vertices


polygonShape.draw = my_draw_polygon


class FallingFigure:
    def __init__(self, color, space,  x, y, width):
        self.color = RGB_COLORS[color]
        self.space = space
        self.width = width
        self.x, self.y = x, y

        self.box2d_init()

    def box2d_init(self):
        pass

    def render(self, screen):
        for body, box in self.bodies:
            box.shape.draw(body, box, self.color, screen)

    def get_color(self):
        return self.color


class FallingIshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        super().__init__(color, space, x, y, cell_width * 2)

    def box2d_init(self):
        self.bodies = []

        x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM + self.width / PPM / 2
        body1 = self.space.CreateDynamicBody(position=(x1, y1), angle=0)
        box1 = body1.CreatePolygonFixture(box=(self.width / PPM / 2, self.width / PPM / 2), density=1, friction=1)
        self.bodies.append((body1, box1))

        x2, y2 = x1 * 3, y1 + self.width / PPM / 2
        body2 = self.space.CreateDynamicBody(position=(x1, y1), angle=0)
        box2 = body2.CreatePolygonFixture(box=(self.width / PPM / 2 * 3, self.width / PPM / 2), density=1, friction=1)
        self.bodies.append((body2, box2))


class FallingJshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        super().__init__(color, space, x, y, cell_width)

    def box2d_init(self):
        self.bodies = []

        x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM + self.width / PPM / 2
        body1 = self.space.CreateDynamicBody(position=(x1, y1), angle=0)
        box1 = body1.CreatePolygonFixture(box=(self.width / PPM / 2, self.width / PPM / 2), density=1, friction=1)
        self.bodies.append((body1, box1))

        x2, y2 = self.x / PPM + self.width / PPM * 1.5, y1 - self.width / PPM
        body2 = self.space.CreateDynamicBody(position=(x2, y2), angle=0)
        box2 = body2.CreatePolygonFixture(box=(self.width / PPM / 2 * 3, self.width / PPM / 2), density=1, friction=1)
        self.bodies.append((body2, box2))
        # joint = self.space.CreateWeldJoint(bodyA=body1, bodyB=body2, localAnchorA=(0, -self.width / PPM / 2),
        #                                    localAnchorB=(-self.width / PPM, self.width / PPM / 2))


class FallingLshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        super().__init__(color, space, x, y, cell_width * 2)


class FallingOshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        super().__init__(color, space, x, y, cell_width * 2)

    def box2d_init(self):
        self.bodies = []

        x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM + self.width / PPM / 2
        body1 = self.space.CreateDynamicBody(position=(x1, y1), angle=0)
        box1 = body1.CreatePolygonFixture(box=(self.width / PPM / 2, self.width / PPM / 2), density=1, friction=1)
        self.bodies.append((body1, box1))


class FallingSshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        super().__init__(color, space, x, y, cell_width * 2)


class FallingTshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        super().__init__(color, space, x, y, cell_width * 2)


class FallingZshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        super().__init__(color, space, x, y, cell_width * 2)