# -*- coding: utf-8 -*-
from libs.overlay import overlay
import pygame


class item_bar(overlay.overlay_element_base_class):

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
		old_item = self.slots[slot]
		self.slots[slot] = item
		return old_item

	def set_pos_of_item(self, old_slot, new_slot):
		#swich positions of items in old_slot and new_slot
		new_item = self.set_item(new_slot, self.slots[old_slot])
		self.set_item(old_slot, new_item)

	def get_item_pos(self, item_name):
		for item in self.slots:
			if item is not None:
				if item.name == item_name:
					return self.slots.index(item)

	def blit(self, screen):
		if self.active:
			screen.blit(self.img, self.pos)
			for index in range(len(self.slots)):
				item = self.slots[index]
				if not item is None:
					this_pos = self.slot_pos[index]
					screen.blit(item.img, this_pos)
