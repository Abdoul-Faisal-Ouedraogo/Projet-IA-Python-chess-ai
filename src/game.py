import pygame

from src.ai.minimax import minimax
from src.config.const import *
from src.config.config import Config
from src.core.board import Board
from src.core.square import Square
from src.gui.dragger import Dragger


class Game:
    def __init__(self, ai_enabled=False, ai_color="black", ai_depth=2):
        self.ai_enabled = ai_enabled
        self.ai_color = ai_color
        self.ai_depth = ai_depth

        self.config = Config()
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.hovered_sqr = None
        self.active = True

        # Historique des coups
        self.move_history = []

        # Horloge
        self.white_time = 0
        self.black_time = 0
        self.last_tick = pygame.time.get_ticks()


        self.white_name = "Joueur Blanc"
        self.black_name = "Joueur Noir"

        # fin de partie
        self.end_message = ""
        self.replay_button = pygame.Rect(0, 0, 0, 0)
        self.quit_button = pygame.Rect(0, 0, 0, 0)

        # pause
        self.paused = False



    # --- AFFICHAGE ---

    def show_game_over(self, surface):
        if not self.active:
            lbl = self.config.font.render("GAME OVER", True, (255, 0, 0))
            lbl_rect = lbl.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            surface.blit(lbl, lbl_rect)

    def show_bg(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQSIZE, TOP_UI + row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    surface.blit(lbl, (5, TOP_UI + 5 + row * SQSIZE))
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    surface.blit(lbl, (col * SQSIZE + SQSIZE - 20, TOP_UI + 8 * SQSIZE - 20))

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = (
                            col * SQSIZE + SQSIZE // 2,
                            TOP_UI + row * SQSIZE + SQSIZE // 2
                        )
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQSIZE, TOP_UI + move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, TOP_UI + pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (
                self.hovered_sqr.col * SQSIZE,
                TOP_UI + self.hovered_sqr.row * SQSIZE,
                SQSIZE,
                SQSIZE
            )
            pygame.draw.rect(surface, color, rect, width=3)

    def show_end_screen(self, surface, result_text):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

        font_big = pygame.font.SysFont("arial", 48, bold=True)
        text = font_big.render(result_text, True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        surface.blit(text, rect)

        font_btn = pygame.font.SysFont("arial", 32)
        replay_text = font_btn.render("Rejouer", True, (0, 0, 0))
        quit_text = font_btn.render("Quitter", True, (0, 0, 0))

        self.replay_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 140, 50)
        self.quit_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 20, 140, 50)

        pygame.draw.rect(surface, (255, 255, 255), self.replay_button, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), self.quit_button, border_radius=8)

        surface.blit(replay_text, (self.replay_button.x + 20, self.replay_button.y + 10))
        surface.blit(quit_text, (self.quit_button.x + 25, self.quit_button.y + 10))

    # --- LOGIQUE ---

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        if row is None or col is None:
            self.hovered_sqr = None
            return
        if 0 <= row < 8 and 0 <= col < 8:
            self.hovered_sqr = self.board.squares[row][col]
        else:
            self.hovered_sqr = None

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def check_endgame(self):
        color = self.next_player

        if not self.board.has_valid_moves(color):
            self.active = False
            if self.board.is_in_check(color):
                return "Échec et mat !"
            else:
                return "Pat !"

        return None

    # --- IA ---

    def compute_ai_move(self):
        dynamic_depth = self.ai_depth
        if self.board.count_pieces() > 20:
            dynamic_depth = 1

        score, best_move = minimax(
            self.board,
            depth=dynamic_depth,
            alpha=-float('inf'),
            beta=float('inf'),
            maximizing_player=(self.ai_color == "white")
        )
        return best_move

    def reset(self):
        self.__init__(
            ai_enabled=self.ai_enabled,
            ai_color=self.ai_color,
            ai_depth=self.ai_depth
        )

    def update_clock(self):
        if not self.active:
            return

        now = pygame.time.get_ticks()
        delta = (now - self.last_tick) / 1000
        self.last_tick = now

        if self.next_player == "white":
            self.white_time += delta
        else:
            self.black_time += delta
