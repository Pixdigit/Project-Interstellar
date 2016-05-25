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
from pygame.locals import QUIT, KEYUP, KEYDOWN


def init():
	pass
	#nothing to initialize

"""Handles user input"""


def handle():

	# handles user input
	#TODO: Add docs

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
			if key == "w" or key == "up":
				settings.up = False
			if key == "s" or key == "down":
				settings.down = False
			if key == "a" or key == "left":
				settings.left = False
			if key == "d" or key == "right":
				settings.right = False
		#Handles keypresses
		if event.type == KEYDOWN:
			key = pygame.key.name(event.key)
			if key == "escape":
				menu.pause()
			if key == "f3":
				settings.debugscreen = settings.toggle(settings.debugscreen, True, False)
			if key == "f12":
				filename = "./screenshots/screenshot" + time.strftime("^%d-%m-%Y^%H.%M.%S")
				pygame.image.save(settings.screen, filename + ".png")
			if key == "f6":
				sounds.music.play("next")
			if key == "x":
				settings.player.speedboost = 0.3
			if key == "y":
				settings.player.speedboost = 1.7
			if key == "w" or key == "up":
				settings.up = True
			if key == "s" or key == "down":
				settings.down = True
			if key == "a" or key == "left":
				settings.left = True
			if key == "d" or key == "right":
				settings.right = True
			if key == "o":
				if settings.player.pos.x >= 0.9 and settings.player.pos.y >= 0.9:
					pygame.mixer.music.load("./assets/music/$not$ard_tatort.ogg")
					pygame.mixer.music.play(1, 0.0)
			if key == "f" or key == "space":
				tmp_bullet = objects.bullet(settings.player.rotation, settings.player.pos)
				settings.bullets.append(tmp_bullet)
			if key == "c":
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
				#Numpad presses
				#Switches between worlds
				if len(key) == 3 and settings.debugmode:
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
