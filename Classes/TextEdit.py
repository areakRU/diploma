import pygame as pg
import os

class TextEdit:
    def __init__(self, surface:pg.Surface, IMAGE_NAME:str,center:tuple, text_string:str, text_size:int, text_color:tuple):
        self.surface = surface
        self.center = center
        self.text_string = text_string
        self.text_size = text_size
        self.text_color = text_color
        self.IMAGE_NAME = IMAGE_NAME
        self.EDIT = False
        self.FONT_PATH = self.get_font_path()
        self.TEXT_EDIT_PATH = self.get_text_edit_path()
        self.text_edit = None
        self.text_edit_rect = None
        self.text = None
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


    def get_text_edit_path(self):
        TEXT_EDIT_PATH = os.path.abspath(__file__)
        TEXT_EDIT_PATH = os.path.split(TEXT_EDIT_PATH)[0]
        TEXT_EDIT_PATH = TEXT_EDIT_PATH.split('\\')[0:-1]
        TEXT_EDIT_PATH = "\\".join(TEXT_EDIT_PATH) + '\\Graphics\\' + self.IMAGE_NAME

        if not os.path.exists(TEXT_EDIT_PATH):
            os.mkdir(TEXT_EDIT_PATH)

        return TEXT_EDIT_PATH


    def draw_text_edit(self):
        self.text_edit = pg.image.load(self.TEXT_EDIT_PATH)
        self.text_edit_rect = self.text_edit.get_rect()
        self.text_edit_rect.center = self.center

        self.font = pg.font.Font(self.FONT_PATH, self.text_size)
        self.text = self.font.render(self.text_string, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.center

        pg.draw.rect(self.surface, (255,255,255), self.text_rect)
        self.surface.blit(self.text_edit, self.text_edit_rect.topleft)
        self.surface.blit(self.text, self.text_rect.topleft)


    def get_textstring(self):
        return self.text_string


    def get_text_rect(self):
        return self.text_rect


    def get_textedit_rect(self):
        return self.text_edit_rect


    def set_textstring(self, text_string):
        text_string_temp = text_string        
        
        text_temp = self.font.render(text_string_temp, True, self.text_color)
        text_temp_rect = text_temp.get_rect()
        text_temp_rect.center = self.center

        if text_temp_rect.width < self.text_edit_rect.width:
            pg.draw.rect(self.surface, (255,255,255), self.text_rect)
            self.text_string = text_string
            self.text = self.font.render(self.text_string, True, self.text_color)
            self.text_rect = self.text.get_rect()
            self.text_rect.center = self.center
            self.surface.blit(self.text_edit, self.text_edit_rect.topleft)
            self.surface.blit(self.text, self.text_rect.topleft)

        print(self.text_string)

    
    def set_edit(self, EDIT:bool):
        self.EDIT = EDIT


    def get_edit(self):
        return self.EDIT