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
from pygame.locals import *

#Starts timer/clock for the movement, so it stays constant
pygame.time.set_timer(USEREVENT + 1, 25)

#initialize all variables for the modules
settings.init()
movement.init()
sounds.init()
movement.handle()
draw.init()
specials.init()


print(("Loading time: " + str(pygame.time.get_ticks() / 1000.0)))

if not settings.skip:
	menu.main()

#start clock for checking time how long has been played
global clock
clock = settings.clock

#start the missions
missions.init()


def main():
	while settings.run:

		#get events/user-input
		settings.upd("get_events")
		sounds.music.update(settings.events)

		#handle the user input
		interface.handle()

		#handles the movement every 25 milliseconds
		for event in settings.events:
			if event.type == USEREVENT + 1:
				movement.handle()

		#makes a clock tick (pygame internal stuff)
		clock.tick()

		#display everything
		draw.ingame()

		#check if missions have been fulfilled
		missions.handle("ingame")


while True:
	#basic cycle: Start game, when won show main menu
	main()
	settings.run = True
	settings.reset()
	menu.main()