from Classes.Circle import Circle

class SingInData:
    def __init__(self):
        self.login = None
        self.password = None
        self.graphic_password = list()


    def set_login(self, login:str):
        self.login = login


    def set_password(self, password:str):
        self.password = password


    def add_to_graphic_password(self, circle:Circle):
        self.graphic_password.append(circle)


    def delete_part_of_graphic_password(self, circle:Circle):
        for idx_circle in range(len(self.graphic_password)):
            if self.graphic_password[idx_circle].circle.center == circle.circle.center:
                del self.graphic_password[idx_circle]
                break


    def get_graphic_password(self):
        prepared_graphic_password = [str(circle.previous_color) for circle in self.graphic_password]
        return ''.join(prepared_graphic_password)