from random import choice


class ChessAI(object):
    def __init__(self):
        pass

    @staticmethod
    def get_a_move(chess_board, validator):
        valid_moves = []
        piece_moves = {}
        for piece in chess_board.get_all_pieces_colour(validator.colour):
            moves = validator.validate_moves(piece, chess_board, True)
            if len(moves) == 0:
                pass
            else:
                piece_moves[piece] = moves
                valid_moves.append(piece_moves)
                piece_moves = {}
        move = choice(valid_moves)
        piece = list(move.keys())[0]
        destination = choice(move[piece])
        destination = list(destination.values())[0]
        return piece, destination
