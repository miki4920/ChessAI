from ChessObjects import Piece


def get_initial_chessboard(size):
    chessboard = [list([None] * 8) for _ in range(0, 8)]
    chessboard = create_pawns(chessboard, size)
    chessboard = create_other_pieces(chessboard, size)
    return chessboard


def create_pawns(chessboard, size):
    for index in range(0, 8):
        chessboard[1][index] = Piece("pawn", True, size)
        chessboard[6][index] = Piece("pawn", False, size)
    return chessboard


def create_other_pieces(chessboard, size):
    pieces_dictionary = {0: "castle",
                         1: "knight",
                         2: "bishop",
                         3: "queen",
                         4: "king",
                         5: "bishop",
                         6: "knight",
                         7: "castle", }
    for index in range(0, 8):
        chessboard[0][index] = Piece(pieces_dictionary[index], True, size)
        chessboard[7][index] = Piece(pieces_dictionary[index], False, size)
    return chessboard


class ChessBoard(object):
    def __init__(self, square_size):
        self.chess_board = get_initial_chessboard(square_size)

    def get_tile(self, move):
        return self.chess_board[move[1]][move[0]]

    def set_tile(self, move, value):
        self.chess_board[move[1]][move[0]] = value

    @staticmethod
    def get_all_moves():
        moves = []
        for y in range(0, 8):
            for x in range(0, 8):
                moves.append([x, y])
        return moves

    def get_all_pieces_colour(self, colour):
        pieces = []
        for move in self.get_all_moves():
            if self.get_tile(move) is not None and self.get_tile(move).colour == colour:
                pieces.append(self.get_tile(move))
        return pieces

    def draw(self):
        [piece.draw() for piece in sum(self.chess_board, []) if piece]
