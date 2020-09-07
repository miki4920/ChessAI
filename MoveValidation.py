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
        dx = move[0] - piece[0]
        dy = move[1] - piece[1]
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

    def en_passant(self, dx):
        output = {}
        if 0 <= self.piece.original_position[0] + dx <= 7:
            side_tile = self.chess_board.get_tile(
                (self.piece.original_position[0] + dx, self.piece.original_position[1]))
            side_tile = side_tile if side_tile is not None and side_tile.previous_position is not None else None
            if self.tile is None and side_tile is not None and side_tile.colour != self.piece.colour and side_tile.name == "pawn" and abs(
                    side_tile.original_position[1] - side_tile.previous_position[1]) == 2 and abs(dx) == 1:
                output = {"en_passant": side_tile}
        return output

    def pawn(self, change):
        dx, dy = change
        colour = 1 if self.piece.colour else -1
        dy = dy * colour
        output = {}
        if abs(dx) == 1 and dy == 1:
            if self.tile is not None and self.tile.colour != self.piece.colour:
                output = {"capture": True}
            elif self.en_passant(dx):
                output = self.en_passant(dx)
        elif dy == 1 and dx == 0 and self.tile is None:
            output = {"move": True}
        elif 1 <= dy <= 2 and dx == 0 and self.validate_path() and not self.piece.previous_position:
            output = {"move": True}
        return output

    def castle(self, change):
        dx, dy = change
        output = {}
        if (dx != 0 and dy == 0 or dx == 0 and dy != 0) and self.validate_path():
            if self.tile is None:
                output = {"move": True}
            else:
                output = {"capture": True}
        return output

    def knight(self, change):
        dx, dy = list(map(abs, change))
        output = {}
        if dx == 2 and dy == 1 or dx == 1 and dy == 2:
            if self.tile is None:
                output = {"move": True}
            else:
                output = {"capture": True}
        return output

    def bishop(self, change):
        dx, dy = list(map(abs, change))
        output = {}
        if dx == dy and dx != 0 and self.validate_path():
            if self.tile is None:
                output = {"move": True}
            else:
                output = {"capture": True}
        return output

    def queen(self, change):
        return self.bishop(change) or self.castle(change)

    def castling(self, dx):
        return False

    def king(self, change):
        output = {}
        dx, dy = list(map(abs, change))
        if dx < 2 and dy < 2 and (dx != 0 or dy != 0):
            if self.tile is None:
                output = {"move": True}
            else:
                output = {"capture": True}
        elif self.castling(dx):
            output = {"castling": self.castling(change[0])}
        return output

    def valid_piece_move(self):
        function_dictionary = {"pawn": self.pawn,
                               "castle": self.castle,
                               "knight": self.knight,
                               "bishop": self.bishop,
                               "queen": self.queen,
                               "king": self.king}
        change = self.return_change(self.move, self.piece.original_position)
        if self.tile is None or self.tile.colour != self.piece.colour:
            return function_dictionary[self.piece.name](change)
        return {}

    def validate_move(self, piece, chess_board, move, check):
        self.piece = piece
        self.move = move
        self.chess_board = chess_board
        self.tile = self.chess_board.get_tile(self.move)
        output = self.valid_piece_move()
        if check and output:
            tile = self.chess_board.get_tile(move)
            self.chess_board.set_tile(move, self.piece)
            if self.check(self.chess_board):
                output = {}
            self.chess_board.set_tile(move, tile)
        return output

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
