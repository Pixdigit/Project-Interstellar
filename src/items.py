# -*- coding: utf-8 -*-
import pygame
import json
import importlib
import settings
from libs import overlay
from . import overlay_handler


def init():
	overlay_handler.overlay.get_by_name("item_slot_1"
				).set_sub(new_item("speed_boost"))
	overlay_handler.overlay.update()


class new_item(overlay.elements.overlay_element, object):

	def __init__(self, config_file):
		self.proto = super(new_item, self)
		self.pos = pygame.Rect(0, 0, 0, 0)
		self.load_config_from_file(config_file)
		self.proto.__init__(self.name, self.pos_getter, img=self.img)
		self.resize(overlay_handler.overlay.get_by_name("item_slot_1").pos.size)

	def pos_getter(self):
		if self.name in [elem.name for elem in overlay_handler.overlay.get_sub()]:
			self.pos.center = (overlay_handler.overlay.get_upper(
					self.name).pos.width / 2,) * 2

	def load_config_from_file(self, config_folder_name):
		config_folder = "./assets/API_elems/items/" + config_folder_name + "/"
		config_file = open(config_folder + "data.json")

		data = json.load(config_file)

		self.name = data["name"]

		self.orig_img = pygame.image.load(config_folder + data["icon_path"])
		self.resize(self.orig_img.get_size())

		directory = config_folder[2:].replace("/", ".") + "item"
		functions = importlib.import_module(directory)
		self.init = functions.init
		self.use = functions.use
		self.init(self, settings.player, settings.world, settings)

	def resize(self, new_size):
		self.img = pygame.transform.smoothscale(self.orig_img, new_size)
		self.pos.size = self.img.get_size()

	def blit(self, screen, rel_pos):
		self.update()
		self.proto.blit(screen, rel_pos)
