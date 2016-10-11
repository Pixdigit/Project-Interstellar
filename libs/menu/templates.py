# -*- coding: utf-8 -*-
import pygame
from creator import create_menu


class element_template():

	#TODO FINISH

	def __init__(self):
		self.pos = pygame.Rext(0, 0, 0, 0)
		self.layer = 1
		self.name = "Generic Element"


class complete_template():

	def __init__(self, menu_config_path, screen, event_getter=pygame.event.get,
			variables={}, externals=[]):
		"""Initialize menu"""

		if not callable(event_getter):
			event_getter = lambda: event_getter

		self.event_getter = event_getter

		# import variables
		self.screenx, self.screeny = screen.get_size()
		self.screen = screen

		if type(variables) == dict:
			self.variables = lambda: variables
		elif callable(variables):
			self.variables = variables
		else:
			raise TypeError("The given argument for variables can not be understood.\n"
					"Please use a dict or a function that returns a dict.")

		self.externals = externals

		#strip filename
		self.menu_name = menu_config_path[
				menu_config_path.rfind("/") + 1:menu_config_path.rfind(".")]
		self.conf_path = menu_config_path

		# set mouse visible
		pygame.mouse.set_visible(True)

		# create menu
		self.menu = create_menu(
					menu_config_path,
					pygame.Rect((0, 0), (self.screenx, self.screeny)), self.variables)

		#TODO Add externals

	def run(self):
		events = self.event_getter()
		self.screen.fill((0, 0, 0))
		self.menu.blit(self.screen)
		self.menu.update(events)

		return event_converter(events, self.menu)

	def update(self, screen):
		self.screenx, self.screeny = screen.get_size()
		for external in self.externals:
			external.update(self.screenx, self.screeny)
		self.__init__(self.conf_path, screen, self.event_getter,
			self.variables, self.externals)


class slider_post():
	"""Custom class to represend sliders.
	This way we can use __eq__ to check for slider by name."""
	def __init__(self, slider_obj):
		self.name = slider_obj.name
		self.value = slider_obj.value
		self.index = slider_obj.get_selection_index()
		self.text = slider_obj.get_selection_name()

	def __eq__(self, other):
		return self.name == other


def event_converter(events, menu):
		new_events = []
		for event in events:
			if event.type == pygame.locals.QUIT:
				pygame.mouse.set_visible(False)
				new_events.append("event.EXIT")
			if event.type == pygame.locals.KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					pygame.mouse.set_visible(False)
					new_events.append("event.QUIT")
				if key in ["return", "enter"]:
					pygame.mouse.set_visible(False)
					new_events.append("event.CONTINUE")
				new_events.append(key)
			if event.type == pygame.locals.USEREVENT and event.code == "MENU":
				klicked = menu.get_klicked()
				for elem in klicked:
					elem.klicked = False
					new_events.append(elem.name)
			else:
				new_events.append(event)

		for slider in menu.get_types("slider"):
			if slider.dragged:
				tmp_event = slider_post(slider)
				new_events.append(tmp_event)
		return(new_events)
