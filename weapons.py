import pygame as pg
from settings import *
from player_states import *
from state_machine import *
import random


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def draw_circle(sprite, color):
    sprite.image.fill((0, 0, 0, 0))
    pg.draw.circle(sprite.image, color, (TILESIZE // 2, TILESIZE // 2,), TILESIZE// 2)


# function: 1/100 chance of spawning the weapon every second
def weapon_spawn(sprite):
    total_ticks = pg.time.get_ticks()
    # this checks the function once every second
    # Rohnin helped me with this
    if total_ticks - sprite.seconds > 1000:
        sprite.seconds = total_ticks
        if not sprite.has_weapon:
            weapon_attempt = random.randint(1, 50)
            if weapon_attempt == 1:
                print('lottery successful')
                #cool_down = pg.time.get_ticks()
                #while cool_down < 10000:
                sprite.has_weapon = True
                choose_weapon(sprite)
                sprite.weapon_duration = total_ticks
                #ticks = 0
                #sprite.has_weapon = False
                #sprite.image.fill(GRAY)
            else:
                #sprite.image = pg.Surface((TILESIZE, TILESIZE), pg.SRCALPHA)
                draw_circle(sprite, GRAY)
   
    # weapon stays in the sprite for 10 seconds
    if sprite.has_weapon:
        if total_ticks - sprite.weapon_duration > 7000 and total_ticks - sprite.weapon_duration < 10000:
                if ((total_ticks - sprite.weapon_duration) // 250) % 2 == 0:
                    draw_circle(sprite, WHITE)
                else:
                    sprite.image = sprite.weapon_color.copy()
        # we set the sprite duration equal to total_ticks earlier, now 10s will pass
        if total_ticks - sprite.weapon_duration >= 10000:
            # this warns the player if there is three seconds or less left for the weapon to be collected
            print('weapon cooldown done')
            sprite.has_weapon = False
            draw_circle(sprite, GRAY)


# def spawn_timing(sprite):
#     sprite.cool_down = pg.time.get_ticks()
#     if sprite.cool_down > 2000:
#         print('exceeded cooldown time')


# def weapon_spawn_timing(sprite):
#     # function: 1/15 chance of spawning the weapon
#     cool_time = pg.time.get_ticks()
#     sprite.image.fill(GRAY)
#     weapon_attempt = random.randint(1, 870)
#     if cool_time > 1000:
#         while weapon_attempt == 1:
#             print('lottery successful')
#             choose_weapon(sprite)
#             sprite.has_weapon = True
#             # weapon is stored for 10 seconds
#             weapon_stored_time = pg.time.get_ticks()
#             if weapon_stored_time > 10000:
#                 weapon_attempt = 0
#                 weapon_stored_time = 0
#                 sprite.image.fill(GRAY)
#                 sprite.has_weapon = False
#         else:
#             sprite.weapon_attempt = 0
#             cool_time = 0
#             sprite.image.fill(GRAY)
#             sprite.has_weapon = False


def choose_weapon(weapon):
    # choose a random number from 1 to 3 and give me the results
    weapon.code = random.randint(1, 3)
    if weapon.code == 1:
        weapon.type = "Spear"
        draw_circle(weapon, PURPLE)
    elif weapon.code == 2:
        weapon.type = 'Hammer'
        draw_circle(weapon, ORANGE)
    else:
        weapon.type = "Sword"
        draw_circle(weapon, GREEN)
   
    # keeps this info stored for the color
    weapon.weapon_color = weapon.image.copy()

def collide_and_collect(sprite, group):
    # True for 3rd argument kills the coin permanently
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    for coin in hits:
        if coin.active and coin.has_weapon:
            coin.collect()
            print("coin collected")
            sprite.weapon_equipped = True

def weapon_collection(sprite, group, weapon):
    if sprite.weapon_equipped == True:
        pass




