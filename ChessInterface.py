import pyglet
from ChessBoard import ChessBoard
from pyglet.gl import *
from pyglet.window import mouse
from UtilityFunctions import SizeConverter
from MoveValidation import ValidateMove
from ChessObjects import create_dot
from ChessAI import ChessAI

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
        self.ai = ChessAI()
        super(Interface, self).__init__(width=self.resolution, height=self.resolution)
        super(Interface, self).set_location(center[0], center[1])
        self.chess_squares = [None] * 64
        self.chess_board = ChessBoard(self.square_size)
        self.draw_chessboard()
        self.current_piece = None
        self.win = False

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
                    piece.set_position((row, column))
                    self.chess_board.set_tile((row, column), piece)

    def on_draw(self):
        window.clear()
        [square.draw() for square in self.chess_squares]
        if self.current_piece:
            valid_moves = self.validator.validate_moves(self.current_piece, self.chess_board)
            valid_moves = [list(move.values())[0] for move in valid_moves]
            [create_dot(self.converter.stp(coordinates), self.square_size).draw() for coordinates in valid_moves]
            self.current_piece.draw()
        self.chess_board.draw()

    def on_mouse_press(self, x, y, buttons, modifiers):
        destination = self.converter.pts((x, y))
        piece = self.chess_board.get_tile(destination)
        if piece and not self.current_piece and mouse.LEFT and not self.win:
            self.select_piece(piece, destination)
        elif self.current_piece:
            self.move_piece(self.current_piece, destination)
            self.current_piece = None

    def select_piece(self, piece, move):
        if self.validator.colour == piece.colour:
            self.current_piece = piece
            self.chess_board.set_tile(move, None)

    def move_piece(self, piece, destination):
        task = self.validator.validate_move(piece, self.chess_board, destination, False)
        if task:
            self.chess_board.accept_move(task, piece)
            self.current_piece.set_position(destination)
            self.validator.colour = not self.validator.colour
        else:
            self.chess_board.set_tile(piece.original_position, piece)


window = Interface()
window.config.alpha_size = 8
pyglet.app.run()
