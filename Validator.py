class Validator(object):
    def __init__(self):
        self.board_size = 8

    @staticmethod
    def in_bounds(position):
        return 0 <= position <= 7

    def king(self, position):
        list_of_moves = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                list_of_moves.append((position[0] + x, position[1] + y))
        list_of_moves.remove(position)
        return list_of_moves

    def rook(self, position):
        list_of_moves = []
        for y in range(1, 8 - position[1]):
            possible_position = position[1] - y
            if self.in_bounds(possible_position):
                list_of_moves.append((position[0], possible_position))
            possible_position = position[1] + y
            if self.in_bounds(possible_position):
                list_of_moves.append((position[0], possible_position))
        for x in range(1, 8 - position[1]):
            possible_position = position[1] - x
            if self.in_bounds(possible_position):
                list_of_moves.append((possible_position, position[1]))
            possible_position = position[1] + x
            if self.in_bounds(possible_position):
                list_of_moves.append((possible_position, position[1]))
        return list_of_moves

    def bishop(self, position):
        list_of_moves = []
        for first_axis in range(1, 8 - (max))

    def queen(self, position):
        list_of_moves = []

    def knight(self, position):
        list_of_moves = []

    def pawn(self, position):
        pass


a = Validator()
print(a.rook((3, 3)))
