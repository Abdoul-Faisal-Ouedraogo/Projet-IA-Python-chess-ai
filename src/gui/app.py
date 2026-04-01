import pygame
from ..main import Main
from src.config.color import Color   # si tu utilises Color ailleurs


class App:

    def __init__(self):
        pygame.init()

        # paramètres IA par défaut
        self.ai_enabled = False
        self.ai_color = "black"
        self.ai_depth = 2

        # Main sera créé seulement au lancement de la partie
        self.main = None

        self.state = "menu"


    def run(self):
        while True:
            if self.state == "menu":
                self.render_menu()
                self.handle_menu_events()
            else:
                self.main.mainloop()


    def render_menu(self):
        screen = pygame.display.set_mode((600, 400))
        screen.fill((30, 30, 30))

        font = pygame.font.SysFont("Arial", 28)

        options = [
            f"IA activée : {'Oui' if self.ai_enabled else 'Non'}",
            f"Couleur IA : {self.ai_color}",
            f"Niveau IA (profondeur) : {self.ai_depth}",
            "Lancer la partie"
        ]

        for i, text in enumerate(options):
            label = font.render(text, True, (200, 200, 200))
            screen.blit(label, (50, 80 + i * 60))

        pygame.display.update()


    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # IA activée
                if 80 <= y <= 120:
                    self.ai_enabled = not self.ai_enabled

                # Couleur IA
                elif 140 <= y <= 180:
                    self.ai_color = "white" if self.ai_color == "black" else "black"

                # Niveau IA
                elif 200 <= y <= 240:
                    self.ai_depth = (self.ai_depth % 4) + 1

                # Lancer la partie
                elif 260 <= y <= 300:
                    self.start_game()


    def start_game(self):
        # créer Main avec les paramètres IA
        self.main = Main(
            ai_enabled=self.ai_enabled,
            ai_color=self.ai_color,
            ai_depth=self.ai_depth
        )

        self.state = "game"



if __name__ == "__main__":
    App().run()
