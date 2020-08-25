import pyglet


class Piece(object):
    def __init__(self, name, colour, image):
        self.name = name
        self.colour = colour
        self.sprite = pyglet.sprite.Sprite(image)

    @staticmethod
    def return_legal_moves():
        legal_moves = None
        return legal_moves
