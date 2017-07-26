# -*- coding: utf-8 -*-
import pygame
from pygame.locals import USEREVENT
from libs.pyganim import pyganim
import os
import shutil
import sys
import random
from . import iface
from . import constants as const


def init():

	#global up  # player should move up
	#global down  # player should move down
	#global left  # player should move left
	#global right  # player should move right
	#global konstspeed  # some konstant for speed
	global clock  # clock object of pygame
	#global stdfont  # global font defenition
	#global typeface  # the typeface...
	#global fullscreen  # determines current state if fullscreen or not
	#global fullscreenold  # used to check if fullscreen has changes
	global screen  # the screen
	#global screenx  # maximum x pixels
	#global screeny  # maximum y pixels
	global aspect_ratio  # aspect ratio
	#global screenx_current  # current x pixels
	#global screeny_current  # current y pixels
	global fake_size  # the ratio of screenx_current and size of the background
	global bullets  # list of all bullets
	global dstars  # amount of stars
	global debugscreen  # determines wether to show debug info
	global debugmode  # Enables debugmode
	global isnear  # easteregg
	#global background  # background image
	#global field  # image for the inputfield
	#global bullet_img  # image for the bullet
	#global targeton_img  # surf for target whenlight turned on
	#global targetoff_img  # surf for target when turned off
	#global border1  # A box to hold the status information about energy level
	#global item_bar_image  # The background for items in the itembar
	global code  # used for custom user events
	global events  # events
	global buttonmap  # dict containing the mapping of the userinputs
	global music  # the music playlist object
	#global color  # global color defenition
	global skip  # unsused (currently)
	global volume  # volume
	global musics  # the list of music titles assoziated wih the music files
	global saves  # all savegames
	global psycomode  # if psycomode is turned on
	#global explosions  # list of surfs of explosions
	global explosions_disp  # list of showing explosions
	#global run  # boolean for main loop
	#global dtargets  # amount of targets
	global morevents  # custom event logger
	#global infinitevents  # A event logger which retriggers as long as condition
	#global musicend  # custom event number to show that music ended
	global world  # a placeholder for the world class
	global objects_on_screen  # entitys currently blitted to screen
	global player  # abstract player class
	global localmap  # A dict of the local worlds
	#global loading_time  # time until first blit
	global seed  # the environments seed

	# for this operation os.urandom is used
	seed_size = 16
	seed = random.randint(10 ** (seed_size - 1), (10 ** seed_size) - 1)
	random.seed(seed)

	# set up screen
	pygame.event.set_grab(False)
	pygame.mouse.set_visible(False)

	iface.screen_conf["screenx"] = pygame.display.Info().current_w
	iface.screen_conf["screeny"] = pygame.display.Info().current_h
	screenx = iface.screen_conf["screenx"]
	screeny = iface.screen_conf["screeny"]
	aspect_ratio = screenx / float(screeny)
	#TODO: is this needed?
	iface.screen_conf["screenx_current"] = screenx
	iface.screen_conf["screenx_current"] = screeny

	#TODO: What does this do?
	pygame.display.set_mode((1, 1))


	# create empty folders if needed
	if not os.path.exists("./assets/sprites/player/"):
		os.makedirs("./assets/sprites/player/")
	if not os.path.exists("./screenshots/"):
		os.makedirs("./screenshots/")
	if not os.path.exists("./userdata/"):
		os.makedirs("./userdata/")


	#TODO: What is the clock good for?
	# define some konstants or default values
	clock = pygame.time.Clock()

	#TODO figure out how to restucture
	#up = False
	#down = False
	#left = False
	#right = False

	#TODO: Where do I move this?
	debugscreen = False
	debugmode = True

	#TODO WHAT?
	isnear = "False"
	code = ""

	#TODO Where?
	buttonmap = default_buttonmap()

	skip = False
	#TODO Define interface for this
	volume = 0.5

	#TODO What exactly is this? Put in constants
	fake_size = 8 / 7.0

	#TODO What and Where? | Maybe infinitevents?
	psycomode = False

	#TODO Check if this is still ok-isch practise
	morevents = []

	#TODO Make this part of the world interface
	bullets = []

	#TODO why is this even needed?
	loading_time = 0

	fullscreen = iface.screen_conf["fullscreen"]
	if fullscreen:
		iface.screen_conf["screen"] = pygame.display.set_mode(  (0, 0),
																pygame.FULLSCREEN,
																32)
	else:
		scale_factor = 0.9
	 	screenx_current = int(iface.screen_conf["screenx"] * scale_factor)
		screeny_current = int(screenx_current * 9.0 / 16)
		iface.screen_conf["screen"] = pygame.display.set_mode((screenx_current, screeny_current))
		iface.screen_conf["screenx_current"] = screenx_current
		iface.screen_conf["screenx_current"] = screeny_current


	pygame.display.set_caption("Project Interstellar " + const.version)
	pygame.display.set_icon(pygame.image.load("./assets/sprites/logo.png"))

	if const.debugmode:
		iface.sound_conf["volume"] = 0.0
		fullscreen = False

	#TODO DO THIS RIGHT
	explosions_disp = []

	#TODO make long due change to upd
	upd("get_saves")

	old_img_size = const.item_bar_image.get_size()
	new_x_size = iface.sound_conf["screenx_current"] / 3
	new_y_size = int(old_img_size[1] * (float(new_x_size) / old_img_size[0]))
	item_bar_image = pygame.transform.smoothscale(item_bar_image,
					(new_x_size, new_y_size))

	from .player import player as create_player
	player = create_player()

	from . import worlds
	localmap = {}
	for a in range(8):
		world = worlds.world(str(a + 1))
		world.generate(background, dstars, dtargets)
		localmap[str(a + 1)] = world
	world = localmap["1"]
	upd("adjust_screen")

	#scales images so they fill screen especially when not 16/9 ar
	if aspect_ratio > 16.0 / 9:
		ratio = screenx_current / float(background.get_size()[1])
		pygame.transform.smoothscale(background,
					(screenx_current, int(screeny_current * ratio)))
	elif aspect_ratio < 16.0 / 9:
		ratio = screeny_current / float(background.get_size()[0])
		pygame.transform.smoothscale(background,
					(int(screenx_current * ratio), screeny_current))


def reset():

	"""resets some settings"""
	global konstspeed
	global color

	pygame.event.set_grab(False)
	pygame.mouse.set_visible(False)

	player.reset()

	konstspeed = 0.0025
	color = (255, 255, 10)

	time("start")

	if debugmode:
		fullscreen = False

	world.generate(world.background, dstars, dtargets)


def upd(level):

	"""updates various variables"""
	if level == "get_events":
		global events
		events = pygame.fastevent.get()
		return
	if level == "screenvalues":
		global screenx_current
		global screeny_current
		global aspect_ratio
		screenx_current = pygame.display.Info().current_w
		screeny_current = pygame.display.Info().current_h
		aspect_ratio = screenx_current / float(screeny_current)
		return
	if level == "get_saves":
		global saves
		saves = []
		for elem in os.listdir("./saves/"):
			if os.path.isdir("./saves/" + elem):
				saves.append(elem)
		return
	if level == "adjust_screen":
		global background
		global background_pos
		global konstspeed
		global fullscreen
		#lint:disable
		if fullscreen:
			pygame.display.set_mode((screenx, screeny), pygame.FULLSCREEN)
		if not fullscreen:
		#lint:enable
			pygame.display.set_mode((screenx_current, screeny_current))

		upd("screenvalues")

		konstspeed = 0.0025
		konstspeed = konstspeed * (screenx_current / 1920.0)

		world.adjust_to_screen()  # lint:ok

		#scales images so they fill screen especially when not 16/9 ar
		if aspect_ratio > 16.0 / 9:
			#lint:disable
			ratio = screenx_current / float(background.get_size()[1])
			pygame.transform.smoothscale(background,
			#lint:enable
						(screenx_current, int(screeny_current * ratio)))
		elif aspect_ratio < 16.0 / 9:
			#lint:disable
			ratio = screeny_current / float(background.get_size()[0])
			pygame.transform.smoothscale(background,
			#lint:enable
						(int(screenx_current * ratio), screeny_current))

		return
	print("Something went wrong here")
	raise Exception


def toggle(var, option1, option2):
	# toggles between option1 and 2 and retunr var, saves some space
	if var == option1:
		var = "yep"
	if var == option2:
		var = option1
	if var == "yep":
		var = option2
	return var


def quit():
	"""Routine for exiting"""
	from . import midi_in
	midi_in.quit()
	pygame.quit()
	shutil.rmtree('./assets/sprites/player')
	sys.exit()


def time(action):
	global oldtime
	global newtime
	if not "newtime" in globals():
		newtime = pygame.time.get_ticks()
	if action == "pause":
		oldtime = newtime
		newtime = pygame.time.get_ticks()
		player.timeplay += newtime - oldtime
	if action == "start":
		oldtime = pygame.time.get_ticks()
		newtime = pygame.time.get_ticks()
	if action == "get_time":
		return pygame.time.get_ticks() - oldtime + player.timeplay


def default_buttonmap():
	"""generates the Default Buttonmap, when adding default Values
	use your specified name as key and the corresponding pygame.event key(s)
	in a list as value(s) to the buttons dict"""
	buttons = {}

	buttons["speedup_key"] = ["y", "not_set"]
	buttons["speeddown_key"] = ["x", "not_set"]
	buttons["up_key"] = ["w", "up"]
	buttons["down_key"] = ["s", "down"]
	buttons["left_key"] = ["a", "left"]
	buttons["right_key"] = ["d", "right"]
	buttons["pause_key"] = ["escape", "not_set"]
	buttons["debugscreen_key"] = ["f3", "not_set"]
	buttons["screenshot_key"] = ["f12", "not_set"]
	buttons["next_track_key"] = ["f6", "not_set"]
	buttons["fire_key"] = ["space", "f"]
	buttons["fire_circle_key"] = ["left shift", "c"]

	return buttons
