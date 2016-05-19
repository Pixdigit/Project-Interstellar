# -*- coding: utf-8 -*-
from libs.overlay import overlay_handler
from src import settings


class create_overlay(overlay_handler.create_overlay):
	pass


class create_overlay_object(overlay_handler.create_overlay_object):

	def update(self):
		try:
			text = "World: " + str(settings.world.name)
		except AttributeError:
			# Initializing so world does not exist yet
			text = "World: 1"
		self.load_text(text, settings.typeface, 50, settings.color)