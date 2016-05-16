# -*- coding: utf-8 -*-
import pygame


class create_overlay():
	"""A mother-class for in-game overlays.

	init(self) inits the module
	add_overlay(self, overlay_obj, overwrite=False) adds an overlay element
	hide(self, elements=None) hides elements"""

	def __init__(self):
		self.objects = {}
		self.objs_on_screen = set()

	def add_overlay_element(self, overlay_obj, overwrite=False):
		"""Adds an overlay element to the whole overlay.

		overwrite determines that if an object with the name already
		exists if it should be overwritten
		whereas the object must have following vars:
			name as string
			active as bool
		and following funtions:
			activate() sets active to True. May include animation
			deactivate() sets active to False. May include animation
			hide() sets active to False. Happens immediately
			unhide() sets active to True. Happens immediately
			blit(screen) blits its image onto the screen variable
		"""

		if (overlay_obj.name not in self.objects) or overwrite:
			overlay_obj.deactivate()
			self.objects[overlay_obj.name] = overlay_obj

	def activate(self, elements=None):
		"""Unhides elements.
		When called with no arguments, all elements get shown.
		Can also be called with name or a list with names.
		"""

		if elements is None:
			for object_name in self.objects:
				self.objects[object_name].activate()
		else:
			if type(elements) != list:
				elements = list(elements)
			for element_name in elements:
				self.objects[element_name].activate()

	def hide(self, elements=None):
		"""Hides elements.
		When called with no arguments, all elements get hidden.
		Can also be called with name or a list with names.
		"""

		if elements is None:
			for object_name in self.objects:
				self.objects[object_name].deactivate()
		else:
			if type(elements) != list:
				elements = list(elements)
			for element_name in elements:
				self.objects[element_name].deactivate()

	def blit(self, screen):
		for obj in self.objects.values():
			screen.blit(obj.img, obj.pos)


class overlay_element_base_class():
	"""This is an element which can be used in an overlay"""

	def __init__(self, name, pos, alignment="topleft"):
		self.name = name
		self.pos = pygame.Rect((0, 0, 0, 0))
		#TODO implement size
		self.set_alignment(pos, "topleft")
		self.active = False

	def set_alignment(self, pos, alignment):
		if not alignment in ["topleft", "topright", "bottomleft", "botomright",
				"center", "midtop", "midleft", "midright", "midbottom"]:
					raise TypeError("Alignment is of unknown type: " + str(alignment))
		if alignment == "topleft":
			self.pos.topleft = pos
		elif alignment == "topright":
			self.pos.topright = pos
		elif alignment == "bottomleft":
			self.pos.bottomleft = pos
		elif alignment == "bottomright":
			self.pos.bottomright = pos
		elif alignment == "center":
			self.pos.center = pos
		elif alignment == "midtop":
			self.pos.midtop = pos
		elif alignment == "midleft":
			self.pos.midleft = pos
		elif alignment == "midright":
			self.pos.midright = pos
		elif alignment == "midbottom":
			self.pos.midbottom = pos
		else:
			raise Exception("I have no idea what you have done to crash this…")

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False

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
