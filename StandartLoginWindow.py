from Classes.Button import ButtonImage
from Classes.TextEdit import TextEdit
from Classes.KeyboardDriver import KeyboardDriver
from Classes.Circle import Circle
from Classes.Colors import Colors
from Classes.Text import Text
from Classes.Db import Db
import pygame as pg
import bcrypt
import psycopg2
import sys
import os

class StandartLoginWindow:
    def __init__(self, game_screen:pg.Surface, reload_game_screen:pg.Surface):
        self.keyboard_driver = KeyboardDriver()
        self.standart_login_screen = pg.display.set_mode((game_screen.get_size()[0], game_screen.get_size()[1]))
        self.game_screen = game_screen
        self.reload_game_screen = reload_game_screen
        self.standart_login_screen.fill((255,255,255))
        self.draw_ui()
        self.db = Db(os.environ['DB_DIPLOMA_NAME'], os.environ['DB_DIPLOMA_LOGIN'], os.environ['DB_DIPLOMA_PASSWORD'], 'localhost')
        self.run()


    def draw_ui(self):
        self.auth_text_result = Text(self.standart_login_screen, '', 20, '0x9bcf53', (self.standart_login_screen.get_rect().centerx, self.standart_login_screen.get_rect().height - 250))
        self.login = TextEdit(self.standart_login_screen, 'grey_button05.png', (self.standart_login_screen.get_rect().centerx, self.standart_login_screen.get_rect().height - 200), 'Login', 20, (0, 0, 0))
        self.login.draw_text_edit()
        self.password = TextEdit(self.standart_login_screen, 'grey_button05.png', (self.standart_login_screen.get_rect().centerx, self.standart_login_screen.get_rect().height - 150), 'Password', 20, (0, 0, 0))
        self.password.draw_text_edit()
        self.sign_in_button = ButtonImage(self.standart_login_screen, 'grey_button05.png', (self.standart_login_screen.get_rect().centerx, self.standart_login_screen.get_rect().height - 100), 'Sign In', 20, (0, 0, 0))
        self.sign_in_button.draw_button()
        self.back_button = ButtonImage(self.standart_login_screen, 'grey_button05.png', (self.standart_login_screen.get_rect().centerx, self.standart_login_screen.get_rect().height - 50), 'Back', 20, (0, 0, 0))
        self.back_button.draw_button()


    def handle_mouse_button_down(self):
        cursor_pos = pg.mouse.get_pos()
        if self.login.get_textedit_rect().collidepoint(cursor_pos) or self.login.get_text_rect().collidepoint(cursor_pos):
            self.login.set_edit(True)
        else:
            self.login.set_edit(False)

        if self.password.get_textedit_rect().collidepoint(cursor_pos) or self.password.get_text_rect().collidepoint(cursor_pos):
            self.password.set_edit(True)
        else:
            self.password.set_edit(False)

        if self.back_button.get_button_rect().collidepoint(cursor_pos) or self.back_button.get_text_rect().collidepoint(cursor_pos):
            self.game_screen.blit(self.reload_game_screen, self.reload_game_screen.get_rect().topleft)
            return -1

        if self.sign_in_button.get_button_rect().collidepoint(cursor_pos) or self.sign_in_button.get_text_rect().collidepoint(cursor_pos):
            login = self.login.get_textstring()
            password = str.encode(self.password.get_textstring())
            self.db.cursor.execute('SELECT password, salt_password FROM public."user" WHERE login = %s;', (login, ))
            user_data = self.db.cursor.fetchall()
            if len(user_data) > 0:
                db_password, db_salt = user_data[0]
                password_hashed = bcrypt.hashpw(password, str.encode(db_salt))
                if db_password == password_hashed.decode('utf8'):
                    self.auth_text_result.redraw_text('Authentication completed.', '0x9bcf53')
                else:
                    self.auth_text_result.redraw_text('Authentication error. Enter correct login or password.', '0xe25050')
            else:
                self.auth_text_result.redraw_text('Authentication error. Enter correct login or password.', '0xe25050')
        return None


    def edit_text_edit(self, char:str, text_edit:TextEdit):
        text_string = text_edit.get_textstring()
        if char == 'delete' and len(text_string) > 0:
            text_string = text_string[:-1]
            text_edit.set_textstring(text_string)
        if char != 'delete':
            text_string = text_string + char
            text_edit.set_textstring(text_string)


    def run(self):
        active = True
        while active:
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.handle_mouse_button_down() == -1:
                        active = False
                if (event.type == pg.KEYDOWN or event.type == pg.KEYUP) and self.login.get_edit():
                    char = self.keyboard_driver.get_char(event)
                    if char != None:
                        self.edit_text_edit(char, self.login)
                if (event.type == pg.KEYDOWN or event.type == pg.KEYUP) and self.password.get_edit():
                    char = self.keyboard_driver.get_char(event)
                    if char != None:
                        self.edit_text_edit(char, self.password)