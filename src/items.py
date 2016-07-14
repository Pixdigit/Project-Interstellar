# -*- coding: utf-8 -*-
import pygame
import json
import importlib
import settings


def init():
	pass


class new_item():

	def __init__(self, *args):
		needed_dargs = 2
		if len(args) == needed_dargs:
			self.name = args[0]
			surface = args[1]
			self.orig_img = pygame.transform.smoothscale(surface, (123, 123))
			self.img = pygame.transform.smoothscale(surface, (123, 123))
		elif len(args) != 0:
			raise TypeError("Item.__init__ requires either 0 or "
					+ str(needed_dargs) + " arguments ("
					+ str(len(args)) + " given")

	def load_config_from_file(self, config_folder_name):
		config_folder = "./assets/API_elems/items/" + config_folder_name + "/"
		config_file = open(config_folder + "data.json")
		data = json.load(config_file)
		self.name = data["name"]
		self.orig_img = pygame.image.load(config_folder + data["icon_path"])
		self.img = pygame.transform.smoothscale(self.orig_img, (123, 123))
		directory = config_folder[2:].replace("/", ".") + "item"
		functions = importlib.import_module(directory)
		self.init = functions.init
		self.use = functions.use
		self.init(self, settings.player, settings.world, settings)

	def resize(self, new_size):
		self.img = pygame.transform.smoothscale(self.orig_img, new_size)
