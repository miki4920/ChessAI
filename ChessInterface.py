import pyglet
from ChessBoard import ChessBoard
from pyglet.gl import *
from pyglet.window import mouse
from UtilityFunctions import SizeConverter
from MoveValidation import ValidateMove
from ChessObjects import create_dot


class Interface(pyglet.window.Window):
    def __init__(self):
        self.resolution, center = self.get_resolution()
        self.square_size = int(self.resolution / 8)
        self.converter = SizeConverter(self.square_size)
        self.validator = ValidateMove()
        super(Interface, self).__init__(width=self.resolution, height=self.resolution)
        super(Interface, self).set_location(center[0], center[1])
        self.chess_squares = [None] * 64
        self.chess_board = ChessBoard(self.square_size).get_initial_chessboard()
        self.draw_chessboard()
        self.current_piece = None

    @staticmethod
    def get_resolution():
        display = pyglet.canvas.get_display()
        screen = display.get_default_screen()
        width, height = screen.width, screen.height
        resolution = int(height * 0.93)
        center = int((width - resolution) / 2), int(height * 0.03)
        return resolution, center

    def draw_chessboard(self):
        for column in range(0, 8):
            for row in range(0, 8):
                self.chess_squares[column * 8 + row] = pyglet.shapes.Rectangle(x=self.converter.stp(row),
                                                                               y=self.converter.stp(column),
                                                                               width=self.square_size,
                                                                               height=self.square_size,
                                                                               color=(118, 150, 86)
                                                                               if (column + row) % 2 == 0 else (
                                                                               255, 255, 255))
                if self.chess_board[column][row]:
                    self.chess_board[column][row].set_position((self.converter.stp((row, column))))
                    self.chess_board[column][row].previous_position = None

    def on_draw(self):
        window.clear()
        [square.draw() for square in self.chess_squares]
        if self.current_piece:
            valid_moves = self.validator.validate_moves(self.current_piece, self.chess_board)
            [create_dot(self.converter.stp(coordinates), self.square_size).draw() for coordinates in valid_moves]
            self.current_piece.draw()
            [piece.draw() for piece in sum(self.chess_board, []) if piece]

        else:
            [piece.draw() for piece in sum(self.chess_board, []) if piece]

    def on_mouse_press(self, x, y, buttons, modifiers):
        move = self.converter.pts((x, y))
        piece = self.chess_board[move[1]][move[0]]
        if piece and not self.current_piece:
            if mouse.LEFT and self.validator.validate_pick(piece):
                self.current_piece = piece
                self.chess_board[move[1]][move[0]] = None
                self.current_piece.original_position = (move[0], move[1])
        elif self.current_piece:
            if self.validator.validate_move(self.current_piece, self.chess_board, move):
                self.current_piece.set_position((self.converter.stp(move[0]), self.converter.stp(move[1])))
                self.chess_board[move[1]][move[0]] = self.current_piece
                self.validator.colour = not self.validator.colour
            else:
                self.chess_board[self.current_piece.original_position[1]][
                    self.current_piece.original_position[0]] = self.current_piece
            self.current_piece = None


window = Interface()
window.config.alpha_size = 8
pyglet.app.run()
