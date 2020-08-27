class ValidateMove(object):
    def __init__(self):
        self.board_bounds = (0, 7)
        self.piece = None
        self.move = None
        self.chess_board = None

    def in_bounds(self):
        return self.board_bounds[0] <= self.move[0] <= self.board_bounds[1] and self.board_bounds[0] <= self.move[
            1] <= self.board_bounds[1]

    def return_change(self):
        dx = self.move[0] - self.piece.original_position[0]
        dy = self.move[1] - self.piece.original_position[1]
        return dx, dy

    def pawn(self):
        tile = self.chess_board[self.move[1]][self.move[0]]
        colour = 1 if self.piece.colour == "w" else -1
        dx, dy = self.return_change()
        return 0 < dy * colour <= 2 and dx == 0 or abs(
            dx) == 1 and dy * colour == 1 and tile is not None and tile.colour != self.piece.colour

    def castle(self):
        dx, dy = self.return_change()
        return dx != 0 and dy == 0 or dx == 0 and dy != 0

    def knight(self):
        dx, dy = self.return_change()
        dx = abs(dx)
        dy = abs(dy)
        return dx == 2 and dy == 1 or dx == 1 and dy == 2

    def bishop(self):
        dx, dy = self.return_change()
        dx = abs(dx)
        dy = abs(dy)
        return dx == dy and dx != 0

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
        tile = self.chess_board[self.move[1]][self.move[0]]
        if (tile is None or tile.colour != self.piece.colour) and function_dictionary[self.piece.name]():
            return True
        return False

    def validate_move(self, piece, move, chess_board):
        self.piece = piece
        self.move = move
        self.chess_board = chess_board
        if self.in_bounds():
            if self.valid_piece_move():
                return True
        return False
