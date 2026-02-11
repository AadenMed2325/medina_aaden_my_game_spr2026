# game engine
# I can push from vs code...
# collision should be detected within an update of a Sprite
# can't use "all sprites"
# logical separation of elements, parse what's colliding with what.

# pseudo code - collision
# instantiate the green goal first as a sprite

# polymorphism - many forms
# ability of same function, method, or operator to work in different ways
# depending on object/data type
'''
Main file responsible for game loop including input, update, and draw methods.

'''

import pygame as pg
import sys
# operating system - windows on our computer, bridge to basic funtions
from os import path
# * = wildcard, imports everything
from settings import *
from sprites import *
from utils import *


# the game class that will be instantiated in order to run the game
# Game is a blueprint for what the code has
class Game:
    def __init__(self):
        # pygame is referred to as pg
        pg.init()
        # setting up pygame screen using tuple value for width height
        # placeholder/variable for any instance of the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # convention for Classes is Capital
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.game_cooldown = Cooldown(5000)
    
    # a method is a function tied to a Class

    def load_data(self):
        # accesses the game directory
        self.game_dir = path.dirname(__file__)
        # instantiating the object
        self.map = Map(path.join(self.game_dir, 'level1.txt'))
        print('data is loaded')

    def new(self):
        self.load_data()
        # container class for many sprites
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        #self.player = Player(self, 15, 15)
        # self = the game in this part of the code
        #self.mob = Mob(self, 4, 4)
        #self.wall = Wall(self, WIDTH/2/TILESIZE, HEIGHT/2/TILESIZE)
        
        # loaded map data
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    # object still exists without a name
                    # call class constructor without assigning variable...when
                    Wall(self, col, row)
                if tile == 'P':
                    # self in this part of the game
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        self.run()

    def run(self):
        # while the game is running
        while self.running:
            # self.dt helps with the position of the player
            self.dt = self.clock.tick(FPS) / 1000

            self.events()
            self.update()
            self.draw()

    def events(self):
        # events are stuff that happens with peripherals
        # peripherals - keyboard, mouse, touch screen, controller, microphone, joystick, VR headset
        # event iterates through each item in a group
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                print("I can get mouse input")
            if event.type == pg.KEYUP:
                if event.key == pg.K_k:
                    print("I can determine when keys are released")


    def quit(self):
        pass

    # updates the self.all_sprites group
    def update(self):
        self.all_sprites.update()
    
    # this method uses draw_text to draw text and display it
    def draw(self):
        self.screen.fill(BLUE)
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT - TILESIZE * 3)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    # this method draws text in the game
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


# instantiating the game
if __name__ == "__main__":
    g = Game()

# while the game is running, a new instance of game will run
while g.running:
    g.new()

pg.quit()