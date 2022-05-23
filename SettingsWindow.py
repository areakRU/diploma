from random import randint
from Classes.Button import ButtonImage
from Classes.Text import Text
from Classes.TextEdit import TextEdit
from Classes.KeyboardDriver import KeyboardDriver
from Classes.Circle import Circle
from Classes.Colors import Colors
from Classes.Db import Db
import pygame as pg
import bcrypt
import secrets
import psycopg2
from psycopg2.errors import UniqueViolation, InFailedSqlTransaction
import sys
import os

class SettingsWindow:
    def __init__(self, game_screen:pg.Surface, reload_game_screen:pg.Surface):
        self.colors = Colors().get_colors()
        self.keyboard_driver = KeyboardDriver()
        self.settings_screen = pg.display.set_mode((game_screen.get_size()[0], game_screen.get_size()[1]))
        self.game_screen = game_screen
        self.reload_game_screen = reload_game_screen
        self.settings_screen.fill((255,255,255))
        self.draw_level((5, 1))
        self.draw_ui()
        self.db = Db(os.environ['DB_DIPLOMA_NAME'], os.environ['DB_DIPLOMA_LOGIN'], os.environ['DB_DIPLOMA_PASSWORD'], 'localhost')
        self.run()


    def calculate_level_params(self, game_field_size, game_screen_indent, circle_radius):
        x_array = list()
        y_array = list()
        game_screen_center = (round((self.settings_screen.get_size()[0]-game_screen_indent[0])/2), round((self.settings_screen.get_size()[1]-game_screen_indent[1])/2))
        distance_between_circles = 3*circle_radius
        
        if game_field_size[0] % 2 == 1 and game_field_size[1] % 2 == 1:
            for i in range(game_field_size[0]):
                x = game_screen_center[0] + (i - (game_field_size[0] - 1)/2)*distance_between_circles
                x_array.append(x)
            for j in range(game_field_size[1]):
                y = game_screen_center[1] + (j - (game_field_size[1] - 1)/2)*distance_between_circles
                y_array.append(y)
        if game_field_size[0] % 2 != 1 and game_field_size[1] % 2 == 1:
            for i in range(game_field_size[0]):
                x = game_screen_center[0] - (game_field_size[0]/2)*distance_between_circles + distance_between_circles/2 + i*distance_between_circles
                x_array.append(x)
            for j in range(game_field_size[1]):
                y = game_screen_center[1] + (j - (game_field_size[1] - 1)/2)*distance_between_circles
                y_array.append(y)

        self.x_array = x_array
        self.y_array = y_array
        self.distance_between_circles = distance_between_circles
        return x_array, y_array


    def draw_level(self, game_field_size = (3,3), game_screen_indent = (0, 200), circle_radius = 20):
        self.circles = list()
        x_array, y_array = self.calculate_level_params(game_field_size=game_field_size, game_screen_indent=game_screen_indent, circle_radius=circle_radius)
        self.generate_graphic_password()
        for i in range(len(x_array)):
            self.circles.append(Circle(self.settings_screen, (x_array[i], y_array[0]), self.chosen_colors[i], circle_radius))


    def draw_ui(self):
        self.login = TextEdit(self.settings_screen, 'grey_button05.png', (self.settings_screen.get_rect().centerx, self.settings_screen.get_rect().height - 200), 'Login', 20, (0, 0, 0))
        self.login.draw_text_edit()
        self.password = TextEdit(self.settings_screen, 'grey_button05.png', (self.settings_screen.get_rect().centerx, self.settings_screen.get_rect().height - 150), 'Password', 20, (0, 0, 0))
        self.password.draw_text_edit()
        self.register_button = ButtonImage(self.settings_screen, 'grey_button05.png', (self.settings_screen.get_rect().centerx, self.settings_screen.get_rect().height - 100), 'Register', 20, (0, 0, 0))
        self.register_button.draw_button()
        self.back_button = ButtonImage(self.settings_screen, 'grey_button05.png', (self.settings_screen.get_rect().centerx, self.settings_screen.get_rect().height - 50), 'Back', 20, (0, 0, 0))
        self.back_button.draw_button()

        self.auth_text_result = Text(self.settings_screen, '', 20, '0x9bcf53', (self.login.get_textedit_rect().centerx, self.login.get_textedit_rect().midtop[1]-40))

        self.circle_buttons_up = list()
        self.circle_buttons_down = list()
        for i in range(len(self.x_array)):
            self.circle_buttons_up.append(ButtonImage(self.settings_screen, 'grey_arrowUpGrey.png', (self.x_array[i], self.circles[0].circle.midtop[1]-10), '', 0, (0,0,0)))
            self.circle_buttons_down.append(ButtonImage(self.settings_screen, 'grey_arrowDownGrey.png', (self.x_array[i], self.circles[0].circle.midbottom[1]+10), '', 0, (0,0,0)))
            self.circle_buttons_up[i].draw_button()
            self.circle_buttons_down[i].draw_button()
        

    def generate_graphic_password(self):
        self.chosen_colors = list()
        for cirle in range(len(self.x_array)):
            chosen_color = secrets.choice(self.colors)
            self.chosen_colors.append(chosen_color)


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

        if self.register_button.get_button_rect().collidepoint(cursor_pos) or self.register_button.get_text_rect().collidepoint(cursor_pos):
            login = self.login.get_textstring()
            password = str.encode(self.password.get_textstring())
            graphic_password = str.encode(''.join([str(circle.color) for circle in self.circles]))
            salt_password = bcrypt.gensalt()
            salt_graphic_password = bcrypt.gensalt()
            hash_password = bcrypt.hashpw(password, salt_password)
            hash_graphic_password = bcrypt.hashpw(graphic_password, salt_graphic_password)
            try:
                self.db.cursor.execute('INSERT INTO public."user" (login,password,graphic_password,salt_password,salt_graphic_password) VALUES (%s,%s,%s,%s,%s);', (login, hash_password.decode('utf8'), hash_graphic_password.decode('utf8'), salt_password.decode('utf8'), salt_graphic_password.decode('utf8')))
                self.db.conn.commit()
                self.auth_text_result.redraw_text('Successful registration.', '0x9bcf53')
            except UniqueViolation:
                self.db.conn.rollback()
                self.auth_text_result.redraw_text('The name is already exists.', '0xe25050')

        for id_button_up in range(len(self.circle_buttons_up)):
            if self.circle_buttons_up[id_button_up].get_button_rect().collidepoint(cursor_pos) or self.circle_buttons_up[id_button_up].get_text_rect().collidepoint(cursor_pos):
                id_color = self.colors.index(self.circles[id_button_up].color)
                if id_color + 1 < len(self.colors):
                    id_color = id_color + 1
                self.circles[id_button_up].redraw_circle(self.colors[id_color])
            if self.circle_buttons_down[id_button_up].get_button_rect().collidepoint(cursor_pos) or self.circle_buttons_down[id_button_up].get_text_rect().collidepoint(cursor_pos):
                id_color = self.colors.index(self.circles[id_button_up].color)
                if id_color - 1 >= 0:
                    id_color = id_color - 1
                self.circles[id_button_up].redraw_circle(self.colors[id_color])
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