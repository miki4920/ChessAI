class ValidateMove(object):
    def __init__(self):
        self.board_bounds = (0, 7)
        self.piece = None
        self.move = None
        self.chess_board = None

    def in_bounds(self):
        return self.board_bounds[0] <= self.move[0] <= self.board_bounds[1] and self.board_bounds[0] <= self.move[
            1] <= self.board_bounds[1]

    def valid_piece_move(self):
        tile = self.chess_board[self.move[1]][self.move[0]]
        if tile is None or tile.colour != self.piece.colour:
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
