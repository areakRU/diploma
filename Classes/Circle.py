import pygame as pg
import os

class Circle:
    def __init__(self, surface:pg.Surface, center:tuple, color, radius:int):
        self.surface = surface
        self.center = center
        self.color = color
        self.previous_color = color
        self.radius = radius
        self.circle = None
        self.circle_filling = None
        self.draw_circle()


    def draw_circle(self):
        self.circle_filling = pg.draw.circle(self.surface, self.color, self.center, self.radius)
        self.circle = pg.draw.circle(self.surface, (130,130,130), self.center, self.radius, width=3)


    def redraw_circle(self, color):
        self.previous_color = self.color
        self.color = color
        self.circle_filling = pg.draw.circle(self.surface, color, self.center, self.radius)
        self.circle = pg.draw.circle(self.surface, (130,130,130), self.center, self.radius, width=3)