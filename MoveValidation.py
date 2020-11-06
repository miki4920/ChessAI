from UtilityFunctions import bresenham, delta_distance


class ValidateMove(object):
    def __init__(self):
        self.board_bounds = (0, 7)
        self.colour = True
        self.piece = None
        self.move = None
        self.chess_board = None
        self.tile = None
        self.function_dictionary = {"pawn": self.pawn,
                                    "castle": self.castle,
                                    "knight": self.knight,
                                    "bishop": self.bishop,
                                    "queen": self.queen,
                                    "king": self.king}

    def validate_path(self):
        if self.tile is None or self.tile.colour != self.piece.colour:
            bresenham_list = list(
                bresenham(self.piece.original_position[0], self.piece.original_position[1], self.move[0],
                          self.move[1]))[
                             1:-1]
            if all([self.chess_board.get_tile(coordinate) is None for coordinate in bresenham_list]):
                return True
        return False

    def en_passant(self, dx):
        output = {}
        if 0 <= self.piece.original_position[0] + dx <= 7:
            side_tile = self.chess_board.get_tile(
                (self.piece.original_position[0] + dx, self.piece.original_position[1]))
            side_tile = side_tile if side_tile and side_tile.previous_position else None
            if self.tile is None and side_tile and side_tile.colour != self.piece.colour and side_tile.name == "pawn" and abs(
                    side_tile.original_position[1] - side_tile.previous_position[1]) == 2 and abs(dx) == 1:
                output = {"move": self.move,
                          "en_passant": side_tile.original_position}
        return output

    def pawn(self, change):
        dx, dy = change
        dy = dy * (1 if self.piece.colour else -1)
        output = {}
        if dy == 1 and dx == 0 and self.tile is None:
            output = {"move": self.move}
        elif 1 <= dy <= 2 and dx == 0 and self.validate_path() and not self.piece.previous_position:
            output = {"move": self.move}
        elif abs(dx) == 1 and dy == 1:
            if self.tile and self.tile.colour != self.piece.colour:
                output = {"capture": self.move}
            elif self.en_passant(dx):
                output = self.en_passant(dx)
        return output

    def castle(self, change):
        dx, dy = change
        output = {}
        if (dx != 0 and dy == 0 or dx == 0 and dy != 0) and self.validate_path():
            if self.tile is None:
                output = {"move": self.move}
            else:
                output = {"capture": self.move}
        return output

    def knight(self, change):
        dx, dy = list(map(abs, change))
        output = {}
        if dx == 2 and dy == 1 or dx == 1 and dy == 2:
            if self.tile is None:
                output = {"move": self.move}
            else:
                output = {"capture": self.move}
        return output

    def bishop(self, change):
        dx, dy = list(map(abs, change))
        output = {}
        if dx != 0 and dx == dy and self.validate_path():
            if self.tile is None:
                output = {"move": self.move}
            else:
                output = {"capture": self.move}
        return output

    def queen(self, change):
        return self.bishop(change) or self.castle(change)

    def castling(self, dx, dy):
        castle_dictionary = {(2, 0): ((0, 0), (3, 0)),
                             (6, 0): ((7, 0), (5, 0)),
                             (2, 7): ((0, 7), (3, 7)),
                             (6, 7): ((7, 7), (5, 7))}
        if dx == 2 and dy == 0 and not self.piece.previous_position and self.validate_path():
            castle_coordinates = castle_dictionary[tuple(self.move)]
            tile = self.chess_board.get_tile(castle_coordinates[0])
            if tile and tile.name == "castle" and not tile.previous_position:
                return tile, castle_coordinates[1]
        return {}

    def king(self, change):
        output = {}
        dx, dy = list(map(abs, change))
        if dx < 2 and dy < 2 and (dx != 0 or dy != 0):
            if self.tile is None:
                output = {"move": self.move}
            else:
                output = {"capture": self.move}
        elif self.castling(dx, dy):
            output = {"move": self.move,
                      "castling": self.castling(dx, dy)}
        return output

    def validate_move(self, piece, chess_board, move, check):
        self.piece = piece
        self.move = move
        self.chess_board = chess_board
        self.tile = self.chess_board.get_tile(self.move)
        if self.tile is None or self.tile.colour != self.piece.colour:
            change = delta_distance(self.move, self.piece.original_position)
            output = self.function_dictionary[self.piece.name](change)
            if check and output:
                tile = self.chess_board.get_tile(move)
                self.chess_board.set_tile(move, self.piece)
                if self.check_for_check(self.chess_board):
                    return {}
                self.chess_board.set_tile(move, tile)
                return output
        return {}

    def validate_moves(self, piece, chess_board, check=False):
        moves = []
        for move in chess_board.all_moves:
            output = self.validate_move(piece, chess_board, move, check)
            if output:
                moves.append(output)
        return moves

    def check_for_check(self, chess_board):
        pieces = chess_board.get_all_pieces_colour(not self.colour)
        for piece in pieces:
            for move in self.validate_moves(piece, chess_board):
                capture = move.get("capture")
                if capture:
                    tile = self.chess_board.get_tile(capture)
                    if tile.name == "king":
                        return move
        return {}
