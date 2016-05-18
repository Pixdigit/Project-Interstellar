# -*- coding: utf-8 -*-
import pygame
import math
from libs.pyganim import pyganim
from ConfigParser import SafeConfigParser
from . import overlay_handler


class player():

	def __init__(self):
		global settings
		from . import settings  # lint:ok
		self.speed = 15  # Speed of player (redunant see self.new_ship())

		self.rotation = 0  # Current player rotation
		# Absolute player position. size is calculated when image gets loaded
		self.pos = pygame.Rect(0, 0, 0, 0)
		self.rot_dest = 0  # Where the player should turn
		self.should_move = False  # Determines wether player should move
		self.move_x = 0  # Delta pixel per tick (x)
		self.move_y = 0  # Delta pixel per tick (y)
		self.rel_x = 0  # relative x position
		self.rel_y = 0  # relative y position
		self.timeplay = 0  # Time player has played
		self.update = True  # If yes new image gets loaded
		self.speedboost = 1
		self.explosion_anim = None
		self.new_ship("Player1")
		self.overlay = overlay_handler.create_overlay()
		overlay_elem_pos = (settings.screenx_current / 2, settings.screeny_current)
		overlay_obj = overlay_handler.overlay_element_base_class(
							"items", overlay_elem_pos, "midbottom")
		overlay_obj.load_image("./assets/sprites/item_bar.png")
		self.overlay.add_overlay_element(overlay_obj)
		self.overlay.activate()

	def create_images(self, name):
		"""creates new images from one image for the player"""

		folder = "./assets/sprites/player/"

		names = [
			name + "_up", name + "_upri", name + "_ri", name + "_dori",
			name + "_do", name + "_dole", name + "_le", name + "_uple"]

		# generates new images in ./assets/sprites/player
		for nameoffile in names:
			self.playerup = pygame.image.load("./assets/sprites/ships/" +
			name + ".tif")
			angle = names.index(nameoffile) * -45
			nameoffile = folder + nameoffile + ".png"
			pygame.image.save(pygame.transform.rotate(self.playerup, angle), nameoffile)

		# loads images into ram
		self.playerupri = pygame.image.load(folder + name + "_upri.png")
		self.playerri = pygame.image.load(folder + name + "_ri.png")
		self.playerdori = pygame.image.load(folder + name + "_dori.png")
		self.playerdo = pygame.image.load(folder + name + "_do.png")
		self.playerdole = pygame.image.load(folder + name + "_dole.png")
		self.playerle = pygame.image.load(folder + name + "_le.png")
		self.playeruple = pygame.image.load(folder + name + "_uple.png")

	def select_img(self):
		"""changes the playerimage corresponding to the movement direction"""

		if self.rotation == 0 or self.rotation == 360:
			self.img = self.playerup
		if self.rotation == 45:
			self.img = self.playerupri
		if self.rotation == 90:
			self.img = self.playerri
		if self.rotation == 135:
			self.img = self.playerdori
		if self.rotation == 180:
			self.img = self.playerdo
		if self.rotation == 225:
			self.img = self.playerdole
		if self.rotation == 270:
			self.img = self.playerle
		if self.rotation == 315:
			self.img = self.playeruple

	def move_abs(self, addx, addy):
		#lint:disable
		self.rel_x = (self.pos.x + addx) / float(settings.screenx_current)
		self.rel_y = (self.pos.y + addy) / float(settings.screeny_current)
		self.pos.top = int(self.rel_y * settings.screeny_current)
		self.pos.left = int(self.rel_x * settings.screenx_current)
		#lint:enable

	def move_rel(self, *args):
		if len(args):
			self.rel_x = args[0]
			self.rel_y = args[1]
		#lint:disable
		self.pos.top = int(self.rel_y * settings.screeny_current)
		self.pos.left = int(self.rel_x * settings.screenx_current)
		#lint:enable

	def move(self):
		"""Handle the movement and collisions"""
		#lint:disable
		konstspeed = settings.konstspeed
		windowwidth = settings.screenx_current
		windowheight = settings.screeny_current
		#lint:enable

		if self.rotation > 360:
			self.rotation -= 360
		if self.rotation < 0:
			self.rotation += 360

		#Turns player to according rotation
		#lint:disable
		self.select_angle(settings.up, settings.down,
			settings.left, settings.right)
		#lint:enable

		# handles rotation and gives signal to update player image/surface
		if self.rotation != self.rot_dest:
			self.update = True
			if self.rot_dest > self.rotation:
				if (self.rot_dest - self.rotation) <= 180:
					self.rotation += 5.625
				if (self.rot_dest - self.rotation) > 180:
					self.rotation -= 5.625
			if self.rot_dest < self.rotation:
				if (self.rot_dest - self.rotation) > -180:
					self.rotation -= 5.625
				if (self.rot_dest - self.rotation) <= -180:
					self.rotation += 5.625

		# this part is responsible for the movement of the player
		# this calculates speed in y and x direction
		self.move_x = self.speedboost * konstspeed * math.degrees(math.sin(
			(math.radians(self.rotation))))
		self.move_y = self.speedboost * -konstspeed * math.degrees(math.cos(
			(math.radians(self.rotation))))

		# this actually moves the rect and ensures that you stay in screen
		if self.should_move:
			self.rel_x += float(self.move_x * self.speed) / (windowwidth)
			self.rel_y += float(self.move_y * self.speed) / (windowheight)

			if self.rel_x < 0:
				self.rel_x -= self.rel_x
			if self.rel_x > (1 - (float(self.pos.w) / windowwidth)):
				self.rel_x = 1 - (float(self.pos.w) / windowwidth)
			if self.rel_y < 0:
				self.rel_y -= self.rel_y
			if self.rel_y > (1 - (float(self.rel_y) / windowheight)):
				self.rel_y = 1 - (float(self.pos.h) / windowheight)

			self.pos.top = int(self.rel_y * windowheight)
			self.pos.left = int(self.rel_x * windowwidth)

			#lint:disable
			# Somehow a double check is needed…
			if self.pos.bottom >= settings.screeny_current:
				self.pos.bottom += settings.screeny_current - self.pos.bottom
			if self.pos.right >= settings.screenx_current:
				self.pos.right += settings.screenx_current - self.pos.right
			#lint:enable

		# updates player image if neccesary
		if self.update:
			self.update = False
			self.select_img()

	def select_angle(self, up, down, left, right):

		self.should_move = False
		# sets the direction depending of input
		if not (up == down and left == right):
			# diagonal moves
			if up and left and not down and not right:
				self.should_move = True
				self.rot_dest = 315
			if up and right and not left and not down:
				self.should_move = True
				self.rot_dest = 45
			if down and left and not up and not right:
				self.should_move = True
				self.rot_dest = 225
			if down and right and not up and not left:
				self.should_move = True
				self.rot_dest = 135
			# moving in y != x
			if up and not down:
				if left == right:
					self.should_move = True
					self.rot_dest = 0
			if left and not right:
				if down == up:
					self.should_move = True
					self.rot_dest = 270
			if down and not up:
				if left == right:
					self.should_move = True
					self.rot_dest = 180
			if right and not left:
				if up == down:
					self.should_move = True
					self.rot_dest = 90

	def new_ship(self, name):
		config = SafeConfigParser()
		config.read("./assets/sprites/ships/" + name + ".ini")
		self.speed = config.getfloat("main", "speed")
		self.create_images(name)
		self.img = self.playerup
		self.select_img()
		self.pos.size = self.img.get_size()

	def explode(self):
		self.speedboost = 0
		explosion_img = pyganim.getImagesFromSpriteSheet(
				"./assets/sprites/explosions/ship_expl.png",
				width=256, height=256)
		explosion_attr = [(anim_file, 40) for anim_file in explosion_img]
		self.explosion_anim = pyganim.PygAnimation(explosion_attr, loop=False)
		self.explosion_anim.play()

	def blit(self, screen):
		if self.explosion_anim is None:
			screen.blit(self.img, self.pos)
			self.overlay.blit(screen)
		else:
			self.update = False
			pos = self.pos.copy()
			pos.x -= self.explosion_anim.getMaxSize()[0] / 2
			pos.y -= self.explosion_anim.getMaxSize()[1] / 2
			self.explosion_anim.blit(screen, pos)

	def reset(self):
		self.should_move = False
		self.rot_dest = 0
		self.rotation = 0
		self.speedboost = 1
		self.pos = self.img.get_rect()
