# -*- coding: utf-8 -*-
import pygame


class create_overlay():
	"""A mother-class for in-game overlays.

	init(self) inits the module
	add_overlay(self, overlay_obj) adds an overlay element"""

	def __init__(self):
		self.objects = {}
		self.objs_on_screen = set()

	def add_overlay_element(self, overlay_obj):
		"""Adds an overlay element to the whole overlay.

		This method requires an instance.
		It is called as follows: instance.add_overlay_element(overlay_obj)
		For custom objects see class overlay_object.
		"""
		self.objects[overlay_obj.name] = overlay_obj

	def enable(self, name_list):
		"""Enable the overlay."""
		tmp_list = []
		if name_list == "all":
			tmp_list = list(self.objects.values())
		else:
			if type(name_list) == str:
				name_list = [name_list]
			for obj in self.objects:
				if obj in name_list:
					tmp_list.append(self.objects[obj])
		self.objs_on_screen.update(tmp_list)

	def disable(self, name_list):
		"""Disable the overlay."""
		if name_list == "all":
			self.objs_on_screen = set()
		else:
			if type(name_list) == str:
				name_list = name_list.split(",")
			for obj in self.objects:
				if obj in name_list:
					self.objs_on_screen.remove(self.objects[obj])
					return

	def update(self):
		for overlay_object in list(self.objects.values()):
			overlay_object.update()

	def blit(self, screen):
		for obj in list(self.objects.values()):
			screen.blit(obj.img, obj.pos)


class create_overlay_object():
	"""This is an element which can be used in an overlay"""

	def __init__(self, name):
		self.name = name
		self.pos = pygame.Rect((0, 0, 1, 1))

	def set_image(self, img):
		self.img = img

	def load_image(self, file_or_fileobj):
		self.image = pygame.load(file_or_fileobj)

	def load_text(self, text, font_name, size, color, **kwargs):
		if type(size) == int:
			font = pygame.font.SysFont(font_name, size, **kwargs)
			self.img = font.render(text, True, color)
		if type(size) in [list, tuple]:
			for int_size in range(size[1] / 2):
				font = pygame.font.SysFont(font_name, size, **kwargs)
				test_size = font.render(text)
				if test_size[0] > size[0] or test_size[1] > size[1]:
					font = pygame.font.SysFont(font_name, test_size - 1, **kwargs)
					self.img = font.render(text, True, color)

	def update(self):
		pass
