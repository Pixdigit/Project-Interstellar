# -*- coding: utf-8 -*-
import pygame
from pygame.locals import USEREVENT
from libs.pyganim import pyganim
import os
import shutil
import sys
import random


def init():

	global up  # player should move up
	global down  # player should move down
	global left  # player should move left
	global right  # player should move right
	global konstspeed  # some konstant for speed
	global clock  # clock object of pygame
	global stdfont  # global font defenition
	global typeface  # the typeface...
	global fullscreen  # determines current state if fullscreen or not
	global fullscreenold  # used to check if fullscreen has changes
	global screen  # the screen
	global screenx  # maximum x pixels
	global screeny  # maximum y pixels
	global aspect_ratio  # aspect ratio
	global screenx_current  # current x pixels
	global screeny_current  # current y pixels
	global fake_size  # the ratio of screenx_current and size of the background
	global bullets  # list of all bullets
	global dstars  # amount of stars
	global debugscreen  # determines wether to show debug info
	global debugmode  # Enables debugmode
	global isnear  # easteregg
	global background  # background image
	global field  # image for the inputfield
	global bullet_img  # image for the bullet
	global targeton_img  # surf for target whenlight turned on
	global targetoff_img  # surf for target when turned off
	global border1  # A box to hold the status information about energy level
	global item_bar_image  # The background for items in the itembar
	global code  # used for custom user events
	global events  # events
	global music  # the music playlist object
	global color  # global color defenition
	global skip  # unsused (currently)
	global volume  # volume
	global musics  # the list of music titles assoziated wih the music files
	global saves  # all savegames
	global psycomode  # if psycomode is turned on
	global explosions  # list of surfs of explosions
	global explosions_disp  # list of showing explosions
	global run  # boolean for main loop
	global dtargets  # amount of targets
	global morevents  # custom event logger
	global infinitevents  # A event logger which retriggers as long as condition
	global musicend  # custom event number to show that music ended
	global world  # a placeholder for the world class
	global objects_on_screen  # entitys currently blitted to screen
	global player  # abstract player class
	global localmap  # A dict of the local worlds
	global loading_time  # time until first blit
	global seed  # the environments seed

	# for this operation os.urandom is used
	seed_size = 16
	seed = random.randint(10 ** (seed_size - 1), (10 ** seed_size) - 1)
	random.seed(seed)

	# set up screen
	pygame.event.set_grab(False)
	pygame.mouse.set_visible(False)

	screenx = pygame.display.Info().current_w
	screeny = pygame.display.Info().current_h
	pygame.display.set_mode((1, 1))
	aspect_ratio = screenx / float(screeny)
	screenx_current = screenx
	screeny_current = screeny

	# create empty folders if needed
	if not os.path.exists("./assets/sprites/player/"):
		os.makedirs("./assets/sprites/player/")
	if not os.path.exists("./screenshots/"):
		os.makedirs("./screenshots/")

	# load images and convert them to the fatest blittable format
	background = pygame.image.load("./assets/sprites/Background2.tif").convert()
	field = pygame.image.load("./assets/sprites/inputbox1.tif").convert_alpha()
	bullet_img = pygame.image.load("./assets/sprites/Bullet.tif").convert_alpha()
	targeton_img = pygame.image.load("./assets/sprites/mine_on.tif"
				).convert_alpha()
	targetoff_img = pygame.image.load("./assets/sprites/mine_off.tif"
				).convert_alpha()
	border1 = pygame.image.load("./assets/sprites/bar1.tif").convert_alpha()
	item_bar_image = pygame.image.load("./assets/sprites/item_bar.tif")

	# define some konstants or default values
	clock = pygame.time.Clock()
	typeface = "monospace"
	stdfont = pygame.font.SysFont(typeface, 15)

	version = "0.3.3.1 dev"
	up = False
	down = False
	left = False
	right = False
	konstspeed = 0.0025
	fullscreen = False
	debugscreen = False
	debugmode = True
	dstars = 500
	isnear = "False"
	code = ""
	events = []
	color = (255, 255, 10)
	skip = False
	volume = 0.5
	fullscreenold = False
	fake_size = 8 / 7.0
	psycomode = False
	run = True
	dtargets = 5
	morevents = []
	bullets = []
	infinitevents = {"fire1": False, "roundfire": False}
	musicend = USEREVENT + 100
	events = []
	loading_time = 0

	if fullscreen:
		screen = pygame.display.set_mode(
			(screenx_current, screeny_current),
			pygame.FULLSCREEN, 32)
	if not fullscreen:
		screenx_current = int(screenx_current * 0.9)
		screeny_current = int(screenx_current * 9.0 / 16)
		screen = pygame.display.set_mode((screenx_current, screeny_current),
		0, 32)

	pygame.display.set_caption("Project Interstellar " + version)
	pygame.display.set_icon(pygame.image.load("./assets/sprites/logo.png"))

	# more complex default settings like creation of stars and targets and so on
	if debugmode:
		# Add custom handler here for when debugmode is activated
		volume = 0.0
		# fullscreen = False
		pass

	explosions_disp = []
	explosions = []
	for a in range(3):
		this_width = 128
		this_height = 128
		if a == 2:
			this_width = 96
			this_height = 96
		num = str(a + 9)
		if a == 0:
			num = "0" + num
		explosion_files = pyganim.getImagesFromSpriteSheet(
							"./assets/sprites/explosions/expl_" + num + ".png",
							width=this_width, height=this_height)
		explosion_attr = [(anim_file, 40) for anim_file in explosion_files]
		explosions.append(pyganim.PygAnimation(explosion_attr, loop=False))

	upd("get_saves")

	old_img_size = item_bar_image.get_size()
	new_x_size = screenx_current / 3
	new_y_size = int(old_img_size[1] * (float(new_x_size) / old_img_size[0]))
	item_bar_image = pygame.transform.smoothscale(item_bar_image,
					(new_x_size, new_y_size))

	from .player import player as player
	player = player()

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

	player.reset()  # lint:ok

	konstspeed = 0.0025
	color = (255, 255, 10)

	from . import missions
	missions.time("start")

	if debugmode:  # lint:ok
		fullscreen = False  # lint:ok

	world.generate(world.background, dstars, dtargets)  # lint:ok


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
