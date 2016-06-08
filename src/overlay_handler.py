# -*- coding: utf-8 -*-
from . import settings
from libs.overlay import overlay as overlay_creator
from . import items
from . import overlays

global overlay
if not "overlay" in globals():
	overlay = None


def init():
	global overlay

	overlay = overlay_creator.create_overlay()

	overlay_elem_pos = (settings.screenx_current / 2, settings.screeny_current)
	overlay_obj = overlays.item_bar("items", overlay_elem_pos, "midbottom")
	tmp_item = items.new_item()
	tmp_item.load_config_from_file("speed_boost")
	overlay_obj.set_item(0, tmp_item)
	overlay_obj.set_image(settings.item_bar_image)

	overlay.add_overlay_element(overlay_obj)

	overlay.activate()


def blit():
	global overlay
	overlay.blit(settings.screen)
