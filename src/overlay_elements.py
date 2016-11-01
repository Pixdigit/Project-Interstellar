# -*- coding: utf-8 -*-
import pygame
import libs.overlay as overlay
from . import settings
from . import specials


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


class status_bar(overlay.elements.overlay_element, object):

	def __init__(self):
		self.proto = super(status_bar, self)
		self.proto.__init__("status_bar", self.pos_getter)
		self.pos_getter()
		self.border = pygame.transform.smoothscale(
				settings.border1, self.pos.size).convert_alpha()
		self.indicator = pygame.Surface(self.pos.size).convert()
		self.indicator.set_alpha(40)
		self.indicator.fill((62, 186, 23))

	def pos_getter(self):
		self.pos.width = int(settings.screenx_current * 0.042)
		self.pos.height = int(settings.screeny_current * 0.25) + 10
		self.pos.bottom = settings.screeny_current
		self.pos.right = settings.screenx_current

	def blit(self, screen):
		if not settings.player.pos.colliderect(self.pos):
			screen.blit(self.indicator, (self.pos.left, settings.screeny_current
							- int(specials.energy / 100.0 * self.pos.height)))
			screen.blit(self.border, self.pos)

	def update(self):
		self.__init__()
