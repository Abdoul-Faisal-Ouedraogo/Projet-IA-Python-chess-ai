# src/core/move.py

class Move:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final
        self.promotion = None   # utile plus tard
        self.piece_moved = None

    def __eq__(self, other):
        return (
            self.initial == other.initial and
            self.final == other.final
        )

    def to_pgn(self, board):
        """
        Convertit un coup en notation PGN simple.
        Compatible avec ton moteur actuel.
        """

        piece = self.piece_moved   # <-- LA CORRECTION IMPORTANTE

        # Nom de la pièce (vide pour les pions)
        name = "" if piece.name == "pawn" else piece.name[0].upper()

        # Capture ?
        capture = "x" if self.final.piece else ""

        # Coordonnées finales
        col = chr(self.final.col + ord('a'))
        row = str(8 - self.final.row)

        # Roque
        if piece.name == "king" and abs(self.final.col - self.initial.col) == 2:
            return "O-O" if self.final.col == 6 else "O-O-O"

        # Promotion
        promo = ""
        if self.promotion:
            promo = f"={self.promotion.upper()}"

        return f"{name}{capture}{col}{row}{promo}"
