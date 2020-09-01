import pyglet
from ChessBoard import ChessBoard
from pyglet.gl import *
from pyglet.window import mouse
from UtilityFunctions import SizeConverter
from MoveValidation import ValidateMove
from ChessObjects import create_dot

COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (118, 150, 86)
RESOLUTION_OFFSET = 0.93
BAR_OFFSET = 0.03


class Interface(pyglet.window.Window):
    def __init__(self):
        self.resolution, center = self.get_resolution()
        self.square_size = int(self.resolution / 8)
        self.converter = SizeConverter(self.square_size)
        self.validator = ValidateMove()
        super(Interface, self).__init__(width=self.resolution, height=self.resolution)
        super(Interface, self).set_location(center[0], center[1])
        self.chess_squares = [None] * 64
        self.chess_board = ChessBoard(self.square_size)
        self.draw_chessboard()
        self.current_piece = None

    @staticmethod
    def get_resolution():
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        width, height = screen.width, screen.height
        resolution = int(height * RESOLUTION_OFFSET)
        center = int((width - resolution) / 2), int(height * BAR_OFFSET)
        return resolution, center

    def draw_chessboard(self):
        for column in range(0, 8):
            for row in range(0, 8):
                self.chess_squares[column * 8 + row] = pyglet.shapes.Rectangle(x=self.converter.stp(row),
                                                                               y=self.converter.stp(column),
                                                                               width=self.square_size,
                                                                               height=self.square_size,
                                                                               color=COLOUR_BLACK
                                                                               if (column + row) % 2 == 0 else
                                                                               COLOUR_WHITE)
                if self.chess_board.get_tile((row, column)):
                    piece = self.chess_board.get_tile((row, column))
                    piece.set_position((self.converter.stp((row, column))))
                    piece.previous_position = None
                    self.chess_board.set_tile((row, column), piece)

    def on_draw(self):
        window.clear()
        [square.draw() for square in self.chess_squares]
        if self.current_piece:
            # TODO Create a way to check for check
            valid_moves = self.validator.validate_moves(self.current_piece, self.chess_board)
            [create_dot(self.converter.stp(coordinates), self.square_size).draw() for coordinates in valid_moves]
            self.current_piece.draw()
        self.chess_board.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        move = self.converter.pts((x, y))
        piece = self.chess_board.get_tile(move)
        if piece and not self.current_piece:
            if mouse.LEFT and self.validator.validate_pick(piece):
                self.current_piece = piece
                self.current_piece.original_position = move
                self.chess_board.set_tile(move, None)
        elif self.current_piece:
            if self.validator.validate_move(self.current_piece, self.chess_board, move):
                self.current_piece.set_position((self.converter.stp(move[0]), self.converter.stp(move[1])))
                self.chess_board.set_tile(move, self.current_piece)
                self.validator.colour = not self.validator.colour
            else:
                self.chess_board.set_tile(self.current_piece.original_position, self.current_piece)
            self.current_piece = None


window = Interface()
window.config.alpha_size = 8
pyglet.app.run()
