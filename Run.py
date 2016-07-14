# -*- coding: utf-8 -*-
"""
Used to start the Game and ensure that everythings works fine.
Otherwise it reports an errormessage.
"""

import error_report
try:
	import pygame
	import sys
	import traceback
	import os

	os.environ['SDL_VIDEO_CENTERED'] = '1'

	#fix sound not playing correctly
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.init()
	# checks if font module is availible
	pygame.font
	# Checks for correct version
	if pygame.version.ver < "1.9.1":
		raise SystemExit("Old Pygame version: " + pygame.version.ver)
	version = sys.version.split(" ")[0].split(".")
	version[-1] = version[-1].split("+")[0]
	required = "2.7.6".split(".")
	for index in range(len(required)):
		if int(required[index]) < int(version[index]):
			break
		if int(required[index]) > int(version[index]):
			raise SystemExit("Outdated Python version: " + ".".join(version))
	if sys.version[:1] >= "3":
		raise SystemExit("No support for Python3")

	# Run the game
	from src import main
	main.void()
# Handeling errors
except ImportError as message:
	if str(message)[len(str(message)) - 6:] == "pygame":  # pygame not installed
		raise SystemExit("Pygame not installed")
	else:
		# unknown import error
		report = (("ERROR IMPORTING MODULES: %s" % message))
		print((report))
		error_report.send("Missing library at client:\n" + report)
		raise SystemExit(traceback.format_exc())
except AttributeError as detail:
	# excuted if font module is not installed
	detail = str(detail)
	print(detail)
	if detail[len(detail) - 5:][:4] == "font":  # Checking if font is cause
		raise SystemExit("Font module not installed (SDL_ttf)!")
	else:
		raise Exception(traceback.format_exc())  # Passing error to general handler
except Exception as detail:
	# general errors
	error_report.send(traceback.format_exc())
	raise SystemExit(traceback.format_exc())
