from ctypes import Array
import pygame as pg
from pygame.sprite import Sprite
from player_states import *
from settings import *
from utils import *
from os import path
from state_machine import *
from weapons import *


vec = pg.math.Vector2


#now = pg.time.get_ticks()
# collision function - checks for collision between two entities
# accessible among many sprites
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

def get_health(self, group):
        hits = pg.sprite.spritecollide(self, group, False, collide_hit_rect)
        if hits:
            print('damage done')
            self.health = self.health - len(hits)

#Chat GPT helped me with this, I prompted it to help me turn rects into circles
def draw_circle(sprite, color):
    sprite.image.fill((0, 0, 0, 0))
    pg.draw.circle(sprite.image, color, (TILESIZE // 2, TILESIZE // 2,), TILESIZE// 2)


# function for colliding with walls
# leverages power of hit rect
# checks for vertical/horizontal collision in order
# sets position based on collision direction
def collide_and_freeze(sprite, group, dir):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits and not sprite.frozen:
        print("frozen")
        sprite.frozen = True
        sprite.freeze_time = pg.time.get_ticks()
    if hits:
        if dir == 'x':
            # right is positive velocity
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 1.7
            # left is negative velocity
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 1.7
            sprite.vel.x = 0
            #sprite.image.fill(WHITE)
            sprite.hit_rect.centerx = sprite.pos.x


        if dir == 'y':
            if hits[0].rect.centery > sprite.hit_rect.centery:  # moving down
                # center of rec is half of the square higher than collision point
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 1.7
            if hits[0].rect.centery < sprite.hit_rect.centery:  # moving up
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 1.7
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def immobilized_state(sprite, group):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits and not sprite.frozen:
        print("frozen")
        group.frozen = True
        group.freeze_time = pg.time.get_ticks()


def collide_with_stuff(sprite, group, dir):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if dir == 'x':
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 1.7
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 1.7
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x


        if dir == 'y':
            if hits[0].rect.centery > sprite.hit_rect.centery:  
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 1.7
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 1.7
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


def block_lose_health(sprite, group):
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        sprite.health = sprite.health - hits
# def hit_state(sprite, group):
#     print('hit state running')
#     hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
#     # if player gets attacked
#     if hits and not sprite.frozen:
#         print("i got hit!")
#         # changes the state
#         sprite.frozen = True
#         sprite.freeze_time = pg.time.get_ticks()


def freeze_timing(sprite):
    #print('freeze timer running')
    if sprite.frozen:
        #print('freezing active')
        current_time = pg.time.get_ticks()
        if current_time - sprite.freeze_time < 3000:
            sprite.vel.x = 0
            sprite.vel.y = 0
            draw_circle(sprite, WHITE)
        # counts the time the sprite is frozen
        else:
            print('back to normal')
            sprite.frozen = False
            sprite.freeze_time = 0
            draw_circle(sprite, sprite.default_color)
        # designate correct color


# player class to instantiate Player class
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_players
        Sprite.__init__(self, self.groups)
        self.game = game
        # imports the spritesheet
        #self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        #self.load_images()
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image = self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)


        #self.image.set_colorkey(BLACK)
        self.default_color = RED
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
        draw_circle(self, self.default_color)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        # TILESIZE as a multiplier for the game
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        # player is not walking/jumping in the start
        self.jumping = False
        self.moving = False
        self.frozen = False
        self.freeze_time = 0
        self.freeze_duration = 3000
        # default update and first frame = 0
        self.last_update = 0
        self.current_frame = 0
        # instantiating state machines and the states from state_machine and player_states
        #self.state_machine = StateMachine()
        #self.states: Array[State] = [PlayerIdleState(self), PlayerMoveState(self)]
        #self.state_machine.start_machine(self.states)
   
    def get_keys(self):
        if self.frozen:
            self.vel = vec(0,0)
            return
        # a vector to set velocity of player
        self.vel = vec(0,0)
        # gets key input from the user
        # wasd - up, left, down, right
        keys = pg.key.get_pressed()
        if keys[pg.K_f]:
            print('I fired a projectile')
            p = Projectile(self.game, self.rect.x, self.rect.y)
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
   


       
        # press f to fire a projectile
        # if keys[pg.K_f]:
        #     print('fired a projectile')
        #     p = Projectile(self.game, self.rect.x, self.rect.y)
   
    # loads sprite & images
    #def load_images(self):
        # two states- green & red
        #self.standing_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
                                #self.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE)]
        #self.moving_frames = [self.spritesheet.get_image(TILESIZE*2, 0, TILESIZE, TILESIZE),
                              #self.spritesheet.get_image(TILESIZE*3, 0, TILESIZE, TILESIZE)]
        # edits out the set color, background black
        #for frame in self.standing_frames:
            #frame.set_colorkey(BLACK)
        #for frame in self.moving_frames:
            #frame.set_colorkey(BLACK)
   
    # gets time as it loops
    # def animate(self):
    #     now = pg.time.get_ticks()
    #     if not self.jumping and not self.moving:
    #         if now - self.last_update > 350:
    #             self.last_update = now
    #             # goes through all frame numbers, alternates based on odd/even (modulus)
    #             self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #             bottom = self.rect.bottom
    #             self.image = self.standing_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom
    #     elif self.moving:
    #         if now - self.last_update > 350:
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
    #             bottom = self.rect.bottom
    #             self.image = self.moving_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom
   
    # # checks whether Player is moving or not
    # def state_check(self):
    #     if self.vel != vec(0, 0):
    #         self.state_machine.transition('move')
    #         self.moving = True
    #     else:
    #         self.state_machine.transition('idle')
    #         self.moving = False


    # how to collide with anything based on player
    # def collide_with_stuff(self, group, kill):
    #     hits = pg.sprite.spritecollide(self, group, kill)
    #     if hits:
    #         # get first hit, give me the string value of the name of its clas
    #         if str(hits[0].__class__.__name__) == "Mob":
    #             print("I collided with a mob")
    #         if str(hits[0].__class__.__name__) == "Contender":
    #             print("I collided with my opponent")
    #         if str(hits[0].__class__.__name__) == "Coin":
    #             print("I collided with a coin")


    def update(self):
        # if self.frozen:
        #     self.vec = vec(0,0)
        #     if now - self.freeze_time > self.freeze_duration:
        #         self.frozen = False
        #         self.image.fill(PURPLE)
        self.get_keys()
        #self.state_machine.update()
        #self.animate()
        #self.state_check()
        # sets new position
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        #self.collide_with_stuff(self.game.all_mobs, True)
        #self.collide_with_stuff(self.game.all_players, True)
        #self.collide_with_stuff(self.game.all_blocks, True)
        self.hit_rect.centerx = self.pos.x
        collide_and_collect(self, self.game.all_coins)
        collide_with_stuff(self, self.game.all_walls, 'x')
        collide_with_stuff(self, self.game.all_blocks, 'x')
        collide_and_freeze(self, self.game.all_contenders, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_stuff(self, self.game.all_walls, 'y')
        collide_with_stuff(self, self.game.all_blocks, 'y')
        collide_and_freeze(self, self.game.all_contenders, 'y')
        self.rect.center = self.hit_rect.center
        #immobilized_state(self, self.game.all_blocks)
        # hit_state(self, self.game.all_walls)
        # hit_state(self, self.game.all_walls)
        freeze_timing(self)


class Contender(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_contenders
        Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        self.default_color = BLUE
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
        draw_circle(self, self.default_color)
        #self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        # TILESIZE as a multiplier for the game
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = CONTENDER_HIT_RECT
        # player is not walking/jumping in the start
        self.jumping = False
        self.moving = False
        self.frozen = False
        self.freeze_time = 0
        self.freeze_duration = 3000
        # default update and first frame = 0
        self.last_update = 0
        self.current_frame = 0
   
    def get_keys(self):
        if self.frozen:
            self.vel = vec(0,0)
            return
        # a vector to set velocity of player
        self.vel = vec(0,0)
        # gets key input from the user
        # wasd - up, left, down, right
        keys = pg.key.get_pressed()
        if keys[pg.K_j]:
            self.vel.x = -CONTENDER_SPEED
        if keys[pg.K_l]:
            self.vel.x = CONTENDER_SPEED
        if keys[pg.K_i]:
            self.vel.y = -CONTENDER_SPEED
        if keys[pg.K_k]:
            self.vel.y = CONTENDER_SPEED
        # if player is moving diagonally (both x and y movement does not equal zero)
        if self.vel.x != 0 and self.vel.y != 0:
            # sqrt 2 divided by 2 to represent diagonal movement
            self.vel *= 0.7071
       
    def update(self):
        self.get_keys()
        # sets new position
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_stuff(self, self.game.all_walls, 'x')
        collide_with_stuff(self, self.game.all_blocks, 'x')
        #collide_with_stuff(self, self.game.all_coins, 'x')
        collide_and_freeze(self, self.game.all_players, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_stuff(self, self.game.all_walls, 'y')
        collide_with_stuff(self, self.game.all_blocks, 'y')
        collide_and_collect(self, self.game.all_coins)
        #collide_with_stuff(self, self.game.all_coins, 'y')
        collide_and_freeze(self, self.game.all_players, 'y')
        self.rect.center = self.hit_rect.center
        immobilized_state(self, self.game.all_walls)
        # hit_state(self, self.game.all_walls)
        # hit_state(self, self.game.all_walls)
        freeze_timing(self)






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
        self.image = game.wall_img
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        pass
           
class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = 5
        print('im a real projectile... ')


    def update(self):
        pass
        #hits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        #print(hits)
        #self.pos += self.speed * self.vel
        #self.rect.center = self.pos


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.type = 'None'
        #self.weapon_color = IVORY
        #self.image.fill(YELLOW)
        #self.weapon_attempt = 0
        self.has_weapon = False
        self.active = True
        self.respawn_time = 10000
        # amount of time the weapon will stay
        self.weapon_duration = 0
        # for the cooldown timer to check every second
        self.seconds = 0
        self.cool_down = 0
        self.collect_time = 0
        #self.collection_cooldown = 0
        # ChatGPT helped me with SRCALPHA, I asked it how to turn the sprites from a square
        # to a circle
        self.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
        draw_circle(self, GRAY)
        # if not self.has_weapon:
        #     self.image.fill(GRAY)
        self.hit_rect = WEAPON_HIT_RECT
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        #spawn_timing(self)
        #if self.has_weapon:
            #choose_weapon(self)    
    # GPT helped me with this, I wanted to know how to allow the Coin/Weapon to respawn
    # after the Player collected it
    def collect(self):
        self.active = False
        self.collect_time = pg.time.get_ticks() 
        # this makes the image transparent from 0-255  
        self.image.set_alpha(0)

    def update(self):
        now = pg.time.get_ticks()
        if not self.active:
            if now - self.collect_time > self.respawn_time:
                self.active = True
                # make the image not transparent
                self.image.set_alpha(255)

        if self.active:
            weapon_spawn(self)
            collide_with_stuff(self, self.game.all_blocks, 'x')
            collide_with_stuff(self, self.game.all_blocks, 'y')


#class Block(Sprite):
class P1Block(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_blocks
        Sprite.__init__(self, self.groups)
        self.health = 500
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.game = game
        draw_text(self, str(self.health), 24, BLACK, (TILESIZE * TILESIZE) / 4, TILESIZE * TILESIZE - TILESIZE)
        print(self.health)
        #self.image = (draw_health_bar(game.screen, 8, 8, 88, RED))
        self.image = pg.Surface((TILESIZE/2 + TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.hit_rect = BLOCK_HIT_RECT



   
    # way to get health of block
    #def get_health(self):
        #self.health = 500


    def update(self):
        get_health(self, self.game.all_players)
        get_health(self, self.game.all_contenders)
        # block_lose_health(self, self.game.all_players)
        # block_lose_health(self, self.game.all_contenders)
        # self.hit_rect.centerx = self.pos.x
        # self.hit_rect.centery = self.pos.y
        # self.rect.center = self.hit_rect.center
        #self.health = self.get_health()


class P2Block(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_blocks
        Sprite.__init__(self, self.groups)
        self.health = 500
        print(self.health)
        self.game = game
        self.image = pg.Surface((TILESIZE/2 + TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
   
    def update(self):
        pass



