# -*- coding: utf-8 -*-
from . import settings
from . import namings
from . import sounds
from . import missions
from . import game_data
from libs.pyganim import pyganim
import pygame
from libs import menu
from pygame.locals import QUIT, USEREVENT, KEYDOWN

"""Responsible tor the menus"""


class fade_screen():

	def __init__(self, step, step2, max_alpha, screenx, screeny):
		self.fade = pygame.Surface((screenx, screeny))
		self.fade.fill((0, 0, 0))
		self.fade.set_alpha(0)
		self.timer = pygame.time.get_ticks()
		self.alpha = 0
		self.max_alpha = max_alpha
		self.step = step
		self.step2 = step2

	def blit(self, screen):
		time = pygame.time.get_ticks()
		if (time - self.timer) > self.step and self.alpha <= self.max_alpha:
			self.timer = pygame.time.get_ticks()
			self.alpha += self.step2
		self.fade.set_alpha(self.alpha)
		screen.blit(self.fade, pygame.Rect(0, 0, 0, 0))

	def update(self, screenx, screeny):
		self.__init__(self.step, self.max_alpha, screenx, screeny)


class menu_template():

	def __init__(self, menu_name, fade_step, fade_step2, fade_max,
			variables, externals):
		"""Initialize menu"""

		# import variables
		self.screenx = settings.screenx_current
		self.screeny = settings.screeny_current
		self.screen = settings.screen
		self.fade_step = fade_step
		self.fade_max = fade_max
		self.variables = variables
		self.externals = externals
		self.menu_name = menu_name
		self.fade_step2 = fade_step2

		# set mouse visible
		pygame.mouse.set_visible(True)

		# create menu
		self.menu = menu.create_menu(
					"./assets/templates/" + self.menu_name + ".json",
					pygame.Rect((0, 0), (self.screenx, self.screeny)), lambda: variables)

		# create fade effect
		#fade = fade_screen(self.fade_step, self.fade_step2, self.fade_max,
		#		self.screenx, self.screeny)
#		self.menu.elems["externals"] = [fade]

#		for elem in self.externals:
#			self.menu.elems["externals"].insert(0, elem)

	class slider_post():
		"""A class for posting sliders and including their value
		as a float representative of the class. When the Class is compared
		it will compare the sliders name and return the result."""
		def __init__(self, name, value):
			self.name = name
			self.value = value

		def __eq__(self, other):
			return self.name == other

		def __float__(self):
			return float(self.value)

		def __int__(self):
			return int(self.value)

		def __nonzero__(self):
			try:
				return bool(int(self.value))
			except:
				raise ValueError(
					"Could not convert {0} to bool: {1}".format(type(self.value), self.value))

		def __bool__(self):
			return self.__nonzero__()

	def run(self):

		settings.upd("get_events")
		self.screen.fill((0, 0, 0))
		self.menu.blit(self.screen)
		self.menu.update(settings.events)
		sounds.music.update(events=settings.events)

		events = []
		for event in settings.events:
			if event.type == QUIT:
				pygame.mouse.set_visible(False)
				events.append("event.EXIT")
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					pygame.mouse.set_visible(False)
					events.append("event.QUIT")
				if key in ["return", "enter"]:
					pygame.mouse.set_visible(False)
					events.append("event.CONTINUE")
				events.append(key)
			if event.type == USEREVENT and event.code == "MENU":
				klicked = self.menu.get_klicked()
				for elem in klicked:
					elem.klicked = False
					events.append(elem.name)
		for slider in self.menu.get_types("slider"):
			if slider.dragged:
				tmp_value = slider.value
				tmp_event = self.slider_post(slider.name, tmp_value)
				events.append(tmp_event)
		return(events)

	def update(self):
		for external in self.externals:
			external.update(settings.screenx_current, settings.screeny_current)
		self.__init__(self.menu_name, self.fade_step, self.fade_step2, self.fade_max,
				self.variables, self.externals)


def main():
	"""main menu"""

	# create the planets animation
	class create_planet():

		def __init__(self, screenx, screeny):
			planet_sprite_part1 = pyganim.getImagesFromSpriteSheet(
								"./assets/sprites/spinning_planet/planet_part-0.png",
								width=384, height=384)
			planet_sprite_part2 = pyganim.getImagesFromSpriteSheet(
								"./assets/sprites/spinning_planet/planet_part-1.png",
								width=384, height=384)
			planet_sprite_part3 = pyganim.getImagesFromSpriteSheet(
								"./assets/sprites/spinning_planet/planet_part-2.png",
								width=384, height=384)
			planet_sprite_part4 = pyganim.getImagesFromSpriteSheet(
								"./assets/sprites/spinning_planet/planet_part-3.png",
								width=384, height=384)
			planet_sprite_part5 = pyganim.getImagesFromSpriteSheet(
								"./assets/sprites/spinning_planet/planet_part-4.png",
								width=384, height=384)
			planet_sprite = (planet_sprite_part1 + planet_sprite_part2
					+ planet_sprite_part3 + planet_sprite_part4
					+ planet_sprite_part5)
			planet_sprite_and_attr = [(anim_file, 65) for anim_file in planet_sprite]
			planet = pyganim.PygAnimation(planet_sprite_and_attr)
			planet.scale((int(0.2 * screenx), int(0.2 * screenx)))
			planet_pos = pygame.Rect((0, 0), (384, 384))
			self.planet_pos = planet_pos.move(int(screenx * 0.7), int(screeny * 0.4))
			planet.play()
			self.planet = planet

		def blit(self, screen):
			self.planet.blit(screen, self.planet_pos)

		def update(self, screenx, screeny):
			self.__init__(screenx, screeny)
	planet = create_planet(settings.screenx_current, settings.screeny_current)

	# Load menu
	main_menu = menu_template("main", 70, 1, 100, {}, [planet])

	# inserts menu music
	sounds.music.queue("$not$menue.ogg", 0)
	sounds.music.play("stop")
	sounds.music.play("play", -1)

	# Define loading time on first call
	if settings.loading_time == 0:
		settings.loading_time = pygame.time.get_ticks()
	run = True

	# Menu loop
	while run:

		#TODO: Remove this
		clock = settings.clock
		clock.tick()
		fps = clock.get_fps()
		pygame.display.set_caption("FPS: " + str(fps))

		# Calling events and checking through events
		events = main_menu.run()
		for event in events:
			if event == "event.CONTINUE":
				run = False
			if event == "start":
				settings.reset()
				sounds.music.play("next")
				run = False
			if event == "load":
				savegame = savegames()
				if savegame is not None:
					game_data.load(savegame)
					settings.player.move_rel()
					sounds.music.play("next", 0)
					settings.upd("get_saves")
					settings.upd("adjust_screen")
					run = False
				else:
					pygame.mouse.set_visible(True)
			if event == "settings":
				options()
				main_menu.update()
			if event == "credits":
				namings.run()
			if event in ["exit", "event.EXIT", "event.QUIT"]:
				settings.quit()
		pygame.display.flip()
	sounds.music.play("next", 0)
	pygame.mouse.set_visible(False)


def pause():
	"""pausing menu"""

	missions.time("pause")
	sounds.music.play("pause")
	pygame.mouse.set_visible(True)

	pause_menu = menu_template("pause", 5, 5, 150, {}, [])

	run = True

	while run:

		events = pause_menu.run()
		for event in events:
			if event in ["event.CONTINUE", "continue"]:
				sounds.music.play("unpause")
				run = False
			if event == "save":
				savename = inputpopup(settings.screenx_current / 2,
						settings.screeny_current / 2,
						"Save Game")
				if savename != "Exit":
					game_data.save(savename)
				settings.upd("get_saves")
			if event == "load":
				savegame = savegames()
				if savegame is not None:
					game_data.load(savegame)
					sounds.music.play("unpause")
					settings.upd("get_saves")
					settings.upd("adjust_screen")
					run = False
				else:
					pygame.mouse.set_visible(True)
			if event == "settings":
				options()
				pause_menu.update()
			if event in ["exit", "event.EXIT", "event.QUIT"]:
				main()
				run = False
		pygame.display.flip()
	pygame.mouse.set_visible(False)
	missions.time("start")


def choose_world():
	"""Selecting warp to move to."""

	sounds.music.play("pause")
	pygame.mouse.set_visible(True)

	preview_images = []
	tmpfont = pygame.font.SysFont("monospace", 13)
	for tmp in range(8):
		preview_size = (int(settings.screenx_current / 5.0),
				int(settings.screeny_current / 5.0))
		surf = settings.localmap[str(tmp + 1)].background
		surf = pygame.transform.smoothscale(surf, preview_size)
		text = tmpfont.render("world" + str(tmp + 1), True, settings.color)
		tmprect = text.get_rect()
		tmprect.center = surf.get_rect().center
		surf.blit(text, tmprect)
		preview_images.append(surf)
	world_menu = menu_template("world", 5, 5, 150, {
				"image1": preview_images[0],
				"image2": preview_images[1],
				"image3": preview_images[2],
				"image4": preview_images[3],
				"image5": preview_images[4],
				"image6": preview_images[5],
				"image7": preview_images[6],
				"image8": preview_images[7]}, {})

	pos_data = {
		"pos_rel_obj": "master_screen",
		"from": "TopLeft",
		"to": "TopLeft",
		"x_abs": 0,
		"x_rel": 0,
		"y_abs": 0,
		"y_rel": 0
		}
	background = menu.creator.disp_elem.image("background", settings.screen.copy(),
					pos_data, layer=0)
	world_menu.menu.objects.append(background)
	selected = -1

	run = True

	while run:
		events = world_menu.run()
		for event in events:
			if event in ["event.CONTINUE", "warp"]:
				sounds.music.play("unpause")
				run = False
			if event in ["return", "event.QUIT"]:
				selected = -1
				run = False
			if event in ["event.EXIT"]:
				settings.quit()
			if event[0:5] == "world":
				selected = event[-1]

		pygame.display.flip()

	pygame.mouse.set_visible(False)
	sounds.music.play("unpause")
	return selected


def inputpopup(x, y, header):
	"""Method for having an inputfield or selecting savegame"""
	# as said takes and input and returns a string or returns
	# savegame if header is saying so

	screen = settings.screen
	fade = pygame.Surface((settings.screenx_current, settings.screeny_current))
	fade.fill((0, 0, 0, 255))
	fade_pos = fade.get_rect()

	infield1 = menu.disp_elem.input_field(x, y, header,
					settings.typeface, settings.color, settings.field)
	screen.blit(fade, fade_pos)

	run = True

	while run:

		screen.blit(fade, fade_pos)

		if header == "Load Game":
			text = savegames()
			return text
		settings.upd("get_events")

		text = infield1.gettext(settings.events)

		for event in settings.events:
			if event.type == KEYDOWN:
				if pygame.key.name(event.key) == "escape":
					return "Exit"

		infield1.blit(screen)
		pygame.display.flip()

		if text is not None:
			run = False

	return text


def savegames():
	"""Menu to select a saved game."""

	# Loads in values
	list_of_saves = settings.saves
	D_saves = len(list_of_saves)
	currently_selected = 0

	if len(list_of_saves) == 0:
		print(("No current savegames"))
		return None

	# Defines Menu
	settings_menu = menu_template("load", 0, 255, 255,
			{"savename": list_of_saves[currently_selected]},
			[])

	run = True
	while run:

		# Get all events and handle them
		events = settings_menu.run()
		for event in events:
			# Exits savegame menu
			if event in ["event.EXIT", "event.QUIT", "return"]:
				run = False
				return None
			# Sets the current selected savegame to load
			if event == "load":
				return list_of_saves[currently_selected]
			# Shows next savegame
			if event == "next":
				# Points to an later save
				currently_selected += 1
				# Wraps to the beginning to create a not ending loop
				if currently_selected + 1 > D_saves:
					currently_selected = currently_selected - D_saves
				settings_menu = menu_template("load", 0, 255, 255,
						{"savename": list_of_saves[currently_selected]},
						[])
				# Lets the button last longer in klicked mode
				pygame.time.delay(50)
			# Shows previous savegame
			if event == "previous":
				# Points to an earlier save
				currently_selected -= 1
				# Wraps to the end to create a not ending loop
				if currently_selected < 0:
					currently_selected = D_saves + currently_selected
				settings_menu = menu_template("load", 0, 255, 255,
						{"savename": list_of_saves[currently_selected]},
						[])
				# Lets the button last longer in klicked mode
				pygame.time.delay(50)

		pygame.display.flip()
	pygame.mouse.set_visible(False)


def options():
	"""The settings menu"""

	#TODO WHAT IS BUTTON SIZE USED FOR?
	#button_size = menu.IO.read("./assets/templates/default.vars", "size")
	# a conversion method between selector
	# and actual text size
	# found by trial and error
	button_size = 12.5
	button_size = (button_size - 10) / 5.0

	settings_menu = menu_template("settings", 0, 0, 255,
			{"fullscreen": int(settings.fullscreen),
			"volume": settings.volume,
			"button_size": str(button_size)},
			[])

	sounds.music.play("pause")
	sounds.music.queue("$not$testsound.mp3", 0)
	sounds.music.play("play")

	run = True
	while run:

		events = settings_menu.run()
		for event in events:
			if event in ["event.EXIT", "event.QUIT", "return"]:
				pygame.mixer.music.pause()
				sounds.music.play("unpause")
				run = False
			if event == "volume":
				sounds.music.volume = float(event)
				settings.volume = float(event)
			if event == "fullscreen":
				settings.fullscreen = bool(event)
			if event == "button_Size":
				button_size = float(event)

			if event == "controls":
				change_controlls()
				settings_menu.update()

		sounds.music.update(False, False)
		pygame.display.flip()

	# explanation of the 10 + (5 * …) is written in
	# the Button Size handler in events loop
#	menu.IO.write("./assets/templates/default.vars", "size",
#			10 + (5 * button_size))
#	menu.IO.write("./assets/templates/default.vars", "ratio", 1100)
	settings.upd("adjust_screen")
	game_data.save_user_settings(	volume=settings.volume,
				# a conversion method between selector
				# and actual text size
				# found by trial and error
				size=10 + (5 * button_size),
				buttonmap=settings.buttonmap)
	pygame.mouse.set_visible(False)


def change_controlls():

	run = True
	curr_button_color = menu.IO.read("./assets/templates/default_vars.json",
				"color")

	keymap = {}
	for key in settings.buttonmap:
		keymap[key] = settings.buttonmap[key][0]
		keymap[key[:-4] + "_sec_key"] = settings.buttonmap[key][1]

	controls_menu = menu_template("change_controls", 5, 5, 150,
				keymap, [])

	while run:
		events = controls_menu.run()
		for event in events:
			if event in ["event.EXIT", "event.QUIT", "return"]:
				run = False
				break
			if event in keymap:
					pressed = controls_menu.menu.get_obj(event)
					pressed.changetext("Press to change", curr_button_color, 7)
					controls_menu.run()
					pygame.display.flip()
					new_label = choose_button(keymap, str(event))
					pressed.changetext(new_label, curr_button_color)

		pygame.display.flip()


def choose_button(key_map, key_name):
	choose = True
	while choose:
		settings.upd("get_events")
		for event in settings.events:
			if event.type == QUIT:
				return
			if event.type == KEYDOWN:

				old_key = key_map[key_name]
				new_key = pygame.key.name(event.key)
				if new_key == " ":
					new_key = "space"

				if "_sec_" in key_name:
					map_key = key_name.replace("_sec_", "_")
					index = 1
				else:
					map_key = key_name
					index = 0

				if new_key in list(key_map.values()):
					new_key = old_key
					print("Can't assign a key multible times")
				settings.buttonmap[map_key][index] = new_key

				choose = False
	return new_key
