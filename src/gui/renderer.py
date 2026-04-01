import pygame

class Renderer:

    @staticmethod
    def draw_rect(surface, color, rect, width=0):
        pygame.draw.rect(surface, color, rect, width)

    @staticmethod
    def draw_image(surface, image, rect):
        surface.blit(image, rect)

    @staticmethod
    def draw_text(surface, text, pos, font, color=(0, 0, 0)):
        label = font.render(text, True, color)
        surface.blit(label, pos)
