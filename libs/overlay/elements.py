# -*- coding: utf-8 -*-
import pygame
import os
import helpers


class overlay_element():

	def __init__(self, name, pos_getter, img=None):
		self.name = name
		self.id = helpers.get_unique_id()
		self.sub_elements = []
		self.active = True

		self.rel_pos = pygame.Rect(0, 0, 0, 0)
		if not callable(pos_getter):
			rect = pygame.Rect(pos_getter)
			pos_getter = lambda self, old_rect: rect
		self.pos = pygame.Rect(0, 0, 0, 0)
		self.pos_getter = pos_getter
		self.pos_getter()

		if img is None:
			self.has_image = False
			self.img = pygame.Surface(self.pos.size, pygame.SRCALPHA)
			self.img.set_alpha(0)
		else:
			self.has_image = True
			if type(img) == str and os.path.isfile(img):
				self.img = pygame.image.load(img)
			else:
				self.img = img
			self.pos.size = self.img.get_size()
		self.merge_image = self.img.copy()

		try:
			self.img.convert_alpha()
			self.merge_image.convert_alpha()
		except pygame.error:
			print(("Warning: Creating overlays without video mode set\n"
				"         causes decreased performance while blitting."))

	def set_visability(self, status):
		self.active = status
		for elem in self.sub_elements:
			elem.set_visability(status)

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

	def get_upper(self, id_or_name):
		if type(id_or_name) in [str, unicode]:
			elem_id = self.get_by_name(id_or_name).id
		else:
			elem_id = id_or_name

		obj = self.get_by_id(elem_id)

		for elem in self.get_sub() + [self]:
			if obj in elem.sub_elements:
				return elem
		return None

	def create_sub(self, *args, **kwargs):

		if "subclass" not in kwargs:
			kwargs["subclass"] = overlay_element

		assert issubclass(kwargs["subclass"], overlay_element)

		sub = kwargs["subclass"](*args)
		self.sub_elements.append(sub)
		return sub

	def set_sub(self, obj):
		self.sub_elements.append(obj)

	def get_sub(self):
		elem_list = []
		for elem in self.sub_elements:
			elem_list.append(elem)
			elem_list = elem_list + elem.get_sub()
		return elem_list

	def rm_sub(self, name_or_id):
		if type(name_or_id) == str:
			obj_id = self.get_by_name(name_or_id).id
		else:
			obj_id = name_or_id

		removed_object = None
		for elem in self.sub_elements:
			if elem.id == obj_id:
				removed_object = elem
				self.sub_elements.remove(elem)
				break
			else:
				removed_object = elem.rm_sub(obj_id)
				if removed_object is not None:
					break
		return removed_object

	def update(self):
		self.pos_getter()
		for elem in self.sub_elements:
			elem.update()

	def blit(self, screen, rel_pos):
		rel_pos = pygame.Rect(rel_pos)
		if self.name == "item_bar":
			print self.pos
		if self.active:
			tmp_pos = self.pos.copy()
			tmp_pos.top += rel_pos.top
			tmp_pos.left += rel_pos.left
			screen.blit(self.img, tmp_pos)
			for elem in self.sub_elements:
				elem.blit(screen, tmp_pos)
