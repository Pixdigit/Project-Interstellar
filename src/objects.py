# -*- coding: utf-8 -*-
import pygame
import random
import math
from . import settings
from . import overlay_handler

"""Classes for creating objects"""


class stars():

	def __init__(self):
		"""creates a new star"""

		screenx = settings.screenx_current
		screeny = settings.screeny_current

		self.image = pygame.image.load("./assets/sprites/star1.tif")
		imgsize = self.image.get_width()

		# random size between 0 and 100 %
		self.size = random.randint(0, 100) / 100.0
		minimum = 0.15
		maximum = 0.70
		# determing the depth of the star
		self.depth = (self.size * (maximum - minimum)
				) + minimum  # value mapped between .15 and .70
		self.image = pygame.transform.smoothscale(self.image,
						(int(imgsize * self.depth), int(imgsize * self.depth)))

		self.pos = self.image.get_rect()
		self.screenx = screenx - self.pos.w
		self.screeny = screeny - self.pos.h
		# gives a percentage where star is located
		# values between -1 and +1
		self.relative_x = (random.random() * 2) - 1
		self.relative_y = (random.random() * 2) - 1
		self.update(screenx / 1920.0)

	def move(self, x, y):
		"""Moves the star according to player position"""
		# note: x and y are the player position
		# and that screenx and screeny are not actual screen width and height
		self.pos.left = ((self.screenx - x) * self.depth) - self.pointx
		self.pos.top = ((self.screeny - y) * self.depth) - self.pointy

	def blitstar(self):
		"""blits the star"""
		screeny = settings.screeny_current
		screenx = settings.screenx_current

		if (-self.pos.h < self.pos.top < screeny + self.pos.h and
			-self.pos.w < self.pos.left < screenx + self.pos.w):
			settings.screen.blit(self.image, self.pos)
			return True
		return False

	def update(self, ratio):
		"""Resizes star fitting to resolution"""
		size = int(self.size * (ratio / 2.0))
		if size > 5:
			self.image = pygame.image.load("./assets/sprites/star1.tif")
			self.image = pygame.transform.smoothscale(self.image, (size, size))
			self.pos = self.image.get_rect()
		self.screenx = settings.screenx_current - self.pos.w
		self.screeny = settings.screeny_current - self.pos.h
		self.pointx = self.relative_x * self.screenx
		self.pointy = self.relative_y * self.screeny


class bullet():

	def __init__(self, angle, reference):
		"""Creates new bullet"""
		self.start = (reference.centerx, reference.centery)
		self.image = settings.bullet_img
		self.pos = self.image.get_rect()
		self.pos.center = self.start
		self.angle = angle
		self.move_x = 0.22125 * math.degrees(math.sin((math.radians(self.angle))))
		self.move_y = -0.22125 * math.degrees(math.cos((math.radians(self.angle))))
		if settings.player.should_move:
			self.move_x += settings.player.move_x * settings.player.speed
			self.move_y += settings.player.move_y * settings.player.speed
		self.inscreen = True
		self.distance = [0, 0]
		self.move(settings.player.pos)

	def move(self, player_pos):
		"""Moves the bullet"""
		# movement to adjust to player position
		tmpx = self.start[0] + (self.start[0] - player_pos[0]) - (self.pos.w / 2.0)
		tmpy = self.start[1] + (self.start[1] - player_pos[1]) - (self.pos.h / 2.0)
		# movement by acceleration
		self.distance[0] += self.move_x
		self.distance[1] += self.move_y
		# overall position
		self.pos.center = (self.distance[0] + tmpx, self.distance[1] + tmpy)

		# inscreen detection
		if not self.pos.colliderect(settings.screen.get_rect()):
			self.inscreen = False

	def blit(self):
		"""Blits the bullet"""
		screeny = settings.screeny_current
		screenx = settings.screenx_current

		if 0 < self.pos.top < screeny and 0 < self.pos.left < screenx:
			settings.screen.blit(self.image, self.pos)
			return True
		return False


class target():

	def __init__(self):
		"""Creates new random target"""
		self.image = settings.targeton_img
		self.chooser = True
		self.pos = self.image.get_rect()
		self.pos_xper = random.random()
		self.pos_yper = random.random()
		self.update()
		if not 0 < self.pos_x < settings.world.background_pos:
			message1 = "Targets have been found outside the world!\n"
			message2 = "Please report these values on our github page.\n"
			raise ValueError(message1
					+ message2
					+ str(self.pos_x)
					+ ":"
					+ str(self.pos_y))
		self.timer = random.randint(0, 1000)
		self.gothit = False
		random_explosion = random.randint(0, len(settings.explosions) - 1)
		self.explosion = settings.explosions[random_explosion]
		self.kill_entity = False
		self.inscreen = True
		self.move(settings.player.pos.x, settings.player.pos.y)
		self.test = 0

	def update(self):
		"""Adjusts position according to screen size"""
		self.pos_x = self.pos_xper * 2 * float(settings.screenx_current - self.pos.w)
		self.pos_y = self.pos_yper * 2 * float(settings.screeny_current - self.pos.h)

	def move(self, x, y):
		"""Moves rect according to playerposition"""
		newtime = pygame.time.get_ticks()
		if newtime > self.timer:
			while newtime > self.timer:
				self.timer += 1000
			self.chooser = settings.toggle(self.chooser, True, False)
			if self.chooser:
				self.image = settings.targeton_img
			elif not self.chooser:
				self.image = settings.targetoff_img
		if self.pos.colliderect(settings.screen.get_rect()):
			self.inscreen = True
		else:
			self.inscreen = False

		self.pos.left = self.pos_x - x
		self.pos.top = self.pos_y - y

	def test_ishit(self, bulletrect):
		"""Tests if target got hit"""
		if self.pos.colliderect(bulletrect) and not self.gothit:
			self.pos_x -= self.explosion.getRect().w / 2.0
			self.pos_y -= self.explosion.getRect().h / 2.0
			self.pos.size = self.explosion.getRect().size
			self.explosion.play()
			self.gothit = True
			while self.explosion.state in ["stopped", "paused"]:
				self.explosion.play()

	def blit(self):
		"""Blits target and explosion"""
		if self.gothit:
			# blit explosion
			has_finished = self.explosion.state in ["stopped", "paused"]
			if self.explosion.isFinished() or has_finished:
				# signal to kill entity
				self.kill_entity = True
			elif not self.kill_entity:
				# otherwise show explosion
				self.explosion.blit(settings.screen, self.pos)
				return True
		else:
			# show target if inscreen
			if self.inscreen:
				settings.screen.blit(self.image, self.pos)
				return True
			return False

	def unique_relevant_data(self):
		data = {}
		data["timer"] = self.timer
		data["pos_yper"] = self.pos_yper
		data["pos_xper"] = self.pos_xper
		return data


class warp_station():

	def __init__(self):
		self.x_pos = random.random()
		self.y_pos = random.random()
		self.screen = settings.screen
		self.update()

	def update(self):
		"""Adjusts to screen size"""
		self.img = pygame.image.load("./assets/sprites/station1.tif")
		self.img = pygame.transform.smoothscale(self.img,
						(int(settings.screenx_current * 0.1),
							int(settings.screenx_current * 0.1)
						))
		self.pos = self.img.get_rect()
		self.pos.x = self.x_pos * 2 * float(settings.screenx_current - self.pos.w)
		self.pos.y = self.y_pos * 2 * float(settings.screeny_current - self.pos.h)
		self.anchorx, self.anchory = self.pos.topleft

	def move(self, playerpos):
		self.pos.left = self.anchorx - playerpos.x
		self.pos.top = self.anchory - playerpos.y

	def test(self, playerpos):
		def testpoint(point):
			x_sqr = ((point[0] * point[0])
				- (2.0 * self.pos.centerx * point[0])
				+ (self.pos.centerx * self.pos.centerx))
			y_sqr = ((point[1] * point[1])
				- (2.0 * self.pos.centery * point[1])
				+ (self.pos.centery * self.pos.centery))
			if math.sqrt(x_sqr + y_sqr) < self.pos.w / 2.0:
				return True
			else:
				return False

		def test_collide():
			test = testpoint(playerpos.topleft)
			test = test or testpoint(playerpos.bottomleft)
			test = test or testpoint(playerpos.topright)
			test = test or testpoint(playerpos.bottomright)
			return test
		if test_collide():
			# Warps to the selected world and gets a bit pushed off the station
			from . import menu
			selected_num = menu.choose_world()
			if selected_num >= 0:
				settings.world = settings.localmap[selected_num]
				settings.world.adjust_to_screen()
			settings.player.up = False
			settings.player.down = False
			settings.player.left = False
			settings.player.right = False
			settings.up = False
			settings.down = False
			settings.left = False
			settings.right = False
			while test_collide():
				if settings.player.pos.center[0] < self.pos.center[0]:
					settings.player.move_abs(-20, 0)
				else:
					settings.player.move_abs(20, 0)
				if settings.player.pos.center[1] < self.pos.center[1]:
					settings.player.move_abs(0, -20)
				else:
					settings.player.move_abs(0, 20)
				playerpos = settings.player.pos

	def blit(self):
		self.screen.blit(self.img, self.pos)

	def unique_relevant_data(self):
		data = {}
		data["y_pos"] = self.y_pos
		data["x_pos"] = self.x_pos
		return data


class item_bar(overlay_handler.overlay_element_base_class):

	def init(self):
		#this is a list of the relative positions for the slots. Orientation Topleft
		self.rel_pos_list = [0.002645503, 0.165343915, 0.330687831,
				0.501322751, 0.666666667, 0.832010582]
		self.slots = [None for i in range(6)]
		self.slot_pos = [pygame.Rect((0, 0, 0, 0))] * 6
		self.slot_size = 123

	def update_size(self, old_size):
		#this is an interface to base_class
		self.get_abs_pos()
		self.resize_icons()

	def get_abs_pos(self):
		new_border = int(self.rel_pos_list[0] * self.pos.width)
		self.slot_size = [int(
				(self.pos.width - 9 * self.rel_pos_list[0] * self.pos.width)
				/ 6.0)] * 2
		for rel_pos in self.rel_pos_list:
			index = self.rel_pos_list.index(rel_pos)
			new_x_pos = int(rel_pos * self.pos.width)
			self.slot_pos[index] = pygame.Rect(
						(new_x_pos + self.pos.left, new_border + self.pos.top),
						self.slot_size)

	def resize_icons(self):
		for item in self.slots:
			if not item is None:
				item.resize(self.slot_size)

	def set_item(self, slot, item):
		old_item = self.slot_pos[slot]
		self.slots[slot] = item
		return old_item

	def blit(self, screen):
		if self.active:
			screen.blit(self.img, self.pos)
			for index in range(len(self.slots)):
				item = self.slots[index]
				if not item is None:
					this_pos = self.slot_pos[index]
					screen.blit(item.img, this_pos)
