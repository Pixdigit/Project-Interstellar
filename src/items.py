# -*- coding: utf-8 -*-
import pygame


def init():
	pass


class item():

	def __init__(self, name, surface):
		self.name = name
		self.orig_img = pygame.transform.smoothscale(surface, (123, 123))
		self.img = pygame.transform.smoothscale(surface, (123, 123))

	def resize(self, new_size):
		self.img = pygame.transform.smoothscale(self.orig_img, (new_size, new_size))
