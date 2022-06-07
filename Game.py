import matplotlib
import pygame as pg
import sys
import numpy as np
import os
from Classes.EmgDriver import EmgDriver
from Classes.Filter import Filter
from Classes.Cutter import Cutter
from Classes.NeuralNetwork import Network
from Classes.Button import ButtonImage
from Classes.KeyboardDriver import KeyboardDriver
from Classes.TextEdit import TextEdit
from SettingsWindow import SettingsWindow
from Classes.Circle import Circle
from Classes.Colors import Colors
from Classes.SingInData import SingInData
from StandartLoginWindow import StandartLoginWindow
from Classes.Text import Text
from Classes.Db import Db
import matplotlib.pyplot as plt
import bcrypt
from secrets import choice
import time

class Game:
    def __init__(self, screen_width, screen_height):
        pg.init()
        self.is_game_started = False
        self.colors = Colors().get_colors()
        self.networks = list()
        self.init_networks()
        self.keyboard_driver = KeyboardDriver()
        self.sing_in_data = SingInData()
        self.db = Db(os.environ['DB_DIPLOMA_NAME'], os.environ['DB_DIPLOMA_LOGIN'], os.environ['DB_DIPLOMA_PASSWORD'], 'localhost')
        self.screen = pg.display.set_mode((screen_width,screen_height))
        self.screen.fill((255,255,255))
        self.draw_ui()
        self.draw_level((5,5))
        self.run()


    def init_networks(self):
        self.networks.append(Network('NeuralNetwork\model_1.hdf5'))
        self.networks.append(Network('NeuralNetwork\model_2.hdf5'))
        self.networks.append(Network('NeuralNetwork\model_3.hdf5'))
        self.networks.append(Network('NeuralNetwork\model_4.hdf5'))
        self.networks.append(Network('NeuralNetwork\model_5.hdf5'))
        self.networks.append(Network('NeuralNetwork\model_6.hdf5'))
        self.networks.append(Network('NeuralNetwork\model_7.hdf5'))
        self.networks.append(Network('NeuralNetwork\model_8.hdf5'))


    def draw_ui(self, game_screen_indent = (0, 200)):
        standart_login_button_center = (self.screen.get_size()[0]/2, self.screen.get_rect().height - 50)
        self.standart_login_button = ButtonImage(self.screen, 'grey_button05.png', standart_login_button_center, 'Standart login', 20, (0, 0, 0))
        self.standart_login_button.draw_button()

        start_button_center = (self.screen.get_size()[0]/2, self.screen.get_rect().height - 100)
        self.start_button = ButtonImage(self.screen, 'grey_button05.png', start_button_center, 'Graphic login', 20, (0, 0, 0))
        self.start_button.draw_button()

        create_button_center = (self.screen.get_size()[0]/2, self.screen.get_rect().height - 150)
        self.create_button = ButtonImage(self.screen, 'grey_button05.png', create_button_center, 'Create account', 20, (0, 0, 0))
        self.create_button.draw_button()

        text_edit_center = (self.screen.get_size()[0]/2, self.screen.get_rect().height - 200)
        self.text_edit = TextEdit(self.screen, 'grey_button05.png', text_edit_center, 'Enter login', 20, (0, 0, 0))
        self.text_edit.draw_text_edit()

        refresh_button_center = (self.start_button.get_button_rect().midright[0]+20, self.start_button.get_button_rect().centery)
        self.refresh_button = ButtonImage(self.screen, 'refresh.png', refresh_button_center, '', 0, (0,0,0))
        self.refresh_button.draw_button()

        self.auth_text_result = self.auth_text_result = Text(self.screen, '', 20, '0x9bcf53', (text_edit_center[0], text_edit_center[1]-40))

        self.indicator_center = (self.start_button.get_button_rect().midleft[0]-20, self.screen.get_rect().height - 100)
        self.indicator = Circle(self.screen, self.indicator_center, 0xe25050, 15)


    def calculate_level_params(self, game_field_size, game_screen_indent, circle_radius):
        x_array = list()
        y_array = list()
        game_screen_center = (round((self.screen.get_size()[0]-game_screen_indent[0])/2), round((self.screen.get_size()[1]-game_screen_indent[1])/2))
        distance_between_circles = 3*circle_radius
        
        if game_field_size[0] % 2 == 1 and game_field_size[1] % 2 == 1:
            for i in range(game_field_size[0]):
                x = game_screen_center[0] + (i - (game_field_size[0] - 1)/2)*distance_between_circles
                x_array.append(x)
            for j in range(game_field_size[1]):
                y = game_screen_center[1] + (j - (game_field_size[1] - 1)/2)*distance_between_circles
                y_array.append(y)
        if game_field_size[0] % 2 == 1 and game_field_size[1] % 2 != 1:
            for i in range(game_field_size[0]):
                x = game_screen_center[0] + (i - (game_field_size[0] - 1)/2)*distance_between_circles
                x_array.append(x)
            for j in range(game_field_size[1]):
                y = game_screen_center[1] - (game_field_size[1]/2)*distance_between_circles + distance_between_circles/2 + j*distance_between_circles
                y_array.append(y)
        if game_field_size[0] % 2 != 1 and game_field_size[1] % 2 == 1:
            for i in range(game_field_size[0]):
                x = game_screen_center[0] - (game_field_size[0]/2)*distance_between_circles + distance_between_circles/2 + i*distance_between_circles
                x_array.append(x)
            for j in range(game_field_size[1]):
                y = game_screen_center[1] + (j - (game_field_size[1] - 1)/2)*distance_between_circles
                y_array.append(y)
        if game_field_size[0] % 2 != 1 and game_field_size[1] % 2 != 1:
            for i in range(game_field_size[0]):
                x = game_screen_center[0] - (game_field_size[0]/2)*distance_between_circles + distance_between_circles/2 + i*distance_between_circles
                x_array.append(x)
            for j in range(game_field_size[1]):
                y = game_screen_center[1] - (game_field_size[1]/2)*distance_between_circles + distance_between_circles/2 + j*distance_between_circles
                y_array.append(y)

        self.cursor_position = [x_array[0], y_array[0]]
        self.x_array = x_array
        self.y_array = y_array
        return x_array, y_array


    def draw_level(self, game_field_size = (3,3), game_screen_indent = (0, 200), circle_radius = 20):
        self.circles = list()
        x_array, y_array = self.calculate_level_params(game_field_size=game_field_size, game_screen_indent=game_screen_indent, circle_radius=circle_radius)
        for i in range(len(x_array)):
            circle_row = list()
            for j in range(len(y_array)):
                chosen_color = choice(self.colors)
                circle_row.append(Circle(self.screen, (x_array[i],y_array[j]), chosen_color, circle_radius))
            self.circles.append(circle_row)
        pg.draw.circle(self.screen, (130,130,130), (self.cursor_position[0], self.cursor_position[1]), 5)


    def redraw_level(self, movement_type : np.ndarray):
        id_x = 0
        id_y = 0

        for x in self.x_array:
            if self.cursor_position[0] == x:
                id_x = self.x_array.index(x)
                break
        for y in self.y_array:
            if self.cursor_position[1] == y:
                id_y = self.y_array.index(y)
                break

        if movement_type == 0:
            print('Влево')
            if id_x - 1 >= 0:
                if self.circles[id_x][id_y].color != (130,130,130):
                    self.circles[id_x][id_y].redraw_circle(self.circles[id_x][id_y].color)
                self.cursor_position[0] = self.x_array[id_x - 1]
                pg.draw.circle(self.screen, (130,130,130), (self.cursor_position[0], self.cursor_position[1]), 5)            
        elif movement_type == 1:
            if id_x + 1 < len(self.x_array):
                if self.circles[id_x][id_y].color != (130,130,130):
                    self.circles[id_x][id_y].redraw_circle(self.circles[id_x][id_y].color)
                self.cursor_position[0] = self.x_array[id_x + 1]
                pg.draw.circle(self.screen, (130,130,130), (self.cursor_position[0], self.cursor_position[1]), 5)  
            print('Вправо')
        elif movement_type == 2:
            if id_y - 1 >= 0:
                if self.circles[id_x][id_y].color != (130,130,130):
                    self.circles[id_x][id_y].redraw_circle(self.circles[id_x][id_y].color)
                self.cursor_position[1] = self.y_array[id_y - 1]
                pg.draw.circle(self.screen, (130,130,130), (self.cursor_position[0], self.cursor_position[1]), 5)
            print('Вверх')
        elif movement_type == 3:
            if id_y + 1 < len(self.y_array):
                if self.circles[id_x][id_y].color != (130,130,130):
                    self.circles[id_x][id_y].redraw_circle(self.circles[id_x][id_y].color)
                self.cursor_position[1] = self.y_array[id_y + 1]
                pg.draw.circle(self.screen, (130,130,130), (self.cursor_position[0], self.cursor_position[1]), 5)  
            print('Вниз')
        elif movement_type == 4:
            for circle_row in range(len(self.circles[0])):
                for circle_column in range(len(self.circles[1])):
                    if self.circles[circle_row][circle_column].center[0] == self.cursor_position[0] and self.circles[circle_row][circle_column].center[1] == self.cursor_position[1]:
                        if self.circles[circle_row][circle_column].color == (130,130,130):
                            self.sing_in_data.delete_part_of_graphic_password(self.circles[circle_row][circle_column])
                            self.circles[circle_row][circle_column].redraw_circle(self.circles[circle_row][circle_column].previous_color)
                        else:
                            self.sing_in_data.add_to_graphic_password(self.circles[circle_row][circle_column])
                            self.circles[circle_row][circle_column].redraw_circle((130,130,130))
                        pg.draw.circle(self.screen, (130,130,130), (self.cursor_position[0], self.cursor_position[1]), 5)
            print('Щелчок')
        elif movement_type == 5:
            self.is_game_started = False
            login = self.text_edit.get_textstring()
            graphic_password = str.encode(self.sing_in_data.get_graphic_password())
            self.db.cursor.execute('SELECT graphic_password, salt_graphic_password FROM public."user" WHERE login = %s', (login, ))
            user_data = self.db.cursor.fetchall()
            if len(user_data) > 0:
                db_graphic_password, db_salt = user_data[0]
                graphic_password_hashed = bcrypt.hashpw(graphic_password, str.encode(db_salt))
                if db_graphic_password == graphic_password_hashed.decode('utf8'):
                    self.auth_text_result.redraw_text('Authentication completed.', '0x9bcf53')
                else:
                    self.auth_text_result.redraw_text('Authentication error. Enter correct login or password.', '0xe25050')
            else:
                self.auth_text_result.redraw_text('Authentication error. Enter correct login or password.', '0xe25050')
            print('Схатить')
            self.sing_in_data = SingInData()
            self.circles.clear()
            self.draw_level((5,5))


    def get_new_prepared_signal(self):
        try:
            self.auth_text_result.redraw_text('', '0xe25050')
            driver = EmgDriver()
            data = driver.get_data(self.indicator)
            filter = Filter(data, 8)
            filtered_data = filter.filtfilt()
            cutter = Cutter(filtered_data, 2000, 15000, 350000)
            cut_filtered_data = cutter.cut_signal()
        except TimeoutError:
            self.is_game_started = False
            self.auth_text_result.redraw_text('Turn on the board.', '0xe25050')
            return np.array([])
        return cut_filtered_data


    def get_predicted_movement(self, signal):
        y_predicted = np.zeros(len(self.networks), dtype=int)
        for idx_prediction in range(len(self.networks)):
            y_predicted[idx_prediction] = self.networks[idx_prediction].predict_classes(signal)
        count_of_occurences = np.array([len(y_predicted[y_predicted==i]) for i in range(6)])
        return count_of_occurences.argmax()


    def handle_mouse_button_down(self):
        cursor_pos = pg.mouse.get_pos()
        if self.text_edit.get_text_rect().collidepoint(cursor_pos) or self.text_edit.get_textedit_rect().collidepoint(cursor_pos):
            self.text_edit.set_edit(True)
        else:
            self.text_edit.set_edit(False)
        if self.create_button.get_text_rect().collidepoint(cursor_pos) or self.create_button.get_button_rect().collidepoint(cursor_pos):
            settings_window = SettingsWindow(self.screen, pg.Surface.copy(self.screen))
        if self.standart_login_button.get_text_rect().collidepoint(cursor_pos) or self.standart_login_button.get_button_rect().collidepoint(cursor_pos):
            standart_login_window = StandartLoginWindow(self.screen, pg.Surface.copy(self.screen))
        if not self.is_game_started and (self.refresh_button.get_text_rect().collidepoint(cursor_pos) or self.refresh_button.get_button_rect().collidepoint(cursor_pos)):
            self.circles.clear()
            self.draw_level((5,5))
        if self.start_button.get_text_rect().collidepoint(cursor_pos) or self.start_button.get_button_rect().collidepoint(cursor_pos):
            self.is_game_started = True


    def edit_text_edit(self, char:str):
        text_string = self.text_edit.get_textstring()
        if char == 'delete' and len(text_string) > 0:
            text_string = text_string[:-1]
            self.text_edit.set_textstring(text_string)
        if char != 'delete':
            text_string = text_string + char
            self.text_edit.set_textstring(text_string)


    def run(self):
        while True:
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down()
                if (event.type == pg.KEYDOWN or event.type == pg.KEYUP) and self.text_edit.get_edit():
                    char = self.keyboard_driver.get_char(event)
                    if char != None:
                        self.edit_text_edit(char)
            if self.is_game_started:
                emg_signal = self.get_new_prepared_signal()
                if emg_signal.size != 0:
                    predicted_movement = self.get_predicted_movement(emg_signal[0])
                    self.redraw_level(predicted_movement)
                elif emg_signal.size == 0 and self.is_game_started:
                    self.auth_text_result.redraw_text('Please, repeat movement. The movement wasn\'t clear.', '0xe25050')


if __name__ == '__main__':
    game = Game(800,600)