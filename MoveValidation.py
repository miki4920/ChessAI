from bresenham import bresenham


class ValidateMove(object):
    def __init__(self):
        self.board_bounds = (0, 7)
        self.colour = True
        self.piece = None
        self.move = None
        self.moves = []
        self.chess_board = None
        self.tile = None

    @staticmethod
    def get_all_moves():
        moves = []
        for y in range(0, 8):
            for x in range(0, 8):
                moves.append([x, y])
        return moves

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
            if all([self.chess_board[coordinate[1]][coordinate[0]] is None for coordinate in self.return_bresenham()]):
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

    def validate_moves(self, piece, chess_board):
        self.moves = [move for move in self.get_all_moves() if self.validate_move(piece, chess_board, move)]
        return self.moves

    def validate_move(self, piece, chess_board, move):
        self.piece = piece
        self.move = move
        self.chess_board = chess_board
        self.tile = self.chess_board[self.move[1]][self.move[0]]
        if self.colour == self.piece.colour:
            if self.valid_piece_move():
                return True
        return False
