# -*- coding: utf-8 -*-
import pygame
import time
import string
from . import settings
from . import menu
from . import sounds
from . import objects
from . import midi_in
from . import specials
from . import overlay_handler
from pygame.locals import QUIT, KEYUP, KEYDOWN


def init():
	pass
	#nothing to initialize

"""Handles user input"""


def handle():

	#If debugging is active, midi-events will be qued to event-list
	midi_in.do()

	#Translates events to actions or settings
	process_events()

	#Handles advanced interfaces
	specials.update()


def process_events():
	"""This function translates all events in settings.events to in-game Signals.

	It has no Arguments to pass and returns nothing."""

	for event in settings.events:
		#Close cross clicked etc.
		if event.type == QUIT:
			exit()
		#Deacitates the holding state of certain keys
		if event.type == KEYUP:
			key = pygame.key.name(event.key)
			if key == "x" or key == "y":
				settings.player.speedboost = 1
			if key in settings.buttonmap["up_key"]:
				settings.up = False
			if key in settings.buttonmap["down_key"]:
				settings.down = False
			if key in settings.buttonmap["left_key"]:
				settings.left = False
			if key in settings.buttonmap["right_key"]:
				settings.right = False
		#Handles keypresses
		if event.type == KEYDOWN:
			key = pygame.key.name(event.key)
			if key in settings.buttonmap["pause_key"]:
				menu.pause()
			if key in settings.buttonmap["debugscreen_key"]:
				settings.debugscreen = settings.toggle(settings.debugscreen, True, False)
			if key in settings.buttonmap["screenshot_key"]:
				filename = "./screenshots/screenshot" + time.strftime("^%d-%m-%Y^%H.%M.%S")
				pygame.image.save(settings.screen, filename + ".png")
			if key in settings.buttonmap["next_track_key"]:
				sounds.music.play("next")
			if key in settings.buttonmap["speeddown_key"]:
				settings.player.speedboost = 0.3
			if key in settings.buttonmap["speedup_key"]:
				settings.player.speedboost = 1.7
			if key in settings.buttonmap["up_key"]:
				settings.up = True
			if key in settings.buttonmap["down_key"]:
				settings.down = True
			if key in settings.buttonmap["left_key"]:
				settings.left = True
			if key in settings.buttonmap["right_key"]:
				settings.right = True
			if key == "o":
				if settings.player.pos.x >= 0.9 and settings.player.pos.y >= 0.9:
					pygame.mixer.music.load("./assets/music/$not$ard_tatort.ogg")
					pygame.mixer.music.play(1, 0.0)
			if key in settings.buttonmap["fire_key"]:
				tmp_bullet = objects.bullet(settings.player.rotation, settings.player.pos)
				settings.bullets.append(tmp_bullet)
			if key in settings.buttonmap["fire_circle_key"]:
				specials.fire = True
			#These are debugging relevant interfaces
			if settings.debugmode:
				#reloads the screen variables
				if key == "r":
					settings.world.adjust_to_screen()
				#Resets settings
				if key == "q":
					settings.init()
				#Toggles the psychomode
				if key == "p":
					settings.psycomode = settings.toggle(settings.psycomode, True, False)
				#Mutes all sounds
				if key == "q":
					settings.volume = 0
				#Changes ship
				if key == "n":
					settings.player.new_ship("ship_2")
				#Tags all targets as being shot
				if key == "t":
					for target in settings.world.targets:
						target.test_ishit(pygame.Rect((-10000, -10000), (30000, 30000)))
				#regenerates the world
				if key == "g":
					settings.localmap["1"].generate(settings.localmap["1"].background,
								settings.dstars, settings.dtargets)
					settings.world.generate(settings.world.background,
								settings.dstars, settings.dtargets)
				#Prints location of target
				if key == "h":
					for target in settings.world.targets:
						print((target.pos))
				if key == "i":
					overlay = overlay_handler.overlay.get_by_name("item_bar")
					old_status = overlay.active
					overlay.set_visability(not old_status)
				#change item location
				if key in [str(i + 1) for i in range(6)]:
					item_overlay = overlay_handler.overlay.get_by_name("item_bar")
					item = item_overlay.rm_sub("speed_boost")
					item_overlay.get_by_name("item_slot_" + key).set_sub(item)
				#Numpad presses
				#Switches between worlds
				if len(key) == 3:
					if key[0] == "[" and key[2] == "]":
						try:
							num = int(key[1])
							if num != 5:
								if num > 5:
									num -= 1
								settings.world = settings.localmap[str(num)]
						except ValueError:
							pass


def getall(allkeys):
	"""Gets all pressed keys"""
	#TODO: Find better use
	for event in settings.events:
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			key = pygame.key.name(event.key)
			tmp = (not key == "return" and not allkeys)
			if (event.unicode in string.printable or (key[:5] == "world")) and tmp:
				return event.unicode
			elif allkeys:
				return key
