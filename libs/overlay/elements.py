# -*- coding: utf-8 -*-
import pygame


class overlay_element_base_class():
	"""This is an element which can be used in an overlay"""

	def __init__(self, name, pos, alignment="topleft"):
		self.name = name
		#TODO implement size
		self.pos = pygame.Rect((0, 0, 0, 0))
		self.active = False

	def update_size(self, new_size):
		"""This can be used to implement a feature that repond to changes in size"""
		self.img = pygame.transform.smoothscale(self.img, new_size)
		self.pos.size = new_size

	def adjust_to_image(self):
		self.update_size(self.img.get_size())

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
