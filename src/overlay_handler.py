# -*- coding: utf-8 -*-
from . import settings
from . import overlay_elements

global overlay


def init():
	global overlay
	overlay = overlay_elements.item_bar_creator("item_bar")
	overlay.set_visability(True)


def blit():
	global overlay
	overlay.blit(settings.screen, (0, 0, 0, 0))  # lint:ok
