# -*- coding: utf-8 -*-
import pygame
import json
import importlib
import settings
from libs import overlay
from . import overlay_elements


def init():
	overlay_elements.item_bar.get_by_name("item_slot_1"
				).set_sub(new_item("speed_boost"))


class new_item(overlay.elements.overlay_element, object):

	def __init__(self, config_file):
		self.proto = super(new_item, self)
		self.load_config_from_file(config_file)
		self.proto.__init__(self.name, lambda old_pos: self.pos, img=self.img)

	def load_config_from_file(self, config_folder_name):
		config_folder = "./assets/API_elems/items/" + config_folder_name + "/"
		config_file = open(config_folder + "data.json")

		data = json.load(config_file)

		self.name = data["name"]

		self.orig_img = pygame.image.load(config_folder + data["icon_path"])
		self.resize((120, 120))

		directory = config_folder[2:].replace("/", ".") + "item"
		functions = importlib.import_module(directory)
		self.init = functions.init
		self.use = functions.use
		self.init(self, settings.player, settings.world, settings)

	def resize(self, new_size):
		self.img = pygame.transform.smoothscale(self.orig_img, new_size)

	def blit(self, screen):
		self.pos.center = screen.get_rect().center
		screen.blit(self.img, self.pos)
