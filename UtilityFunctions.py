from collections.abc import Iterable


class SizeConverter(object):
    def __init__(self, size):
        self.size = size

    @staticmethod
    def iterable(obj):
        return isinstance(obj, Iterable)

    def stp(self, value):
        if self.iterable(value):
            return tuple(map(lambda i: i * self.size, value))
        return value * self.size

    def pts(self, value):
        if self.iterable(value):
            return tuple(map(lambda i: i // self.size, value))
        return value // self.size


def bresenham(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x * xx + y * yx, y0 + x * xy + y * yy
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy


def delta_distance(move, piece):
    dx = move[0] - piece[0]
    dy = move[1] - piece[1]
    return dx, dy
