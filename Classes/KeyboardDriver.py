import pygame as pg

class KeyboardDriver:
    def __init__(self):
        self.shift_pressed = False
        self.char = None
    

    def get_char(self, event:pg.event.Event):
        self.char = None
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_0:
                self.char = '0'
            elif event.key == pg.K_1:
                self.char = '1'
            elif event.key == pg.K_2:
                self.char = '2'
            elif event.key == pg.K_3:
                self.char = '3'
            elif event.key == pg.K_4:
                self.char = '4'
            elif event.key == pg.K_5:
                self.char = '5'
            elif event.key == pg.K_6:
                self.char = '6'
            elif event.key == pg.K_7:
                self.char = '7'
            elif event.key == pg.K_8:
                self.char = '8'
            elif event.key == pg.K_9:
                self.char = '9'
            elif event.key == pg.K_a:
                self.char = 'a'
            elif event.key == pg.K_b:
                self.char = 'b'
            elif event.key == pg.K_c:
                self.char = 'c'
            elif event.key == pg.K_d:
                self.char = 'd'
            elif event.key == pg.K_e:
                self.char = 'e'
            elif event.key == pg.K_f:
                self.char = 'f'
            elif event.key == pg.K_g:
                self.char = 'g'
            elif event.key == pg.K_h:
                self.char = 'h'
            elif event.key == pg.K_i:
                self.char = 'i'
            elif event.key == pg.K_j:
                self.char = 'j'
            elif event.key == pg.K_k:
                self.char = 'k'
            elif event.key == pg.K_l:
                self.char = 'l'
            elif event.key == pg.K_m:
                self.char = 'm'
            elif event.key == pg.K_n:
                self.char = 'n'
            elif event.key == pg.K_o:
                self.char = 'o'
            elif event.key == pg.K_p:
                self.char = 'p'
            elif event.key == pg.K_q:
                self.char = 'q'
            elif event.key == pg.K_r:
                self.char = 'r'
            elif event.key == pg.K_s:
                self.char = 's'
            elif event.key == pg.K_t:
                self.char = 't'
            elif event.key == pg.K_u:
                self.char = 'u'
            elif event.key == pg.K_v:
                self.char = 'v'
            elif event.key == pg.K_w:
                self.char = 'w'
            elif event.key == pg.K_x:
                self.char = 'x'
            elif event.key == pg.K_y:
                self.char = 'y'
            elif event.key == pg.K_z:
                self.char = 'z'
            elif event.key == pg.K_LSHIFT:
                self.shift_pressed = True
            elif event.key == pg.K_BACKSPACE:
                self.char = 'delete'
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LSHIFT:
                self.shift_pressed = False
            
        if self.shift_pressed and self.char != None:
            self.char = str.capitalize(self.char)

        return self.char