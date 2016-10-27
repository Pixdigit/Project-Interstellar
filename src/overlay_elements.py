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
		size = settings.screenx_current * 0.07
		old_pos.size = (size, size)
		old_pos.topleft = (no * size, 0)
		return old_pos
	return pos


class item_bar_creator(overlay.elements.overlay_element, object):

	def __init__(self, name):
		#TODO find way to get own pos_getter to init func
		self.proto = super(item_bar_creator, self)
		self.proto.__init__(name)
		for i in range(6):
			self.create_sub(i, subclass=item_slot)

	def pos_getter(self):
		print "OK"
		exit()
		height = int(0.11 * settings.screeny_current)
		self.pos.size = (height * 6, height)
		self.pos.bottom = settings.screeny_current
		self.pos.centerx = settings.screenx_current / 2


class item_slot(overlay.elements.overlay_element, object):

	def __init__(self, number):
		self.proto = super(item_slot, self)
		self.slot_nr = number
		self.proto.__init__("item_slot_" + str(number + 1), self.pos_getter,
				img="./assets/sprites/item_bar.tif")

	def pos_getter(self):
		#TODO SET UPPER ELEMENT
		upper = None
		#self.pos.size = (upper.pos.height,) * 2
		self.pos.top = 0
		self.pos.left = (self.slot_nr * self.pos.width)


def init():
	global item_bar
	global item_slot_1
	global item_slot_2
	global item_slot_3
	global item_slot_4
	global item_slot_5
	global item_slot_6

	#item_bar = overlay.elements.overlay_element("item_bar", item_bar_pos)
	#item_slot_1 = item_bar.create_sub("item_slot_1", slot_pos(0),
	#			"./assets/sprites/item_bar.tif")
	#item_slot_2 = item_bar.create_sub("item_slot_2", slot_pos(1),
				#"./assets/sprites/item_bar.tif")
	#item_slot_3 = item_bar.create_sub("item_slot_3", slot_pos(2),
				#"./assets/sprites/item_bar.tif")
	#item_slot_4 = item_bar.create_sub("item_slot_4", slot_pos(3),
				#"./assets/sprites/item_bar.tif")
	#item_slot_5 = item_bar.create_sub("item_slot_5", slot_pos(4),
				#"./assets/sprites/item_bar.tif")
	#item_slot_6 = item_bar.create_sub("item_slot_6", slot_pos(5),
				#"./assets/sprites/item_bar.tif")
