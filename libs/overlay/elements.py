# -*- coding: utf-8 -*-
import pygame
import helpers


class create_overlay():

	def __init__(self, name, pos_getter):
		#TODO Add image argument etc.
		self.name = name
		self.id = helpers.get_unique_id()
		self.sub_elements = []
		self.active = True

		self.img = pygame.Surface((200, 200))
		try:
			self.img.convert()
		except pygame.error:
			print(("Warning: Creating overlays without video mode set\n"
				"         causes decreased performance while blitting."))

		if not callable(pos_getter):
			rect = pygame.Rect(pos_getter)
			pos_getter = lambda: rect
		self.pos = pos_getter()
		self.pos_getter = pos_getter

	def set_visability(self, status, id_or_name_list=[]):
		if len(id_or_name_list) == 0:
			self.active = status
		else:
			for identifier in id_or_name_list:
				if type(identifier) == str:
					self.get_by_name(identifier).set_visability(status)
				else:
					self.get_by_id(identifier).set_visability(status)

	def conv_to_id(self, name_list):
		return [self.get_by_name(name).id for name in name_list]

	def get_by_name(self, name):
		if self.name == name:
			return self
		test_elem = None
		for elem in self.sub_elements:
			test_elem = elem.get_by_name(name)
			if test_elem is not None:
				break
		return test_elem

	def get_by_id(self, elem_id):
		if self.id == elem_id:
			return self
		test_elem = None
		for elem in self.sub_elements:
			test_elem = elem.get_by_id(elem_id)
			if test_elem is not None:
				break
		return test_elem

	def create_sub(self, *args):
		sub = create_overlay(*args)
		self.sub_elements.append(sub)

	def get_sub(self):
		elem_list = []
		for elem in self.sub_elements:
			elem_list.append(elem)
			elem_list = elem_list + elem.get_sub()
		return elem_list

	def update(self):
		for elem in self.sub_elements:
			elem.update()
		self.pos = self.pos_getter()

	def blit(self, screen):
		for elem in self.sub_elements:
			elem.blit(screen)
		if self.active:
			screen.blit(self.img, self.pos)
