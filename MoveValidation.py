from bresenham import bresenham


class ValidateMove(object):
    def __init__(self):
        self.board_bounds = (0, 7)
        self.colour = True
        self.piece = None
        self.move = None
        self.chess_board = None
        self.tile = None

    def validate_pick(self, piece):
        if piece:
            return self.colour == piece.colour

    def return_change(self):
        dx = self.move[0] - self.piece.original_position[0]
        dy = self.move[1] - self.piece.original_position[1]
        return dx, dy

    def return_bresenham(self):
        return list(
            bresenham(self.piece.original_position[0], self.piece.original_position[1], self.move[0], self.move[1]))[
               1:-1]

    def validate_path(self):
        if self.tile is None or self.tile.colour != self.piece.colour:
            if all([self.chess_board.get_tile(coordinate) is None for coordinate in self.return_bresenham()]):
                return True
        return False

    def pawn(self):
        dx, dy = self.return_change()
        colour = 1 if self.piece.colour else -1
        if abs(dx) == 1 and colour * dy == 1 and self.tile is not None and self.tile.colour != self.piece.colour:
            return True
        elif self.piece.previous_position and dy * colour == 1 and dx == 0 and self.tile is None:
            return True
        elif 1 <= dy * colour <= 2 and dx == 0 and self.validate_path() and not self.piece.previous_position:
            return True
        return False

    def castle(self):
        dx, dy = self.return_change()
        if dx != 0 and dy == 0 or dx == 0 and dy != 0:
            return self.validate_path()
        return False

    def knight(self):
        dx, dy = self.return_change()
        dx = abs(dx)
        dy = abs(dy)
        return dx == 2 and dy == 1 or dx == 1 and dy == 2

    def bishop(self):
        dx, dy = self.return_change()
        dx = abs(dx)
        dy = abs(dy)
        if dx == dy and dx != 0:
            return self.validate_path()
        return False

    def queen(self):
        return self.bishop() or self.castle()

    def king(self):
        dx, dy = self.return_change()
        dx = abs(dx)
        dy = abs(dy)
        return dx < 2 and dy < 2

    def valid_piece_move(self):
        function_dictionary = {"pawn": self.pawn,
                               "castle": self.castle,
                               "knight": self.knight,
                               "bishop": self.bishop,
                               "queen": self.queen,
                               "king": self.king}
        if (self.tile is None or self.tile.colour != self.piece.colour) and function_dictionary[self.piece.name]():
            return True
        return False

    def validate_move(self, piece, chess_board, move):
        self.piece = piece
        self.move = move
        self.chess_board = chess_board
        self.tile = self.chess_board.get_tile(self.move)
        if self.valid_piece_move():
            return True
        return False

    def validate_moves(self, piece, chess_board):
        moves = [move for move in chess_board.get_all_moves() if self.validate_move(piece, chess_board, move)]
        return moves

    def validate_check(self, chess_board):
        pieces = chess_board.get_all_pieces_colour(not self.colour)
        moves = []
        for piece in pieces:
            print(piece.original_position)
