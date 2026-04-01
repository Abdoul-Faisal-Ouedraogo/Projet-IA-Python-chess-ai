from src.core.evaluation import evaluate

transposition = {}


def order_moves(board, moves):
    scored = []
    for move in moves:
        score = 0
        if board.squares[move.final.row][move.final.col].has_piece():
            score += 100
        if hasattr(move, "promotion") and move.promotion:
            score += 50
        if move.final.col in [3, 4] and move.final.row in [3, 4]:
            score += 10
        scored.append((score, move))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored]


def minimax(board, depth, alpha, beta, maximizing_player):
    color = 'white' if maximizing_player else 'black'

    key = board.hash()
    if key in transposition and transposition[key]["depth"] >= depth:
        return transposition[key]["score"], transposition[key]["move"]

    if depth == 0 or not board.has_valid_moves(color):
        score = evaluate(board)
        transposition[key] = {"score": score, "move": None, "depth": depth}
        return score, None

    best_move = None

    if maximizing_player:
        max_eval = -float('inf')
        moves = order_moves(board, board.get_all_valid_moves('white'))
        for move in moves:
            piece = board.squares[move.initial.row][move.initial.col].piece
            board.make_move(piece, move)

            score, _ = minimax(board, depth - 1, alpha, beta, False)

            board.undo_move()

            if score > max_eval:
                max_eval = score
                best_move = move

            alpha = max(alpha, score)
            if beta <= alpha:
                break

        transposition[key] = {"score": max_eval, "move": best_move, "depth": depth}
        return max_eval, best_move

    else:
        min_eval = float('inf')
        moves = order_moves(board, board.get_all_valid_moves('black'))
        for move in moves:
            piece = board.squares[move.initial.row][move.initial.col].piece
            board.make_move(piece, move)

            score, _ = minimax(board, depth - 1, alpha, beta, True)

            board.undo_move()

            if score < min_eval:
                min_eval = score
                best_move = move

            beta = min(beta, score)
            if beta <= alpha:
                break

        transposition[key] = {"score": min_eval, "move": best_move, "depth": depth}
        return min_eval, best_move
