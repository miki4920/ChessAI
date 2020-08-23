import pyglet
from pyglet import shapes


class Interface(pyglet.window.Window):
    def __init__(self):
        width, height = self.get_resolution()
        self.resolution = int(height * 0.93)
        super(Interface, self).__init__(width=self.resolution, height=self.resolution)
        super(Interface, self).set_location(int((width - self.resolution) / 2), 0)
        self.BOARD_SIZE = 8
        self.chess_board = self.draw_chessboard()

    @staticmethod
    def get_resolution():
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        return screen.width, screen.height

    def draw_chessboard(self):
        square_size = self.resolution / self.BOARD_SIZE
        chess_board = []
        for column in range(0, 8):
            for row in range(0, 8):
                chess_board.append(
                    shapes.Rectangle(x=row * square_size, y=column * square_size, width=square_size, height=square_size,
                                     color=(0, 0, 0) if (column + row) % 2 == 0 else (255, 255, 255)))
        return chess_board

    def on_draw(self):
        [square.draw() for square in self.chess_board]


window = Interface()
pyglet.app.run()
