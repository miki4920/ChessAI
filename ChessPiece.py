import pyglet


class Piece(object):
    def __init__(self, name, colour, size):
        self.name = name
        self.colour = colour
        self.size = size
        self.sprite = self.get_image()
        self.original_position = self.sprite.position

    def get_image(self):
        piece_image = pyglet.resource.image(f"Textures/{self.name + '_' + self.colour}.png")
        piece_image.width = self.size
        piece_image.height = self.size
        piece_image = pyglet.sprite.Sprite(piece_image)
        return piece_image

    def center(self):
        self.sprite.image.anchor_x = self.sprite.image.width // 2
        self.sprite.image.anchor_y = self.sprite.image.height // 2

    def decenter(self):
        self.sprite.image.anchor_x = 0
        self.sprite.image.anchor_y = 0

    def set_position(self, position):
        self.original_position = position
        self.sprite.position = position

    def draw(self):
        self.sprite.draw()
