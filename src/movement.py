# -*- coding: utf-8 -*-
from . import settings

"""This handles the movement of nearly everything"""


def init():
	"""Initzializing variables"""
	global background_pos
	global draw

	background_pos = settings.world.background_pos
	background_pos.left = -(settings.player.pos.left / 7.0) - 1
	background_pos.top = -(settings.player.pos.top / 7.0) - 1


def handle():
	"""Handle movement"""

	settings.world.move()
	settings.player.move()
