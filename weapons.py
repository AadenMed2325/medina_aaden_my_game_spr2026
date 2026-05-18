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
    if total_ticks - sprite.seconds > 1000 and sprite.game.stage3:
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
                    # assess the attribute of the sprite
                    if sprite.type == "Spear":
                        draw_circle(sprite, PURPLE)
                    if sprite.type == "Hammer":
                        draw_circle(sprite, ORANGE)
                    if sprite.type == "Sword":
                        draw_circle(sprite, GREEN)
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
    # choose a random number from 1 to 10 and give me the results
    # gets the image from the spritesheet weapon.sheet which we assigned earlier
    weapon.code = random.randint(1, 10)
    if weapon.code == 7:
        weapon.type = "Spear"
        weapon.image = weapon.spritesheet.get_image(0, 0, TILESIZE, TILESIZE)
        #draw_circle(weapon, PURPLE)
    elif weapon.code <= 6:
        weapon.type = 'Hammer'
        weapon.image = weapon.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE)
        #draw_circle(weapon, ORANGE)
    else:
        weapon.type = "Sword"
        weapon.image = weapon.spritesheet.get_image(TILESIZE * 2, 0, TILESIZE, TILESIZE)
        #draw_circle(weapon, GREEN)
   
    # keeps this info stored for the color
    weapon.weapon_color = weapon.image.copy()

def collide_and_collect(sprite, group):
    # True for 3rd argument kills the coin permanently
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    for coin in hits:
        if coin.active and coin.has_weapon:
            coin.collect()
            sprite.game.weapon_snd.play()  # Play weapon collect sound
            sprite.collection_time = pg.time.get_ticks()
            # assign the type of weapon
            if coin.type == "Sword":
                print("sword collected")
                sprite.weapon = "Sword"
            elif coin.type == "Hammer":
                print("hammer collected")
                sprite.weapon = "Hammer"
            else:
                print("spear collected")
                sprite.weapon = "Spear"
            sprite.weapon_equipped = True

# pygame ai : I prompted it to differentiate now and collection_elapsed.
# collection_elapsed takes the time that the player has the weapon
# now is the time since the game started
def player_appearance_change(sprite):
    now = pg.time.get_ticks()
    if sprite.weapon_equipped == True:
        collection_elapsed = now - sprite.collection_time
        if sprite.id == 1:
            draw_circle(sprite, PINK)
        elif sprite.id == 2:
            draw_circle(sprite, CYAN)
        if collection_elapsed > 17000:
            if collection_elapsed % 1000 <= 500:
                draw_circle(sprite, WHITE)
            if collection_elapsed > 20000:
                sprite.weapon_equipped = False
                if sprite.id == 1:
                    draw_circle(sprite, RED)
                elif sprite.id == 2:
                    draw_circle(sprite, BLUE)



