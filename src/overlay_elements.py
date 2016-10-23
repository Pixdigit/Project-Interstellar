# -*- coding: utf-8 -*-
import libs.overlay as overlay
from . import settings


def item_bar_pos(old_pos):
	old_pos.size = (124 * 6 + 4, 128)
	old_pos.bottom = settings.screeny_current
	old_pos.centerx = settings.screenx_current / 2
	return old_pos


def slot_pos(no):
	def pos(old_pos):
		old_pos.size = (128, 128)
		old_pos.topleft = (no * 124, 0)
		return old_pos
	return pos


def init():
	global item_bar
	global item_slot_1
	global item_slot_2
	global item_slot_3
	global item_slot_4
	global item_slot_5
	global item_slot_6

	item_bar = overlay.elements.overlay_element("item_bar", item_bar_pos)
	item_slot_1 = item_bar.create_sub("item_slot_1", slot_pos(0),
				"./assets/sprites/item_bar.tif")
	item_slot_2 = item_bar.create_sub("item_slot_2", slot_pos(1),
				"./assets/sprites/item_bar.tif")
	item_slot_3 = item_bar.create_sub("item_slot_3", slot_pos(2),
				"./assets/sprites/item_bar.tif")
	item_slot_4 = item_bar.create_sub("item_slot_4", slot_pos(3),
				"./assets/sprites/item_bar.tif")
	item_slot_5 = item_bar.create_sub("item_slot_5", slot_pos(4),
				"./assets/sprites/item_bar.tif")
	item_slot_6 = item_bar.create_sub("item_slot_6", slot_pos(5),
				"./assets/sprites/item_bar.tif")
