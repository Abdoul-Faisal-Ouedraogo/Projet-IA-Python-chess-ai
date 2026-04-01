import pygame

from src.config.const import *


class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    # -------------------------
    #   AFFICHAGE DU DRAG
    # -------------------------

    def update_blit(self, surface):
        # texture haute résolution pendant le drag
        self.piece.set_texture(size=128)
        img = pygame.image.load(self.piece.texture)

        # position centrée sur la souris
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)

        surface.blit(img, self.piece.texture_rect)

    # -------------------------
    #   GESTION DE LA SOURIS
    # -------------------------

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        # ignorer la zone d’interface
        if pos[1] < TOP_UI:
            return

        self.initial_row = (pos[1] - TOP_UI) // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    # -------------------------
    #   DRAG & DROP
    # -------------------------

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
