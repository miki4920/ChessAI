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
        self.chess_board_pieces = ChessBoard().chess_board
        self.current_piece = None
        self.current_position = None

    @staticmethod
    def get_resolution():
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        return screen.width, screen.height

    @staticmethod
    def rescale_image(square_size, piece_image):
        piece_image = pyglet.resource.image(f"Textures/{piece_image}.png")
        piece_image.width = square_size
        piece_image.height = square_size
        return piece_image

    def draw_chessboard(self):
        chess_board = []
        chess_pieces = []
        for column in range(0, 8):
            for row in range(0, 8):
                chess_board.append(
                    shapes.Rectangle(x=row * self.square_size, y=column * self.square_size, width=self.square_size,
                                     height=self.square_size,
                                     color=(193, 154, 107) if (column + row) % 2 == 0 else (255, 255, 255)))
                if self.chess_board_pieces[column][row]:
                    image = self.rescale_image(self.square_size, self.chess_board_pieces[column][row])
                    chess_pieces.append((image, [row * self.square_size, column * self.square_size]))
        return chess_board, chess_pieces

    def on_draw(self):
        chess_board, chess_pieces_drawing = self.draw_chessboard()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        [square.draw() for square in chess_board]
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        [piece[0].blit(piece[1][0], piece[1][1]) for piece in chess_pieces_drawing]
        if self.current_piece:
            image = self.rescale_image(self.square_size, self.current_piece)
            image.blit(self.current_position[1] * self.square_size, self.current_position[0] * self.square_size)
            self.chess_board_pieces[self.current_position[1]][self.current_position[0]] = self.current_piece

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        x = x // self.square_size
        y = y // self.square_size
        if buttons and mouse.LEFT:
            self.current_piece = self.chess_board_pieces[x][y]
            self.current_position = (x, y)
            self.chess_board_pieces[x][y] = None


window = Interface()
window.config.alpha_size = 8
pyglet.app.run()
