import pygame as pg


WIDTH = 1024
HEIGHT = 768
TITLE = "My cool game..."
FPS = 60
TILESIZE = 32


# player values
PLAYER_SPEED = 280
CONTENDER_SPEED = 280
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE - 5, TILESIZE - 5)
CONTENDER_HIT_RECT = pg.Rect(0, 0, TILESIZE - 5, TILESIZE - 5)

# color values

# tuples storing RGB values
BLUE = (0, 0, 255)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
IVORY = (255, 248, 201)