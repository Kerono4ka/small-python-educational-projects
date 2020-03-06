import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def __sub__(self, point):
        return Vec2d((self.x - point.x, self.y - point.y))

    def __add__(self, point):
        return Vec2d((self.x + point.x, self.y + point.y))

    def __mul__(self, k):
        if isinstance(k, Vec2d):
            return self.x * k.x, self.y * k.y
        return Vec2d((self.x * k, self.y * k))

    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, pos):
        self.points.append(pos)
        self.speeds.append(Vec2d((random.random() * 2, random.random() * 2)))

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, self.points[p_n].int_pair(),
                                 self.points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in self.points:
                pygame.draw.circle(gameDisplay, color, p.int_pair(), width)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d((-self.speeds[p].x, self.speeds[p].y))
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d((self.speeds[p].x, -self.speeds[p].y))


class Knot(Polyline):
    def __init__(self, steps=35):
        self.steps = steps

    def add_point(self, steps=35, points=None):
        self.steps = steps
        self.points = self.get_knot(points)

    def set_points(self, steps=35, points=None):
        self.steps = steps
        self.points = self.get_knot(points)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, points):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn))
        return res


class Helper:
    def __init__(self, steps):
        self.data = [
            ["F1", "Show Help"],
            ["R", "Restart"],
            ["P", "Pause/Play"],
            ["Num+", "More points"],
            ["Num-", "Less points"],
            ["", ""],
            [str(steps), "Current points"]
        ]

    def draw_help(self):
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [      # Ð·Ð°Ð¼ÐºÐ½ÑƒÑ‚Ð°Ñ Ð»Ð¸Ð½Ð¸Ñ Ð²Ð¾ÐºÑ€ÑƒÐ³ Ð¾ÐºÐ½Ð° Ð¿Ð¾Ð¼Ð¾Ñ‰Ð¸
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(self.data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("Blabla")

    steps = 35
    polyline = Polyline()
    knot = Knot()
    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline.__init__()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_RIGHT:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_LEFT:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.add_point(Vec2d(event.pos))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        knot.add_point(steps, polyline.points)
        knot.draw_points("line", 3, color)

        if not pause:
            polyline.set_points()
        if show_help:
            help_window = Helper(steps)
            help_window.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)