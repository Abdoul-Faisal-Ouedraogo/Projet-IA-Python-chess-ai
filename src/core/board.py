import copy
import os

# Constantes
from src.config.const import *

# Classes du core
from src.core.square import Square
from src.core.move import Move
from src.core.piece import Pawn, Knight, Bishop, Rook, Queen, King

# Sons
from src.gui.sound import Sound


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._history = []  # pour make_move / undo_move
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    # -------------------------
    #   MOTEUR DE COUPS
    # -------------------------

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join('assets/sounds/capture.wav'))
                    sound.play()
            else:
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True
        piece.clear_moves()
        self.last_move = move

    def make_move(self, piece, move):
        """Version logique ultra rapide pour l'IA (sans sons, sans roque auto)."""
        initial = move.initial
        final = move.final

        captured_piece = self.squares[final.row][final.col].piece
        self._history.append(
            (piece, move, captured_piece, piece.moved, self.last_move)
        )

        # déplacement simple
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        piece.moved = True
        self.last_move = move

    def undo_move(self):
        """Annule le dernier coup joué par make_move()."""
        piece, move, captured_piece, old_moved, old_last = self._history.pop()

        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = piece
        self.squares[final.row][final.col].piece = captured_piece
        piece.moved = old_moved
        self.last_move = old_last

    def valid_move(self, piece, move):
        return move in piece.moves

    # -------------------------
    #   UTILITAIRES IA
    # -------------------------

    def hash(self):
        """Hash logique du plateau pour la transposition."""
        h = 0
        for row in range(8):
            for col in range(8):
                sq = self.squares[row][col]
                if sq.has_piece():
                    p = sq.piece
                    h ^= hash((row, col, p.name, p.color, p.moved))
        return h

    def count_pieces(self):
        """Retourne le nombre total de pièces sur le plateau."""
        count = 0
        for row in range(8):
            for col in range(8):
                if self.squares[row][col].has_piece():
                    count += 1
        return count

    def get_all_valid_moves(self, color):
        """Retourne la liste de tous les coups valides pour une couleur."""
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(color):
                    piece = self.squares[row][col].piece
                    self.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        moves.append(move)
        return moves

    # -------------------------
    #   PROMO / ROQUE / EN PASSANT
    # -------------------------

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        piece.en_passant = True

    # -------------------------
    #   CHECK / MOUVEMENTS
    # -------------------------

    def in_check(self, piece, move):
        """Teste si un coup laisse son propre roi en échec (version sans deepcopy)."""
        self.make_move(piece, move)
        in_check = self.is_in_check(piece.color)
        self.undo_move()
        return in_check

    def calc_moves(self, piece, row, col, bool=True):
        # (ton code calc_moves inchangé, je le laisse tel quel)
        # ------------- COPIE EXACTE DE TA VERSION ACTUELLE -------------
        def pawn_moves():
            steps = 1 if piece.moved else 2
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else:
                        break
                else:
                    break

            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn) and p.en_passant:
                        initial = Square(row, col)
                        final = Square(fr, col-1, p)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn) and p.en_passant:
                        initial = Square(row, col)
                        final = Square(fr, col+1, p)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]
            for possible_move_row, possible_move_col in possible_moves:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

        def straightline_moves(incrs):
            for row_incr, col_incr in incrs:
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    else:
                        break
                    possible_move_row += row_incr
                    possible_move_col += col_incr

        def king_moves():
            adjs = [
                (row-1, col+0),
                (row-1, col+1),
                (row+0, col+1),
                (row+1, col+1),
                (row+1, col+0),
                (row+1, col-1),
                (row+0, col-1),
                (row-1, col-1),
            ]
            for possible_move_row, possible_move_col in adjs:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

            if not piece.moved:
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook) and not left_rook.moved:
                    for c in range(1, 4):
                        if self.squares[row][c].has_piece():
                            break
                        if c == 3:
                            piece.left_rook = left_rook
                            initial = Square(row, 0)
                            final = Square(row, 3)
                            moveR = Move(initial, final)
                            initial = Square(row, col)
                            final = Square(row, 2)
                            moveK = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)
                            else:
                                left_rook.add_move(moveR)
                                piece.add_move(moveK)

                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook) and not right_rook.moved:
                    for c in range(5, 7):
                        if self.squares[row][c].has_piece():
                            break
                        if c == 6:
                            piece.right_rook = right_rook
                            initial = Square(row, 7)
                            final = Square(row, 5)
                            moveR = Move(initial, final)
                            initial = Square(row, col)
                            final = Square(row, 6)
                            moveK = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)
                            else:
                                right_rook.add_move(moveR)
                                piece.add_move(moveK)

        piece.clear_moves()

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([(-1, 1), (-1, -1), (1, 1), (1, -1)])
        elif isinstance(piece, Rook):
            straightline_moves([(-1, 0), (0, 1), (1, 0), (0, -1)])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1), (-1, -1), (1, 1), (1, -1),
                (-1, 0), (0, 1), (1, 0), (0, -1)
            ])
        elif isinstance(piece, King):
            king_moves()

    # -------------------------
    #   CREATION DU PLATEAU
    # -------------------------

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    # -------------------------
    #   CHECK / MAT
    # -------------------------

    def has_valid_moves(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(color):
                    piece = self.squares[row][col].piece
                    self.calc_moves(piece, row, col, bool=True)
                    if len(piece.moves) > 0:
                        return True
        return False

    def is_in_check(self, color):
        """Vérifie si le roi de la couleur donnée est attaqué."""
        king_pos = None
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(color):
                    piece = self.squares[row][col].piece
                    if piece.name.lower() == 'king':
                        king_pos = (row, col)
                        break
            if king_pos:
                break

        if king_pos is None:
            return False

        enemy_color = 'white' if color == 'black' else 'black'
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(enemy_color):
                    p = self.squares[row][col].piece
                    self.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if m.final.row == king_pos[0] and m.final.col == king_pos[1]:
                            return True
        return False

    def count_pieces_color(self, color):
        count = 0
        for row in range(8):
            for col in range(8):
                if self.squares[row][col].has_team_piece(color):
                    count += 1
        return count
