import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        # creating the data for building the map using a list
        self.data = []
        
        # open a file, closing it with 'with'
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        
        # 
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE



# this class creates a countdown timer for a cooldown
class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        # allows us to set property for time until cooldown
        self.time = time
    def start(self):
        # returns the number of milliseconds since py.game __init__
        self.start_time = pg.time.get_ticks()
        # ready constantly checks if set time has ticked down to 0
    def ready(self):
        # sets current time to amount of ticks
        current_time = pg.time.get_ticks()
        # if the difference between current and start time are greater than self.time, then display
        # current time is the time that has passed
        # self.start_time - time since an exact object or process was initialized
        # self.time is the duration limit of the object or process
        # return True
        if current_time - self.start_time >= self.time:
            return True
        return False