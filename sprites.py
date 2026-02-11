import pygame as pg
from pygame.sprite import Sprite
from settings import *

vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        # TILESIZE as a multiplier for the game
        self.pos = vec(x,y) * TILESIZE
    
    def get_keys(self):
        # a vector to set velocity of player
        self.vel = vec(0,0)
        # gets key input from the user
        # wasd - up, left, down, right
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # if player is moving diagonally (both x and y movement does not equal zero)
        if self.vel.x != 0 and self.vel.y != 0:
            # sqrt 2 divided by 2 to represent diagonal movement
            self.vel *= 0.7071

    def update(self):
        self.get_keys()
        # sets new position
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        #self.rect.x += 1
        #if self.rect.x > WIDTH:
        #    self.rect.x -= 1

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(1,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = 5

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        if hits:
            print("collided")
            self.speed = 10
        
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.pos.y += TILESIZE
        self.pos += self.speed * self.vel
        self.rect.center = self.pos
        #self.pos -= self.game.player.pos *- self.game.dt
        #self.rect.center = self.pos
        # sets new position
        #self.pos += self.vel * self.game.dt

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        pass
            


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
    
    def update(self):
        pass
