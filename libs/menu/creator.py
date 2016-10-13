# -*- coding: utf-8 -*-
import pygame
import json
import disp_elem
import os


def load_json(json_file):
	"""This loader returns filename when json loading failed"""
	with open(json_file) as conf_file:
		try:
			json_data = json.load(conf_file)
		except ValueError:
			raise ValueError("JSON loading error: " + json_file)
	return json_data


def add_key(key, dictionary, datatype):
	if key not in dictionary:
		dictionary[key] = datatype()
	return dictionary


def merge(iter1, iter2):
	"""Recursive merging of iter1 and iter2. Items in iter1 will be preserved"""

	if type(iter1) != type(iter2):
		raise ValueError("Cannot merge different iterables.")

	if type(iter1) == list:
		return list(set(iter1 + iter2))

	if type(iter1) == dict:
		for new_key in iter2:
			new_value = iter2[new_key]

			if type(new_value) not in [dict, list]:
				if new_key not in iter1:
					iter1[new_key] = new_value
			else:
				if new_key not in iter1:
					iter1[new_key] = iter2[new_key]
				else:
					iter1[new_key] = merge(iter1[new_key], iter2[new_key])

	return iter1


def load_vars(filename, pre_imports=[]):

	with open(filename)as data_file:
		menu_data = json.load(data_file)

	#add keys if not existing
	menu_data = add_key("variables", menu_data, dict)
	menu_data = add_key("imports", menu_data, list)
	variables = menu_data["variables"]

	#resolve imports
	imports = {}
	pre_imports.append(filename)
	for import_file in menu_data["imports"]:
		#prevent looping imports
		if import_file in pre_imports:
			continue
		else:
			#merge new vairables
			imports = merge(imports, load_vars(import_file, pre_imports=pre_imports))

	variables = merge(variables, imports)

	return variables


default_pos = {
	"pos_rel_obj": "master_screen",
	"from": "BottomRight",
	"to": "Center",
	"x_rel": 0.5,
	"y_rel": 0.5,
	"x_abs": 0,
	"y_abs": 0,
	"layer": 1}


class create_menu():

	def __init__(self, filename, ref, ref_updater, static=True):

		self.data_file = filename
		self.reference = ref
		self.menu_data = load_json(self.data_file)

		#load variables and dependencies
		#I dont know why the emtpy list. But it stops it from using the list
			#from the menu before
		self.variables = load_vars(self.data_file, [])

		#merge all types into list
		#and add std vars
		number_corrector = lambda float_var: (
						str(float_var * 100)[:str(float_var * 100).find(".")] + "%")
		floats_list = [number_corrector((x + 1) / 255.0) for x in range(255)]
		self.merged_variables = {"floats": floats_list}
		self.merged_variables.update(self.variables)

		#add custom runtime variables
		self.ref_updater = ref_updater
		self.merged_variables.update(self.ref_updater())

		self.load_objects()

		if static:
			self.merge_static()

	def load_objects(self):

		add_key("objects", self.menu_data, dict)
		add_key("sliders", self.menu_data["objects"], list)
		add_key("buttons", self.menu_data["objects"], list)
		add_key("titles", self.menu_data["objects"], list)
		add_key("images", self.menu_data["objects"], list)

		self.object_data = self.menu_data["objects"]
		self.objects = []

		def get_data(data_dict, key_name, expect_type=None, default=None):

			def type_mismatch(expect_type):
				if expect_type is None:
					expect_type = "<type \"NoneType\">"
				error = (self.data_file[self.data_file.rfind("/") + 1:]
					+ ": "
					+ str(key_name)
					+ " should be an: "
					+ str(expect_type)[7:-2]
					+ " | Got an: "
					+ str(type(data_in))[7:-2]
					+ " == "
					+ str(data_in)
					)
				raise ValueError(error)

			#Try to load value
			try:
				data_in = data_dict[key_name]
			except KeyError:
				#Not in dict -> Raise error or return default
				if default is not None and key_name not in data_dict:
					return default

				if not "name" in data_dict:
					data_dict["name"] = "NONAME"
				error = (str(key_name)
					+ " is not a property of: "
					+ data_dict["name"]
					)
				raise KeyError(error)

			#Got a vairable
			if (type(data_in) in [str, unicode]) and data_in[0] == "$":
				#Try to load variable
				try:
						data_in = get_data(self.merged_variables, data_in[1:])
				except KeyError:
					print ""
					print self.merged_variables
					raise KeyError(data_in + " is not a variable.")
				return data_in

			#If we expect a string anything goes
			if expect_type in [str, unicode]:
				return str(data_in)
			#If we expect int Try resolving percentages
			elif expect_type in [int, float]:
				try:
					if type(data_in) in [str, unicode]:
						if data_in[0] == "%":
							try:
								return float(data_in[1:]) / 100
							except ValueError:
								type_mismatch(float)
						else:
							return float(data_in)
					else:
						try:
							return float(data_in)
						except TypeError:
							type_mismatch(float)
				except ValueError:
					type_mismatch(expect_type)
			#If we got a list recursively resolve
			elif type(data_in) == list:
				new_list = []
				for item in data_in:
					#merge if element is list
					if type(item) in [str, unicode] and item[0] == "$":
						if type(self.merged_variables[item[1:]]) == list:
							new_list = new_list + get_data(data_in, data_in.index(item), None)
						else:
							new_list.append(str(self.merged_variables[item[1:]]))
					else:
						new_list.append(get_data(data_in, data_in.index(item), None))
				return new_list
			#If we got a dict recursively resovle that
			elif type(data_in) == dict:
				new_data = {}
				for key in data_in:
					new_data[key] = get_data(data_in, key)
				return new_data
			#If input is int there is not much else to return
			elif type(data_in) in [int, float]:
				return float(data_in)
			#If input is bool return bool
			elif type(data_in) == bool:
				return data_in
			#If no expection is given try float first then usual value
			elif expect_type is None:
				try:
					return get_data(data_dict, key_name, float)
				except ValueError:
					return data_in
			else:
				#If nothing else works return blank input
				if type(data_in) == expect_type or expect_type is None:
					return data_in
				else:
					type_mismatch(expect_type)
			raise RuntimeError("I have no idea how this happend! : "
					+ str(data_in) + " | " + str(expect_type))


		default_font = {
			"color": [0, 0, 0],
			"font": "monospace",
			"size": 20,
			"bold": False,
			"italics": False,
			"underline": False,
			"anitalias": True}

		#create titles
		for title_data in self.object_data["titles"]:
			name = get_data(title_data, "name", str)
			label = get_data(title_data, "label", str, default="")
			font_conf = get_data(title_data, "font_conf", dict, default=default_font)
			pos_data = get_data(title_data, "position", dict, default=default_pos)
			layer = pos_data["layer"]

			for attr in ["color", "font", "size",
				"bold", "italics", "underline", "antialias"]:
				if attr in title_data:
					font_conf[attr] = get_data(title_data, attr)

			self.objects.append(disp_elem.text(name, label, font_conf,
						pos_data, layer=layer))

		#create buttons
		for button_data in self.object_data["buttons"]:
			name = get_data(button_data, "name", str)
			content = get_data(button_data, "content", str, default="")
			box = get_data(button_data, "box", list)
			ratio = get_data(button_data, "width_to_hight_ratio", float, default=1)
			pos_data = get_data(button_data, "position", dict, default=default_pos)
			layer = pos_data["layer"]

			if type(content) in [str, unicode] and os.path.isfile(content):
				try:
					content = pygame.image.load(content)
				except pygame.error:
					print(("Could not load image file: " + content))
					print(("Using filename as text.\n"))
			elif type(content) == pygame.Surface:
				image = content.convert()
				content = disp_elem.image("NONAME", image, {"NOPOSDATA": True})
			else:
				font_conf = get_data(button_data, "font_conf", default=default_font)

				for attr in ["color", "font", "size",
					"bold", "italics", "underline", "antialias"]:
					if attr in button_data:
						font_conf[attr] = get_data(button_data, attr)
				content = disp_elem.text("NONE42", content, font_conf,
						default_pos, layer=0)

			self.objects.append(
					disp_elem.button(name, content, ratio, box, pos_data, layer=layer))

		#create sliders
		for slider_data in self.object_data["sliders"]:
			name = get_data(slider_data, "name", str)
			label = get_data(slider_data, "label", str, default="")
			typeface = get_data(slider_data, "typeface", str, default="monospace")
			size = get_data(slider_data, "size", int)
			color = get_data(slider_data, "color", list, default=(255, 255, 255))
			options_list = get_data(slider_data, "selection_range", list)
			default_value = get_data(slider_data, "preset_value", float)
			box = get_data(slider_data, "box", list)
			ratio = get_data(slider_data, "width_to_hight_ratio", float)
			pos_data = get_data(slider_data, "position", dict, default=default_pos)
			layer = pos_data["layer"]

			self.objects.append(disp_elem.slider(name, label, typeface, color, size,
					ratio, options_list, default_value, box, pos_data, layer=layer))

		#create images
		for image_data in self.object_data["images"]:
			img = disp_elem.image(
					get_data(image_data, "name", str),
					get_data(image_data, "image", str),
					get_data(image_data, "position", dict, default=default_pos),
					layer=get_data(image_data, "position", dict, default=default_pos)["layer"])

			self.objects.append(img)

		for obj in self.objects:
			obj.get_rel_pos([self.reference] + self.objects)

	def merge_static(self):

		#TODO: Finish merging all mergable types

		merge_elems = {}

		for elem in self.objects:
			if elem.type == "text":
				merge_elems[elem.text_img] = elem.layer
			if elem.type == "image":
				merge_elems[elem.image] = elem.layer

	def update(self, events):
		for obj in self.objects:
			obj.update(events)

	def blit(self, screen):
		self.objects.sort(key=lambda obj: obj.layer)
		for obj in self.objects:
			obj.blit(screen)

	def get_klicked(self):
		klicked = []
		for obj in self.objects:
			if obj.type == "button":
				if obj.klicked:
					klicked.append(obj)
		return klicked

	def get_types(self, obj_type):
		obj_list = []
		for obj in self.objects:
			if obj.type == obj_type:
				obj_list.append(obj)
		return obj_list

	def get_obj(self, name):
		for obj in self.objects:
			if obj.name == name:
				return obj
