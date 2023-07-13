import numpy as np

class Robot(object):
    def __init__(self):
        self.act2cost = {(-1,0):1, (0,1):2, (0,-1):2, (1,0):3}

    def take_action(self, loc, action):
        x, y = loc
        x += action[0];  y += action[1]
        return (x,y)



