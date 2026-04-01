import json
from src.core.board import Board
from src.core.square import Square
from src.core.piece import Pawn, Knight, Bishop, Rook, Queen, King

def load_game(game, path="save.json"):
    with open(path, "r") as f:
        data = json.load(f)

    # Réinitialiser le jeu
    game.reset()
    board = game.board

    # Vider le plateau
    for row in range(8):
        for col in range(8):
            board.squares[row][col].piece = None

    # Recréer les pièces
    for p in data["pieces"]:
        type_ = p["type"]
        color = p["color"]
        row = p["row"]
        col = p["col"]

        cls = {
            "pawn": Pawn,
            "knight": Knight,
            "bishop": Bishop,
            "rook": Rook,
            "queen": Queen,
            "king": King
        }[type_]

        piece = cls(color)
        piece.moved = p["moved"]
        if hasattr(piece, "en_passant"):
            piece.en_passant = p.get("en_passant", False)

        board.squares[row][col].piece = piece

    # Restaurer les autres infos
    game.next_player = data["current_player"]
    game.white_time = data.get("white_time", 0)
    game.black_time = data.get("black_time", 0)
    game.ai_enabled = data.get("ai_enabled", False)
    game.ai_color = data.get("ai_color", "black")
    game.ai_depth = data.get("ai_depth", 2)

    # Historique
    game.move_history = []

    print("Partie chargée :", path)
