from src.config.const import ROWS, COLS

def evaluate(board):
    """
    Fonction d'évaluation principale.
    Retourne un score positif si les blancs sont mieux,
    négatif si les noirs sont mieux.
    """

    score = 0

    # -------------------------
    # 1. Valeur matérielle + tables de position
    # -------------------------
    for row in range(ROWS):
        for col in range(COLS):
            square = board.squares[row][col]

            if square.has_piece():
                piece = square.piece

                # valeur matérielle (déjà signée selon la couleur)
                piece_value = piece.value

                # table de position (toujours positive pour les blancs)
                pos_value = piece.position_weights[row][col]

                # si la pièce est noire → inverser la table
                if piece.color == "black":
                    pos_value = -pos_value

                score += piece_value + pos_value

    # -------------------------
    # 2. Mobilité (nombre de coups possibles)
    # -------------------------
    white_moves = _count_moves(board, "white")
    black_moves = _count_moves(board, "black")

    score += (white_moves - black_moves) * 0.1  # petit impact

    # -------------------------
    # 3. Roi en échec
    # -------------------------
    if board.is_in_check("white"):
        score -= 50
    if board.is_in_check("black"):
        score += 50

    # -------------------------
    # 4. Échec et mat / pat
    # -------------------------
    if not board.has_valid_moves("white"):
        if board.is_in_check("white"):
            return -99999  # les blancs sont mats
        else:
            return 0       # pat

    if not board.has_valid_moves("black"):
        if board.is_in_check("black"):
            return 99999   # les noirs sont mats
        else:
            return 0       # pat

    return score


# ---------------------------------------------------------
#   FONCTION INTERNE : compter les coups possibles
# ---------------------------------------------------------

def _count_moves(board, color):
    """Retourne le nombre total de coups possibles pour une couleur."""
    count = 0
    for row in range(ROWS):
        for col in range(COLS):
            if board.squares[row][col].has_team_piece(color):
                piece = board.squares[row][col].piece
                board.calc_moves(piece, row, col, True)
                count += len(piece.moves)
    return count
