# -*- coding: utf-8 -*-
import pygame
from libs.pyganim import pyganim

version = "0.3.3.1 dev"

typeface = "monospace"
stdfont = pygame.font.SysFont(typeface, 15)

debugmode = True

musicend = pygame.locals.USEREVENT + 100

physics_update_delay = 25  # milliseconds

speed_factor = 0.0025  # used to be konstspeed
dstars = 500
dtargets = 5
color_palette = ((255, 255, 10), (0, 0, 0))  # used to be color and single tuple

#TODO Images are not constants
# load images and convert them to the fatest blittable format
background = pygame.image.load("./assets/sprites/Background2.tif").convert()
field = pygame.image.load("./assets/sprites/inputbox1.tif").convert_alpha()
bullet_img = pygame.image.load("./assets/sprites/Bullet.tif").convert_alpha()
targeton_img = pygame.image.load("./assets/sprites/mine_on.tif").convert_alpha()
targetoff_img = pygame.image.load("./assets/sprites/mine_off.tif").convert_alpha()
border1 = pygame.image.load("./assets/sprites/bar1.tif").convert_alpha()
item_bar_image = pygame.image.load("./assets/sprites/item_bar.tif").convert()


explosions= [
                pyganim.PygAnimation(
                                        [(image, 40) for image in pyganim.getImagesFromSpriteSheet(
					                                               "./assets/sprites/explosions/expl_09.png",
					                                               width=128, height=128)],
                                        loop=False),
                pyganim.PygAnimation(
                                        [(image, 40) for image in pyganim.getImagesFromSpriteSheet(
					                                               "./assets/sprites/explosions/expl_10.png",
					                                               width=128, height=128)],
                                        loop=False),
                pyganim.PygAnimation(
                                        [(image, 40) for image in pyganim.getImagesFromSpriteSheet(
					                                               "./assets/sprites/explosions/expl_11.png",
					                                               width=96, height=96)],
                                        loop=False)
            ]
