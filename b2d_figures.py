import pygame

from assets import PPM, WINDOW_WIDTH, WINDOW_HEIGHT, RGB_COLORS
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody, weldJoint


def to_radians(angle):
    return angle * 3.14 / 180


def my_draw_polygon(polygon, body, fixture, color, screen):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], WINDOW_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, color, vertices)


polygonShape.draw = my_draw_polygon


class FallingFigure:
    def __init__(self, color, space,  x, y, width):
        self.color = RGB_COLORS[color]
        self.space = space
        self.width = width
        self.x, self.y = x, y

        self.box2d_init()

    def box2d_init(self, x1, y1, width1, height1, x2, y2, width2, height2, anchor_a, anchor_b, rect=False):
        self.bodies = []

        body1 = self.space.CreateDynamicBody(position=(x1, y1), angle=0)
        box1 = body1.CreatePolygonFixture(box=(width1, height1), density=1, friction=1)
        self.bodies.append((body1, box1))

        if not rect:
            body2 = self.space.CreateDynamicBody(position=(x2, y2), angle=0)
            box2 = body2.CreatePolygonFixture(box=(width2, height2), density=1, friction=1)
            self.bodies.append((body2, box2))

            joint = self.space.CreateWeldJoint(bodyA=body1, bodyB=body2, localAnchorA=anchor_a,
                                               localAnchorB=anchor_b)

    def render(self, screen):
        for body, box in self.bodies:
            box.shape.draw(body, box, self.color, screen)

    def get_y_coord(self):
        list_of_vertices = []
        for body, box in self.bodies:
            vertices = [(body.transform * v) * PPM for v in box.shape.vertices]
            vertices = [(v[0], WINDOW_HEIGHT - v[1]) for v in vertices]
            list_of_vertices.append(vertices)

        y_coords = []
        for figure_piece in list_of_vertices:
            for x_y in figure_piece:
                y_coords.append(x_y[1])
        return min(y_coords)


class FallingIshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        self.count_rotates = count_rotates % 2
        super().__init__(color, space, x, y, cell_width)

    def box2d_init(self):
        if self.count_rotates == 0:
            x1, y1 = self.x / PPM + self.width / PPM * 2, (600 - self.y) / PPM - self.width / PPM / 2
            width1, height1 = self.width / PPM * 2, self.width / PPM / 2
        elif self.count_rotates == 1:
            x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM - self.width / PPM * 2
            width1, height1 = self.width / PPM / 2, self.width / PPM * 2

        x2, y2 = -1, -1
        width2, height2 = -1, -1
        anchor_a, anchor_b = -1, -1

        super().box2d_init(x1, y1, width1, height1, x2, y2, width2, height2, anchor_a, anchor_b, rect=True)


class FallingJshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        self.count_rotates = count_rotates % 4
        super().__init__(color, space, x, y, cell_width)

    def box2d_init(self):
        if self.count_rotates == 0:
            x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM - self.width / PPM / 2
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 + self.width / PPM, y1 - self.width / PPM
            width2, height2 = self.width / PPM / 2 * 3, self.width / PPM / 2
            anchor_a, anchor_b = (0, -self.width / PPM / 2), (-self.width / PPM, self.width / PPM / 2)

        elif self.count_rotates == 1:
            x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM - self.width / PPM * 2.5
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 + self.width / PPM, y1 + self.width / PPM
            width2, height2 = self.width / PPM / 2, self.width / PPM / 2 * 3
            anchor_a, anchor_b = (self.width / PPM / 2, 0), (-self.width / PPM / 2, -self.width / PPM)

        elif self.count_rotates == 2:
            x1, y1 = self.x / PPM + self.width / PPM * 2.5, (600 - self.y) / PPM - self.width / PPM * 1.5
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 - self.width / PPM, y1 + self.width / PPM
            width2, height2 = self.width / PPM / 2 * 3, self.width / PPM / 2
            anchor_a, anchor_b = (0, self.width / PPM / 2), (self.width / PPM, -self.width / PPM / 2)

        elif self.count_rotates == 3:
            x1, y1 = self.x / PPM + self.width / PPM * 1.5, (600 - self.y) / PPM - self.width / PPM / 2
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 - self.width / PPM, y1 - self.width / PPM
            width2, height2 = self.width / PPM / 2, self.width / PPM / 2 * 3
            anchor_a, anchor_b = (-self.width / PPM / 2, 0), (self.width / PPM / 2, self.width / PPM)

        super().box2d_init(x1, y1, width1, height1, x2, y2, width2, height2, anchor_a, anchor_b)


class FallingLshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        self.count_rotates = count_rotates % 4
        super().__init__(color, space, x, y, cell_width)

    def box2d_init(self):
        if self.count_rotates == 0:
            x1, y1 = self.x / PPM + self.width / PPM * 2.5, (600 - self.y) / PPM - self.width / PPM / 2
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 - self.width / PPM, y1 - self.width / PPM
            width2, height2 = self.width / PPM / 2 * 3, self.width / PPM / 2
            anchor_a, anchor_b = (0, -self.width / PPM / 2), (self.width / PPM, self.width / PPM / 2)

        elif self.count_rotates == 1:
            x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM - self.width / PPM / 2
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 + self.width / PPM, y1 - self.width / PPM
            width2, height2 = self.width / PPM / 2, self.width / PPM / 2 * 3
            anchor_a, anchor_b = (self.width / PPM / 2, 0), (-self.width / PPM / 2, self.width / PPM)

        elif self.count_rotates == 2:
            x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM - self.width / PPM * 1.5
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 + self.width / PPM, y1 + self.width / PPM
            width2, height2 = self.width / PPM / 2 * 3, self.width / PPM / 2
            anchor_a, anchor_b = (0, self.width / PPM / 2), (-self.width / PPM, -self.width / PPM / 2)

        elif self.count_rotates == 3:
            x1, y1 = self.x / PPM + self.width / PPM * 1.5, (600 - self.y) / PPM - self.width / PPM * 2.5
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 - self.width / PPM, y1 + self.width / PPM
            width2, height2 = self.width / PPM / 2, self.width / PPM / 2 * 3
            anchor_a, anchor_b = (-self.width / PPM / 2, 0), (self.width / PPM / 2, -self.width / PPM)

        super().box2d_init(x1, y1, width1, height1, x2, y2, width2, height2, anchor_a, anchor_b)


class FallingOshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        super().__init__(color, space, x, y, cell_width * 2)

    def box2d_init(self):
        x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM - self.width / PPM / 2
        width1, height1 = self.width / PPM / 2, self.width / PPM / 2
        x2, y2 = -1, -1
        width2, height2 = -1, -1
        anchor_a, anchor_b = -1, -1

        super().box2d_init(x1, y1, width1, height1, x2, y2, width2, height2, anchor_a, anchor_b, rect=True)


class FallingSshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        self.count_rotates = count_rotates % 2
        super().__init__(color, space, x, y, cell_width)

    def box2d_init(self):
        if self.count_rotates == 0:
            x1, y1 = self.x / PPM + self.width / PPM, (600 - self.y) / PPM - self.width / PPM * 1.5
            width1, height1 = self.width / PPM, self.width / PPM / 2
            x2, y2 = x1 + self.width / PPM, y1 + self.width / PPM
            width2, height2 = self.width / PPM, self.width / PPM / 2
            anchor_a, anchor_b = ((-self.width / PPM / 2, -self.width / PPM / 2),
                                  (self.width / PPM / 2, self.width / PPM / 2))

        elif self.count_rotates == 1:
            x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM - self.width / PPM
            width1, height1 = self.width / PPM / 2, self.width / PPM
            x2, y2 = x1 + self.width / PPM, y1 - self.width / PPM
            width2, height2 = self.width / PPM / 2, self.width / PPM
            anchor_a, anchor_b = ((self.width / PPM / 2, -self.width / PPM / 2),
                                  (-self.width / PPM / 2, self.width / PPM / 2))

        super().box2d_init(x1, y1, width1, height1, x2, y2, width2, height2, anchor_a, anchor_b)


class FallingTshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        self.count_rotates = count_rotates % 4
        super().__init__(color, space, x, y, cell_width)

    def box2d_init(self):
        if self.count_rotates == 0:
            x1, y1 = self.x / PPM + self.width / PPM * 1.5, (600 - self.y) / PPM - self.width / PPM / 2
            width1, height1 = self.width / PPM / 2 * 3, self.width / PPM / 2
            x2, y2 = x1, y1 - self.width / PPM
            width2, height2 = self.width / PPM / 2, self.width / PPM / 2
            anchor_a, anchor_b = (0, -self.width / PPM / 2), (0, self.width / PPM / 2)

        elif self.count_rotates == 1:
            x1, y1 = self.x / PPM + self.width / PPM * 1.5, (600 - self.y) / PPM - self.width / PPM * 1.5
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 - self.width / PPM, y1
            width2, height2 = self.width / PPM / 2, self.width / PPM / 2 * 3
            anchor_a, anchor_b = (-self.width / PPM / 2, 0), (self.width / PPM / 2, 0)

        elif self.count_rotates == 2:
            x1, y1 = self.x / PPM + self.width / PPM * 1.5, (600 - self.y) / PPM - self.width / PPM / 2
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1, y1 - self.width / PPM
            width2, height2 = self.width / PPM / 2 * 3, self.width / PPM / 2
            anchor_a, anchor_b = (0, -self.width / PPM / 2), (0, self.width / PPM / 2)

        elif self.count_rotates == 3:
            x1, y1 = self.x / PPM + self.width / PPM / 2, (600 - self.y) / PPM - self.width / PPM * 1.5
            width1, height1 = self.width / PPM / 2, self.width / PPM / 2
            x2, y2 = x1 + self.width / PPM, y1
            width2, height2 = self.width / PPM / 2, self.width / PPM / 2 * 3
            anchor_a, anchor_b = (self.width / PPM / 2, 0), (-self.width / PPM / 2, 0)

        super().box2d_init(x1, y1, width1, height1, x2, y2, width2, height2, anchor_a, anchor_b)


class FallingZshaped(FallingFigure):
    def __init__(self, color, space, x, y, cell_width, count_rotates):
        self.count_rotates = count_rotates % 2
        super().__init__(color, space, x, y, cell_width)

    def box2d_init(self):
        if self.count_rotates == 0:
            x1, y1 = self.x / PPM + self.width / PPM, (600 - self.y) / PPM - self.width / PPM / 2
            width1, height1 = self.width / PPM, self.width / PPM / 2
            x2, y2 = x1 + self.width / PPM, y1 - self.width / PPM
            width2, height2 = self.width / PPM, self.width / PPM / 2
            anchor_a, anchor_b = ((self.width / PPM / 2, -self.width / PPM / 2),
                                  (-self.width / PPM / 2, self.width / PPM / 2))

        elif self.count_rotates == 1:
            x1, y1 = self.x / PPM + self.width / PPM * 1.5, (600 - self.y) / PPM - self.width / PPM
            width1, height1 = self.width / PPM / 2, self.width / PPM
            x2, y2 = x1 - self.width / PPM, y1 - self.width / PPM
            width2, height2 = self.width / PPM / 2, self.width / PPM
            anchor_a, anchor_b = ((-self.width / PPM / 2, -self.width / PPM / 2),
                                  (self.width / PPM / 2, self.width / PPM / 2))

        super().box2d_init(x1, y1, width1, height1, x2, y2, width2, height2, anchor_a, anchor_b)
