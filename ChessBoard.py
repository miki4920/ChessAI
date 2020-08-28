from ChessObjects import Piece


class ChessBoard(object):
    def __init__(self, square_size):
        self.square_size = square_size

    def get_initial_chessboard(self):
        chessboard = [list([None] * 8) for _ in range(0, 8)]
        chessboard = self.create_pawns(chessboard)
        chessboard = self.create_other_pieces(chessboard)
        return chessboard

    def create_pawns(self, chessboard):
        for index in range(0, 8):
            chessboard[1][index] = Piece("pawn", True, self.square_size)
            chessboard[6][index] = Piece("pawn", False, self.square_size)
        return chessboard

    def create_other_pieces(self, chessboard):
        pieces_dictionary = {0: "castle",
                             1: "knight",
                             2: "bishop",
                             3: "queen",
                             4: "king",
                             5: "bishop",
                             6: "knight",
                             7: "castle", }
        for index in range(0, 8):
            chessboard[0][index] = Piece(pieces_dictionary[index], True, self.square_size)
            chessboard[7][index] = Piece(pieces_dictionary[index], False, self.square_size)
        return chessboard
