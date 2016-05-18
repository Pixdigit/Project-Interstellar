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
		for obj in list(self.objects.values()):
			obj.blit(screen)


class overlay_element_base_class():
	"""This is an element which can be used in an overlay"""

	def __init__(self, name, pos, alignment="topleft"):
		self.name = name
		#TODO implement size
		self.pos = pygame.Rect((0, 0, 0, 0))
		self.alignment = alignment
		self.set_alignment(pos, alignment)
		self.active = False

	def adjust_to_image(self):
		old_pos = self.pos.copy()
		self.pos.size = self.img.get_size()
		if self.alignment == "topleft":
			new_pos = old_pos.topleft
		elif self.alignment == "topright":
			new_pos = old_pos.topright
		elif self.alignment == "bottomleft":
			new_pos = old_pos.bottomleft
		elif self.alignment == "bottomright":
			new_pos = old_pos.bottomright
		elif self.alignment == "center":
			new_pos = old_pos.center
		elif self.alignment == "midtop":
			new_pos = old_pos.midtop
		elif self.alignment == "midleft":
			new_pos = old_pos.midleft
		elif self.alignment == "midright":
			new_pos = old_pos.midright
		elif self.alignment == "midbottom":
			new_pos = old_pos.midbottom
		self.set_alignment(new_pos, self.alignment)
		print self.pos.midbottom
		print self.pos.bottom
		print self.pos.midtop

	def set_alignment(self, pos, alignment):
		if not alignment in ["topleft", "topright", "bottomleft", "botomright",
				"center", "midtop", "midleft", "midright", "midbottom"]:
			raise TypeError("Alignment is of unknown type: " + str(alignment))
		else:
			self.alignment = alignment
		if self.alignment == "topleft":
			self.pos.topleft = pos
		elif self.alignment == "topright":
			self.pos.topright = pos
		elif self.alignment == "bottomleft":
			self.pos.bottomleft = pos
		elif self.alignment == "bottomright":
			self.pos.bottomright = pos
		elif self.alignment == "center":
			self.pos.center = pos
		elif self.alignment == "midtop":
			self.pos.midtop = pos
		elif self.alignment == "midleft":
			self.pos.midleft = pos
		elif self.alignment == "midright":
			self.pos.midright = pos
		elif self.alignment == "midbottom":
			self.pos.midbottom = pos
		else:
			raise Exception("I have no idea what you have done to crash this…")

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False

	def set_image(self, img):
		self.img = img
		self.adjust_to_image()

	def load_image(self, file_or_fileobj):
		self.img = pygame.image.load(file_or_fileobj)
		self.adjust_to_image()

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
		self.adjust_to_image()

	def blit(self, screen):
		if self.active:
			screen.blit(self.img, self.pos)
