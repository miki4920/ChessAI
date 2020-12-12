class Validator(object):
    def __init__(self):
        self.board_size = 8

    def king(self, position):
        list_of_moves = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                list_of_moves.append((position[0] + x, position[1] + y))
        list_of_moves.remove(position)
        return list_of_moves

    def rook(self):
        pass

    def bishop(self):
        pass

    def queen(self):
        pass

    def knight(self):
        pass

    def pawn(self):
        pass


a = Validator()
print(a.king((3, 3)))
