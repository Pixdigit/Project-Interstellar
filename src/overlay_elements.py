# -*- coding: utf-8 -*-
import pygame
import libs.overlay as overlay
from . import settings


class item_bar_creator(overlay.elements.overlay_element, object):

	def __init__(self, name):
		self.proto = super(item_bar_creator, self)
		self.proto.__init__(name, self.pos_getter)
		for i in range(6):
			self.create_sub(i, subclass=item_slot)
		self.update()

	def pos_getter(self):
		height = int(0.11 * settings.screeny_current)
		self.pos.size = (height * 6, height)
		self.pos.bottom = settings.screeny_current
		self.pos.centerx = settings.screenx_current / 2


class item_slot(overlay.elements.overlay_element, object):

	def __init__(self, number):
		self.proto = super(item_slot, self)
		self.slot_nr = number
		self.proto.__init__("item_slot_" + str(number + 1), self.pos_getter,
				img="./assets/sprites/item_bar.tif")
		self.orig_img = self.img.copy()
		self.img = pygame.transform.smoothscale(self.orig_img, self.pos.size)

	def update(self):
		self.proto.update()
		self.img = pygame.transform.smoothscale(self.orig_img, self.pos.size)

	def pos_getter(self):
		self.pos.size = (int(0.11 * settings.screeny_current),) * 2
		self.pos.top = 0
		self.pos.left = (self.slot_nr * self.pos.width)
