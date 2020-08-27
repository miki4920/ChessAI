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
