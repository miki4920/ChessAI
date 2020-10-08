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
        self.all_moves = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [0, 1], [1, 1], [2, 1],
                          [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2],
                          [6, 2], [7, 2], [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [0, 4],
                          [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [0, 5], [1, 5], [2, 5], [3, 5],
                          [4, 5], [5, 5], [6, 5], [7, 5], [0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6],
                          [7, 6], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7], [7, 7]]

    def get_tile(self, move):
        return self.chess_board[move[1]][move[0]]

    def set_tile(self, move, value):
        self.chess_board[move[1]][move[0]] = value

    def get_all_pieces_colour(self, colour):
        pieces = []
        for move in self.all_moves:
            if self.get_tile(move) is not None and self.get_tile(move).colour == colour:
                pieces.append(self.get_tile(move))
        return pieces

    def draw(self):
        [piece.draw() for piece in sum(self.chess_board, []) if piece]
