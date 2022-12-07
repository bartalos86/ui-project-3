import random
import numpy as np

colors = ["#ff0000", "#00ff00", "#0000ff", "#ff00ff"]

class Point:
    def __init__(self, x, y, color = None):
        self.x = x
        self.y = y
        if color == None:
            self.color = random.choice(colors)
        else:
            self.color = color


    def generate_offsets(self, max_offset_distance = 100):
        x_min = -max_offset_distance
        x_max = max_offset_distance
        y_min = -max_offset_distance
        y_max = max_offset_distance


        if(self.x < (-5000 + max_offset_distance)):
            x_min = (5000+self.x)*-1
        if(self.x > (5000 - max_offset_distance)):
            x_max = 5000-self.x;

        if(self.y < (-5000 + max_offset_distance)):
            y_min = (5000+self.y)*-1
        if(self.y > (5000-max_offset_distance)):
            y_max = 5000-self.y;

        self.x_offset = random.randrange(x_min,x_max)
        self.y_offset = random.randrange(y_min,y_max)

        self.x = self.x + self.x_offset
        self.y = self.y + self.y_offset

        # if self.x < -5000 or self.x > 5000 or self.y < -5000 or self.y > 5000:
        #     print(f"self.x: {self.x} self.y: {self.y}")

    def get_code(self):
        return str(self.x) + ":"+str(self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_color(self):
        return self.color
    def set_color(self, color):
        self.color = color
        