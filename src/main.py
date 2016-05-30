# -*- coding: utf-8 -*-
"""
The Main function of the Game.
Controlls the general flow.
"""

import pygame
from . import movement
from . import settings
from . import interface
from . import draw
from . import menu
from . import missions
from . import specials
from . import sounds
from . import midi_in
from . import items
from . import overlay_handler
from pygame.locals import USEREVENT

# Starts timer/clock for the movement, so it stays constant
pygame.time.set_timer(USEREVENT + 1, 25)

# initialize all variables for the modules
settings.init()
interface.init()
draw.init()
movement.init()
sounds.init()
movement.handle()
specials.init()
midi_in.init()
items.init()
overlay_handler.init()

if not settings.skip:
	menu.main()

print(("Loading time:" + str(settings.loading_time / 1000.0)))
print(("Your seed is:" + str(settings.seed)))

# start clock for checking time how long has been played
global clock
clock = settings.clock

# start the missions
missions.init()


def main():
	while settings.run:

		# get events/user-input
		settings.upd("get_events")
		sounds.music.update(settings.events)
		sounds.music.volume = settings.volume

		# handle the user input
		interface.handle()

		# handles the movement every 25 milliseconds
		for event in settings.events:
			if event.type == USEREVENT + 1:
				movement.handle()

		# makes a clock tick (pygame internal stuff)
		clock.tick()

		# display everything
		draw.ingame()

		# check if missions have been fulfilled
		missions.handle()


while True:
	# basic cycle: Start game, when won show main menu
	main()
	settings.run = True
	settings.reset()
	menu.main()
