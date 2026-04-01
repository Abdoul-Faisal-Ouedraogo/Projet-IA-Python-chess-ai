class AI:
    def __init__(self, depth):
        self.depth = depth

    def choose_move(self, board):
        score, move = minimax(...)
        return move
