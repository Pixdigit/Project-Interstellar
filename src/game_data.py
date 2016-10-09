# -*- coding: utf-8 -*-
import json
import os
import pygame
import sys
import traceback
from . import settings
from . import sounds
from . import objects


def save(name):

	name = name.encode("utf-8")
	# removes invalid characters
	if "/" in name:
		name = name.replace("/", "\\")
	if "%" in name:
		name = name.replace("%", "")

	if not os.path.isdir("./saves/%s/" % name):
		os.makedirs("./saves/%s/" % name)

	all_world_data = {}
	world_image = {}
	for world_name in settings.localmap:
		if not os.path.isdir("./saves/%s/%s" % (name, world_name)):
			os.makedirs("./saves/%s/%s" % (name, world_name))
		all_world_data[world_name] = {}
		all_world_data[world_name]["targets"] = list()
		all_world_data[world_name]["station"] = dict()
		for target in settings.localmap[world_name].targets:
			all_world_data[world_name]["targets"].append(target.unique_relevant_data())
		station_data = settings.localmap[world_name].warp1.unique_relevant_data()
		all_world_data[world_name]["station"] = station_data
		world_image[world_name] = settings.localmap[world_name].background

	data = {"fullscreen": settings.fullscreen,
		"screenx_current": settings.screenx_current,
		"screeny_current": settings.screeny_current,
		"debugmode": settings.debugmode,
		"debugscreen": settings.debugscreen,
		"player.rel_x": settings.player.rel_x,
		"player.rel_y": settings.player.rel_y,
		"sounds.music.volume": sounds.music.volume,
		"player.timeplay": settings.player.timeplay,
		"world.name": settings.world.name,
		"worlds": list(settings.localmap.keys())
		}

	settings_file = open("./saves/" + name + "/Data.json", "w")
	for world_name in settings.localmap:
		world_file = open("./saves/%s/%s/world.json" % (name, world_name), "w")
		pygame.image.save(world_image[world_name],
				"./saves/%s/%s/background.tga" % (name, world_name))
		json.dump(all_world_data[world_name], world_file, indent=12)
	json.dump(data, settings_file, indent=12)


def save_user_settings(**args):
	path = "./userdata/user_settings.json"
	settings_file = open(path, "w")
	json.dump(args, settings_file, indent=12)
	settings_file.close()


def load(name):
	"""Load savegame"""

	try:
		data = json.load(open("./saves/" + unicode(name) + "/Data.json", "r"))
		settings.fullscreen = data["fullscreen"]
		settings.screenx_current = data["screenx_current"]
		settings.screeny_current = data["screeny_current"]
		settings.debugmode = data["debugmode"]
		settings.debugscreen = data["debugscreen"]
		settings.player.rel_x = data["player.rel_x"]
		settings.player.rel_y = data["player.rel_y"]
		sounds.music.volume = data["sounds.music.volume"]
		settings.player.timeplay = data["player.timeplay"]
		world_names = data["worlds"]

		from . import worlds
		localmap = {}
		for world_name in world_names:
			background_dir = "./saves/%s/%s/background.tga" % (name, world_name)
			background = pygame.image.load(background_dir)
			world_data = json.load(open("./saves/%s/%s/world.json"
						% (name, world_name), "r"))
			localmap[world_name] = worlds.world(world_name)
			localmap[world_name].generate(background, settings.dstars, 0)
			for target_data in world_data["targets"]:
				tmp_target = objects.target()
				tmp_target.pos_xper = target_data["pos_xper"]
				tmp_target.pos_yper = target_data["pos_yper"]
				tmp_target.timer = target_data["timer"]
				tmp_target.update()
				localmap[world_name].targets.append(tmp_target)
			tmp_station = objects.warp_station()
			tmp_station.x_pos = world_data["station"]["x_pos"]
			tmp_station.y_pos = world_data["station"]["y_pos"]
			tmp_station.update()
			localmap[world_name].warp1 = tmp_station
		settings.localmap = localmap
		settings.world = localmap[data["world.name"]]
	except Exception:
		print(("Unexpected error:", sys.exc_info()[0]))
		print((traceback.format_exc()))


def load_user_settings():
	if os.path.exists("./userdata/user_settings.json"):
		settings_file = open("./userdata/user_settings.json", "r")
		setting = json.load(settings_file)
		settings_file.close()

		try:
			settings.volume = setting["volume"]
			sounds.music.volume = setting["volume"]
		except:
			pass
		try:
			settings.buttonmap = setting["buttonmap"]
		except:
			pass
	else:
		pass