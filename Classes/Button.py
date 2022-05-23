import pygame as pg
import os

class ButtonImage:
    def __init__(self, surface:pg.Surface, IMAGE_NAME:str, center:tuple, text:str, text_size:int, text_color:tuple):
        self.surface = surface
        self.center = center
        self.text_size = text_size
        self.text_color = text_color
        self.IMAGE_NAME = IMAGE_NAME
        self.FONT_PATH = self.get_font_path()
        self.BUTTON_PATH = self.get_button_path()
        self.button = None
        self.button_rect = None
        self.text = text
        self.text_rect = None
        self.font = None


    def get_font_path(self):
        FONT_PATH = os.path.abspath(__file__)
        FONT_PATH = os.path.split(FONT_PATH)[0]
        FONT_PATH = FONT_PATH.split('\\')[0:-1]
        FONT_PATH = "\\".join(FONT_PATH) + '\\Fonts\\Dihjauti-Regular.otf'

        if not os.path.exists(FONT_PATH):
            os.mkdir(FONT_PATH)

        return FONT_PATH


    def get_button_path(self):
        BUTTON_PATH = os.path.abspath(__file__)
        BUTTON_PATH = os.path.split(BUTTON_PATH)[0]
        BUTTON_PATH = BUTTON_PATH.split('\\')[0:-1]
        BUTTON_PATH = "\\".join(BUTTON_PATH) + '\\Graphics\\' + self.IMAGE_NAME

        if not os.path.exists(BUTTON_PATH):
            os.mkdir(BUTTON_PATH)

        return BUTTON_PATH


    def draw_button(self):
        self.button = pg.image.load(self.BUTTON_PATH)
        self.button_rect = self.button.get_rect()
        self.button_rect.center = self.center
        self.surface.blit(self.button, self.button_rect.topleft)

        self.font = pg.font.Font(self.FONT_PATH, self.text_size)
        self.text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.center
        self.surface.blit(self.text, self.text_rect.topleft)


    def get_text_rect(self):
        return self.text_rect

    
    def get_button_rect(self):
        return self.button_rect