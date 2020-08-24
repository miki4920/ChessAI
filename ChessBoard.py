class ChessBoard(object):
    def __init__(self):
        self.chess_board = self.get_initial_chessboard()

    def get_initial_chessboard(self):
        chessboard = [list([None] * 8) for _ in range(0, 8)]
        chessboard = self.create_pawns(chessboard)
        chessboard = self.create_other_pieces(chessboard)
        return chessboard

    @staticmethod
    def create_pawns(chessboard):
        for index in range(0, 8):
            chessboard[6][index] = "pawn" + "_b"
            chessboard[1][index] = "pawn" + "_w"
        return chessboard

    @staticmethod
    def create_other_pieces(chessboard):
        pieces_dictionary = {0: "castle",
                             1: "knight",
                             2: "bishop",
                             3: "queen",
                             4: "king",
                             5: "bishop",
                             6: "knight",
                             7: "castle", }
        for index in range(0, 8):
            chessboard[0][index] = pieces_dictionary[index] + "_w"
            chessboard[7][index] = pieces_dictionary[index] + "_b"
        return chessboard
