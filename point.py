import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def generate_offsets(self):
        x_min = -100
        x_max = 100
        y_min = -100
        y_max = 100


        if(self.x < -4900):
            x_min = (5000-self.x)*-1
        if(self.x > 4900):
            x_max = 5000-self.x;

        if(self.y < -4900):
            y_min = (5000-self.y)*-1
        if(self.y > 4900):
            y_max = 5000-self.y;

        self.x_offset = random.randrange(x_min,x_max)
        self.y_offset = random.randrange(y_min,y_max)

        self.x = self.x + self.x_offset
        self.y = self.y + self.y_offset

    def get_code(self):
        return str(self.x) + ":"+str(self.y)

    def get_x(self):
        return self.x + self.x_offset

    def get_y(self):
        return self.y + self.y_offset
        