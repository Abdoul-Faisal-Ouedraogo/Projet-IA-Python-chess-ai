import pygame
import sys

from src.config.const import *
from src.game import Game
from src.core.square import Square
from src.core.move import Move


class Main:
    def __init__(self, ai_enabled=False, ai_color="black", ai_depth=2):
        pygame.init()

        self.ai_enabled = ai_enabled
        self.ai_color = ai_color
        self.ai_depth = ai_depth

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess AI - Master Data Engineer")

        self.main = Game(
            ai_enabled=self.ai_enabled,
            ai_color=self.ai_color,
            ai_depth=self.ai_depth
        )

        # Boutons
        self.theme_button = pygame.Rect(10, 10, 120, 40)
        self.save_button = pygame.Rect(WIDTH - 130, 10, 120, 40)
        self.load_button = pygame.Rect(WIDTH - 130, 60, 120, 40)
        self.reset_button = pygame.Rect(WIDTH - 130, 110, 120, 40)
        self.pause_button = pygame.Rect(WIDTH - 130, 160, 120, 40)
        self.quit_button = pygame.Rect(WIDTH - 130, 210, 120, 40)

    def mainloop(self):
        while True:
            screen = self.screen
            game = self.main
            board = game.board
            dragger = game.dragger

            # Mise à jour horloge
            game.update_clock()

            # Si le jeu est en pause → on freeze tout
            if game.paused:
                pygame.draw.rect(screen, (240, 240, 240), (0, 0, WIDTH, TOP_UI))
                pause_text = game.config.font.render("⏸ Jeu en pause", True, (0, 0, 0))
                screen.blit(pause_text, (WIDTH//2 - 80, 20))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.pause_button.collidepoint(event.pos):
                            game.paused = False
                continue

            # --- AFFICHAGE PLATEAU ---
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            # --- BARRE DU HAUT ---
            pygame.draw.rect(screen, (240, 240, 240), (0, 0, WIDTH, TOP_UI))

            # Tour de jeu
            current = game.white_name if game.next_player == 'white' else game.black_name
            turn_text = game.config.font.render(f"Tour : {current}", True, (0, 0, 0))
            screen.blit(turn_text, (20, 10))

            # Horloge
            white_t = int(game.white_time)
            black_t = int(game.black_time)
            clock_text = game.config.font.render(
                f"⏱ Blanc : {white_t}s   Noir : {black_t}s",
                True, (0, 0, 0)
            )
            screen.blit(clock_text, (20, 45))

            # Compteur de pièces
            white_count = board.count_pieces_color("white")
            black_count = board.count_pieces_color("black")
            count_text = game.config.font.render(
                f"♙ Blanc : {white_count}   ♟ Noir : {black_count}",
                True, (0, 0, 0)
            )
            screen.blit(count_text, (20, 80))

            # Boutons
            pygame.draw.rect(screen, (200, 200, 200), self.theme_button, border_radius=6)
            screen.blit(game.config.font.render("Thème", True, (0, 0, 0)),
                        (self.theme_button.x + 20, self.theme_button.y + 10))

            pygame.draw.rect(screen, (200, 200, 200), self.save_button, border_radius=6)
            screen.blit(game.config.font.render("Enregistrer", True, (0, 0, 0)),
                        (self.save_button.x + 10, self.save_button.y + 10))

            pygame.draw.rect(screen, (200, 200, 200), self.load_button, border_radius=6)
            screen.blit(game.config.font.render("Charger", True, (0, 0, 0)),
                        (self.load_button.x + 20, self.load_button.y + 10))

            pygame.draw.rect(screen, (200, 200, 200), self.reset_button, border_radius=6)
            screen.blit(game.config.font.render("Recommencer", True, (0, 0, 0)),
                        (self.reset_button.x + 5, self.reset_button.y + 10))

            pygame.draw.rect(screen, (200, 200, 200), self.pause_button, border_radius=6)
            screen.blit(game.config.font.render("Pause", True, (0, 0, 0)),
                        (self.pause_button.x + 25, self.pause_button.y + 10))

            pygame.draw.rect(screen, (200, 200, 200), self.quit_button, border_radius=6)
            screen.blit(game.config.font.render("Quitter", True, (0, 0, 0)),
                        (self.quit_button.x + 25, self.quit_button.y + 10))

            # Pièce en cours de drag
            if dragger.dragging:
                dragger.update_blit(screen)

            # --- IA ---
            if game.active and game.ai_enabled and game.next_player == game.ai_color:
                move = game.compute_ai_move()
                if move:
                    move.piece_moved = board.squares[move.initial.row][move.initial.col].piece
                    board.move(move.piece_moved, move)
                    game.move_history.append(move)
                    game.next_turn()

                    result = game.check_endgame()
                    if result:
                        game.end_message = result

            # --- EVENTS ---
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Écran de fin
                if not game.active:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if game.replay_button.collidepoint(event.pos):
                            game.reset()
                            continue
                        if game.quit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                    continue

                # CLIC SOURIS
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Boutons
                    if self.theme_button.collidepoint(event.pos):
                        game.change_theme()
                        continue

                    if self.save_button.collidepoint(event.pos):
                        from src.io.save import save_game
                        save_game(game)
                        continue

                    if self.load_button.collidepoint(event.pos):
                        from src.io.load import load_game
                        load_game(game)
                        continue

                    if self.reset_button.collidepoint(event.pos):
                        game.reset()
                        continue

                    if self.pause_button.collidepoint(event.pos):
                        game.paused = True
                        continue

                    if self.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                    # Empêcher de jouer pendant IA
                    if game.ai_enabled and game.next_player == game.ai_color:
                        continue

                    dragger.update_mouse(event.pos)
                    if dragger.mouseY < TOP_UI:
                        continue

                    clicked_row = (dragger.mouseY - TOP_UI) // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if 0 <= clicked_row < 8 and 0 <= clicked_col < 8:
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if piece.color == game.next_player:
                                board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)

                # MOUVEMENT SOURIS
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                    motion_row = (event.pos[1] - TOP_UI) // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    if 0 <= motion_row < 8 and 0 <= motion_col < 8:
                        game.set_hover(motion_row, motion_col)

                # RELÂCHER CLIC
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:

                        if game.ai_enabled and game.next_player == game.ai_color:
                            dragger.undrag_piece()
                            continue

                        dragger.update_mouse(event.pos)
                        released_row = (dragger.mouseY - TOP_UI) // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        if 0 <= released_row < 8 and 0 <= released_col < 8:
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)
                            move.piece_moved = dragger.piece

                            if board.valid_move(dragger.piece, move):
                                captured = board.squares[released_row][released_col].has_piece()
                                board.move(dragger.piece, move)
                                board.set_true_en_passant(dragger.piece)
                                game.play_sound(captured)
                                game.move_history.append(move)
                                game.next_turn()

                                result = game.check_endgame()
                                if result:
                                    game.end_message = result

                        dragger.undrag_piece()

            # Écran de fin
            if not game.active:
                game.show_end_screen(screen, game.end_message)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.mainloop()
