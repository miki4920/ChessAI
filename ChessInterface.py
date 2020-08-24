import pyglet
from pyglet import shapes
from ChessBoard import ChessBoard
from pyglet.gl import *
from pyglet.window import mouse


class Interface(pyglet.window.Window):
    def __init__(self):
        width, height = self.get_resolution()
        self.resolution = int(height * 0.93)
        self.square_size = int(self.resolution / 8)
        super(Interface, self).__init__(width=self.resolution, height=self.resolution)
        super(Interface, self).set_location(int((width - self.resolution) / 2), int(height * 0.03))
        self.chess_squares = [None] * 64
        self.chess_board = ChessBoard().chess_board
        self.draw_chessboard()
        self.current_piece = None
        self.original_position = None

    @staticmethod
    def get_resolution():
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        return screen.width, screen.height

    def rescale_image(self, piece_image):
        piece_image = pyglet.resource.image(f"Textures/{piece_image}.png")
        piece_image.width = self.square_size
        piece_image.height = self.square_size
        piece_image = pyglet.sprite.Sprite(piece_image)
        return piece_image

    def draw_chessboard(self):
        for column in range(0, 8):
            for row in range(0, 8):
                self.chess_squares[column * 8 + row] = shapes.Rectangle(x=row * self.square_size,
                                                                        y=column * self.square_size,
                                                                        width=self.square_size,
                                                                        height=self.square_size,
                                                                        color=(193, 154, 107)
                                                                        if (column + row) % 2 == 0 else (255, 255, 255))
                if self.chess_board[column][row]:
                    image = self.rescale_image(self.chess_board[column][row])
                    image.position = (row * self.square_size, column * self.square_size)
                    self.chess_board[column][row] = image

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
        x_modulus = x // self.square_size
        y_modulus = y // self.square_size
        if buttons and mouse.LEFT and not self.current_piece:
            self.current_piece = self.chess_board[y_modulus][x_modulus]
            self.chess_board[y_modulus][x_modulus] = None
            self.original_position = x_modulus, y_modulus
        elif buttons and mouse.LEFT and self.current_piece:
            self.current_piece.position = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.current_piece:
            x_modulus = x // self.square_size
            y_modulus = y // self.square_size

            if not self.chess_board[y_modulus][x_modulus]:
                self.current_piece.position = (x_modulus * self.square_size, y_modulus * self.square_size)
                self.chess_board[y_modulus][x_modulus] = self.current_piece
            else:
                self.chess_board[self.original_position[1]][self.original_position[0]] = self.current_piece
                self.current_piece.position = self.original_position[0] * self.square_size, self.original_position[
                    1] * self.square_size
            self.current_piece = None


window = Interface()
window.config.alpha_size = 8
pyglet.app.run()
