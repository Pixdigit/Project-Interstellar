# -*- coding: utf-8 -*-
import pygame


global default_font_conf
default_font_conf = {
		"color": [0, 0, 0],
		"font": "monospace",
		"size": 20,
		"bold": False,
		"italics": False,
		"underline": False,
		"anitalias": True}


def get_point(rect, point_name):
	point_name = point_name.lower()
	if point_name == "topleft":
		return rect.topleft
	if point_name in ["topcenter", "topmid"]:
		return rect.midtop
	if point_name == "topright":
		return rect.topright
	if point_name == "centerleft":
		return rect.midleft
	if point_name in ["centercenter", "center", "midmid", "mid"]:
		return rect.center
	if point_name == "centerright":
		return rect.midright
	if point_name == "bottomleft":
		return rect.bottomleft
	if point_name in ["bottomcenter", "bottommid"]:
		return rect.midbottom
	if point_name == "bottomright":
		return rect.bottomright

	#did not match
	raise ValueError(point_name + " is not a valid point.")


class element_template():

	def __init__(self):
		self.pos = pygame.Rect(0, 0, 0, 0)
		self.layer = 1
		self.name = "Generic Element"
		self.type = "custom"
		self.pos_data = {
				"pos_rel_obj": "master_screen",
				"from": "BottomRight",
				"to": "Center",
				"x_rel": 0.5,
				"y_rel": 0.5,
				"x_abs": 0,
				"y_abs": 0,
				"layer": 1}
		self.img = pygame.Surface((0, 0)).convert()

		self.checked = False
		self.active_pos_search = False

	def get_rel_pos(self, object_list):
		#set status
		self.checked = True
		self.active_pos_search = True

		if self.pos_data["pos_rel_obj"] == "master_screen":
			rel_pos = object_list[0]
			self.pos_data["from"] = "BottomRight"
		else:
			#search and get relational points
			for obj in object_list[1:]:
				if obj.name == self.pos_data["pos_rel_obj"]:
					if obj.checked:
						if obj.active_pos_search:
							#tried to load from undeterminable position
							raise RuntimeError("Relational position refers to itself.")
						else:
							rel_pos = obj.pos
					else:
						rel_pos = obj.get_rel_pos(object_list)
		#get point from rect
		rel_point = get_point(rel_pos, self.pos_data["from"])

		#update position
		self.pos.x = int(self.pos_data["x_abs"]
				+ (self.pos_data["x_rel"] * rel_point[0]))
		self.pos.y = int(self.pos_data["y_abs"]
				+ (self.pos_data["y_rel"] * rel_point[1]))

		#set "to" pos to "from" pos
		dest_point = self.pos.topleft
		org_point = get_point(self.pos, self.pos_data["to"])
		self.pos.x += dest_point[0] - org_point[0]
		self.pos.y += dest_point[1] - org_point[1]

		#reset status and return pos for recursion
		self.active_pos_search = False
		return self.pos

	def get_size(self):
		return self.pos.size

	def update(self, events):
		"""Process events"""
		pass

	def adjust(self, screen):
		"""Adjust to new screen size"""
		pass

	def blit(self, screen):
		screen.blit(self.img, self.pos)

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
		# And prevent looping imports
		from creator import create_menu
		self.menu = create_menu(
					menu_config_path,
					pygame.Rect((0, 0), (self.screenx, self.screeny)), self.variables)

		self.menu.objects = self.menu.objects + externals

	def run(self):
		events = self.event_getter()
		self.screen.fill((0, 0, 0))
		self.menu.blit(self.screen)
		self.menu.update(events)

		return event_converter(events, self.menu)

	def update(self, screen):
		self.screenx, self.screeny = screen.get_size()
		for external in self.externals:
			external.adjust(self.screenx, self.screeny)
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
