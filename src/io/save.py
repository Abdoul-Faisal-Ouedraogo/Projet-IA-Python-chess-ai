import json

def save_game(game, path="save.json"):
    board = game.board

    data = {
        "current_player": game.next_player,
        "white_time": game.white_time,
        "black_time": game.black_time,
        "ai_enabled": game.ai_enabled,
        "ai_color": game.ai_color,
        "ai_depth": game.ai_depth,
        "move_history": [m.to_pgn(board) for m in game.move_history],
        "pieces": []
    }

    for row in range(8):
        for col in range(8):
            square = board.squares[row][col]
            if square.has_piece():
                piece = square.piece
                data["pieces"].append({
                    "type": piece.name.lower(),
                    "color": piece.color,
                    "row": row,
                    "col": col,
                    "moved": piece.moved,
                    "en_passant": getattr(piece, "en_passant", False)
                })

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    print("Partie enregistrée :", path)
