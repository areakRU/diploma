import pygame as pg
import os

class Text:
    def __init__(self, surface: pg.Surface, text: str, font_size: int, color, center: tuple):
        self.FONT_PATH = self.get_font_path()
        self.surface = surface
        self.string_text = text
        self.font_size = font_size
        self.color = color
        self.previous_color = color
        self.center = center
        self.draw_text()

    
    def get_font_path(self):
        FONT_PATH = os.path.abspath(__file__)
        FONT_PATH = os.path.split(FONT_PATH)[0]
        FONT_PATH = FONT_PATH.split('\\')[0:-1]
        FONT_PATH = "\\".join(FONT_PATH) + '\\Fonts\\Dihjauti-Regular.otf'

        if not os.path.exists(FONT_PATH):
            os.mkdir(FONT_PATH)

        return FONT_PATH


    def draw_text(self):
        self.font = pg.font.Font(self.FONT_PATH, self.font_size)
        self.text = self.font.render(self.string_text, True, self.color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.center
        self.surface.blit(self.text, self.text_rect.topleft)
        pg.display.update()


    def redraw_text(self, text: str, color):
        pg.draw.rect(self.surface, (255,255,255), self.text_rect)
        self.string_text = text
        self.previous_color = self.color
        self.color = color
        self.text = self.font.render(text, True, self.color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.center
        self.surface.blit(self.text, self.text_rect.topleft)
        pg.display.update()