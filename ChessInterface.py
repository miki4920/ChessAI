import pyglet
from pyglet import shapes
from ChessBoard import ChessBoard
from pyglet.gl import *
from pyglet.window import mouse
from UtilityFunctions import SizeConverter


class Interface(pyglet.window.Window):
    def __init__(self):
        # TODO Simplify interface, put more elements into "get_resolution"
        width, height = self.get_resolution()
        self.resolution = int(height * 0.93)
        self.square_size = int(self.resolution / 8)
        self.converter = SizeConverter(self.square_size)
        super(Interface, self).__init__(width=self.resolution, height=self.resolution)
        super(Interface, self).set_location(int((width - self.resolution) / 2), int(height * 0.03))
        self.chess_squares = [None] * 64
        self.chess_board = ChessBoard(self.square_size).get_initial_chessboard()
        self.draw_chessboard()
        self.current_piece = None

    @staticmethod
    def get_resolution():
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        return screen.width, screen.height

    # TODO Implement a chess class
    def draw_chessboard(self):
        for column in range(0, 8):
            for row in range(0, 8):
                self.chess_squares[column * 8 + row] = shapes.Rectangle(x=self.converter.stp(row),
                                                                        y=self.converter.stp(column),
                                                                        width=self.square_size,
                                                                        height=self.square_size,
                                                                        color=(193, 154, 107)
                                                                        if (column + row) % 2 == 0 else (255, 255, 255))
                if self.chess_board[column][row]:
                    self.chess_board[column][row].set_position((self.converter.stp((row, column))))

    def on_draw(self):
        window.clear()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        [square.draw() for square in self.chess_squares]
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        [piece.draw() for piece in sum(self.chess_board, []) if piece]
        if self.current_piece:
            self.current_piece.draw()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        x_modulus, y_modulus = self.converter.pts((x, y))
        if buttons and mouse.LEFT and not self.current_piece:
            self.current_piece = self.chess_board[y_modulus][x_modulus]
            if self.current_piece:
                self.current_piece.center()
                self.chess_board[y_modulus][x_modulus] = None
                self.current_piece.original_position = (x_modulus, y_modulus)
        elif buttons and mouse.LEFT and self.current_piece:
            self.current_piece.sprite.position = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.current_piece:
            x_modulus, y_modulus = self.converter.pts((x, y))
            # TODO Move rescaling into separate function
            self.current_piece.decenter()
            if not self.chess_board[y_modulus][x_modulus]:
                self.current_piece.set_position((self.converter.stp(x_modulus), self.converter.stp(y_modulus)))
                self.chess_board[y_modulus][x_modulus] = self.current_piece
            else:
                self.chess_board[self.current_piece.original_position[1]][
                    self.current_piece.original_position[0]] = self.current_piece
                self.current_piece.set_position(self.converter.stp(self.current_piece.original_position))
            self.current_piece = None


window = Interface()
window.config.alpha_size = 8
pyglet.app.run()
