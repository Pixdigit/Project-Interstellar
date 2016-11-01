# -*- coding: utf-8 -*-
from . import settings
from . import overlay_elements

global overlay


def init():
	global overlay
	global status_overlay
	overlay = overlay_elements.item_bar_creator("item_bar")
	status_overlay = overlay_elements.status_bar()
	overlay.set_visability(True)
	status_overlay.set_visability(True)


def blit():
	global overlay
	global status_overlay
	overlay.blit(settings.screen, (0, 0, 0, 0))  # lint:ok
	status_overlay.blit(settings.screen)  # lint:ok
