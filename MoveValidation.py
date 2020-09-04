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

    @staticmethod
    def return_change(move, piece):
        try:
            dx = move[0] - piece[0]
            dy = move[1] - piece[1]
            return dx, dy
        except:
            print(move, piece)

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
        dx, dy = self.return_change(self.move, self.piece.original_position)
        colour = 1 if self.piece.colour else -1
        dy = dy * colour
        if abs(dx) == 1 and dy == 1:
            if self.tile is not None and self.tile.colour != self.piece.colour:
                return True
            if 0 <= self.piece.original_position[0] + colour <= 7:
                side_tile = self.chess_board.get_tile(
                    (self.piece.original_position[0] + colour, self.piece.original_position[1]))
                side_tile = side_tile if side_tile is not None and side_tile.previous_position is not None else None
                if self.tile is None and side_tile is not None and side_tile.colour != self.piece.colour and abs(
                        side_tile.original_position[1] - side_tile.previous_position[1]) == 2 and dx == 1:
                    return True
            elif 0 <= self.piece.original_position[0] - colour <= 7:
                side_tile = self.chess_board.get_tile(
                    (self.piece.original_position[0] - colour, self.piece.original_position[1]))
                side_tile = side_tile if side_tile is not None and side_tile.previous_position is not None else None
                if self.tile is None and side_tile is not None and side_tile.colour != self.piece.colour and abs(
                        side_tile.original_position[1] - side_tile.previous_position[1]) == 2 and dx == -1:
                    return True
        elif self.piece.previous_position and dy == 1 and dx == 0 and self.tile is None:
            return True
        elif 1 <= dy <= 2 and dx == 0 and self.validate_path() and not self.piece.previous_position:
            return True
        return False

    def castle(self):
        dx, dy = self.return_change(self.move, self.piece.original_position)
        if dx != 0 and dy == 0 or dx == 0 and dy != 0:
            return self.validate_path()
        return False

    def knight(self):
        dx, dy = self.return_change(self.move, self.piece.original_position)
        dx = abs(dx)
        dy = abs(dy)
        return dx == 2 and dy == 1 or dx == 1 and dy == 2

    def bishop(self):
        dx, dy = self.return_change(self.move, self.piece.original_position)
        dx = abs(dx)
        dy = abs(dy)
        if dx == dy and dx != 0:
            return self.validate_path()
        return False

    def queen(self):
        return self.bishop() or self.castle()

    def king(self):
        dx, dy = self.return_change(self.move, self.piece.original_position)
        dx = abs(dx)
        dy = abs(dy)
        return dx < 2 and dy < 2 and (dx != 0 or dy != 0)

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

    def validate_move(self, piece, chess_board, move, check):
        self.piece = piece
        self.move = move
        self.chess_board = chess_board
        self.tile = self.chess_board.get_tile(self.move)
        valid = True
        if not self.valid_piece_move():
            valid = False
        if check and valid:
            tile = self.chess_board.get_tile(move)
            self.chess_board.set_tile(move, self.piece)
            if self.check(self.chess_board):
                valid = False
            self.chess_board.set_tile(move, tile)
        return valid

    def validate_moves(self, piece, chess_board, check=False):
        moves = [move for move in chess_board.get_all_moves() if self.validate_move(piece, chess_board, move, check)]
        return moves

    def check(self, chess_board):
        pieces = chess_board.get_all_pieces_colour(not self.colour)
        check = False
        for piece in pieces:
            for move in self.validate_moves(piece, chess_board):
                move = self.chess_board.get_tile(move)
                if move is not None and move.name == "king":
                    check = True
                    break
        return check
