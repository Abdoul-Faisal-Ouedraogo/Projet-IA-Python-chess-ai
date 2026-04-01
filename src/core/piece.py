import os

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        # L'IA maximisera pour les blancs (+1) et minimisera pour les noirs (-1)
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        self.en_passant = False
        # Table de position : encourage les pions à avancer au centre
        self.position_weights = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, -20, -20, 10, 10,  5],
            [5, -5, -10,  0,  0, -10, -5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        super().__init__('pawn', color, 100.0) # On passe en nombres entiers pour la précision

class Knight(Piece):
    def __init__(self, color):
        # Le cavalier est pénalisé sur les bords (moins de mobilité)
        self.position_weights = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,  0,  5,  5,  0, -20, -40],
            [-30,  5, 10, 15, 15, 10,  5, -30],
            [-30,  0, 15, 20, 20, 15,  0, -30],
            [-30,  5, 15, 20, 20, 15,  5, -30],
            [-30,  0, 10, 15, 15, 10,  0, -30],
            [-40, -20,  0,  0,  0,  0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]
        super().__init__('knight', color, 320.0)

class Bishop(Piece):
    def __init__(self, color):
        self.position_weights = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10,  5,  0,  0,  0,  0,  5, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10,  0, 10, 10, 10, 10,  0, -10],
            [-10,  5,  5, 10, 10,  5,  5, -10],
            [-10,  0,  5, 10, 10,  5,  0, -10],
            [-10,  0,  0,  0,  0,  0,  0, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ]
        super().__init__('bishop', color, 330.0)

class Rook(Piece):
    def __init__(self, color):
        self.position_weights = [
            [0,  0,  0,  5,  5,  0,  0,  0],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        super().__init__('rook', color, 500.0)

class Queen(Piece):
    def __init__(self, color):
        self.position_weights = [
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10,  0,  5,  0,  0,  0,  0, -10],
            [-10,  5,  5,  5,  5,  5,  0, -10],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [-10,  0,  5,  5,  5,  5,  0, -10],
            [-10,  0,  0,  0,  0,  0,  0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20]
        ]
        super().__init__('queen', color, 900.0)

class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        # Le roi doit rester à l'abri au début (coins)
        self.position_weights = [
            [20, 30, 10,  0,  0, 10, 30, 20],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30]
        ]
        super().__init__('king', color, 20000.0)