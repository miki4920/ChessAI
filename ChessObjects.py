import pyglet
from UtilityFunctions import SizeConverter


def get_image(path):
    image = pyglet.resource.image(path)
    image = pyglet.sprite.Sprite(image)
    return image


def adjust_size(sprite, size):
    sprite.image.width = size
    sprite.image.height = size
    return sprite


class Piece(object):
    def __init__(self, name, colour, size):
        self.name = name
        self.colour = colour
        self.size = size
        self.converter = SizeConverter(size)
        self.sprite = adjust_size(get_image(f"Textures/{self.name + '_' + ('w' if self.colour else 'b')}.png"), size)
        self.original_position = None
        self.previous_position = None

    def set_position(self, position):
        if self.original_position is not None:
            self.previous_position = self.original_position
        self.original_position = position
        self.sprite.position = self.converter.stp(position)

    def draw(self):
        self.sprite.draw()


def create_dot(coordinates, size):
    sprite = get_image(f"Textures/dot.png")
    sprite = adjust_size(sprite, size * 0.4)
    sprite.image.anchor_x = sprite.image.width // 2
    sprite.image.anchor_y = sprite.image.height // 2
    sprite.position = coordinates[0] + size // 2, coordinates[1] + size // 2
    return sprite
