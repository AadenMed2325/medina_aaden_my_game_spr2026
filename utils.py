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


class Spritesheet:
    # convert the loaded file to something visible
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
   
    def get_image(self, x, y, width, height):
        # makes the image a physical surface
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        new_image = pg.transform.scale(image, (width, height))
        # set colorkey to make the black background transparent
        new_image.set_colorkey(BLACK)
        image = new_image
        return image


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


# displays health bar on the screen
# def draw_health_bar(surf, x, y, pct, color):
#     # if dead
#     if pct < 0:
#         pct = 0
#     HEALTH_LENGTH = WIDTH / 2
#     HEALTH_HEIGHT = TILESIZE
#     fill = (pct/100) * HEALTH_LENGTH
#     outline_rect = pg.Rect(x, y, HEALTH_LENGTH, HEALTH_HEIGHT)
#     fill_rect = (x, y, fill, HEALTH_HEIGHT)
#     pg.draw.rect(surf, color, fill_rect)
#     pg.draw.rect(surf, WHITE, outline_rect, 2)

