class ValidateMove(object):
    def __init__(self):
        self.board_bounds = (0, 7)

    def in_bounds(self, destination):
        return self.board_bounds <= destination <= self.board_bounds
