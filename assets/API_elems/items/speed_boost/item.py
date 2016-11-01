# -*- coding: utf-8 -*-


#TODO: API concept


def init(self, player, world, settings):
	global player_obj
	player_obj = player


def use(self):
	global player_obj
	player_obj.speed *= 2.0

def unuse(self):
	global player_obj
	palyer_obj.speed /= 2.0
