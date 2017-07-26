# -*- coding: utf-8 -*-
from . import settings
from . import busses
from . import constants
from libs import clock

"""This handles the movement of nearly everything"""


def init():
	"""Initzializing variables"""
	busses.schedules_bus["physics"] = clock.schedule(handle, constants.pyhsics_update_delay)


def handle():
	"""Handle movement"""

	settings.world.move()
	settings.player.move()
